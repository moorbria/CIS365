import heapq
import numpy as np
import os
import time
import logging
import hlt
from collections import OrderedDict
import itertools
from tsmlstarterbot.common import *
from tsmlstarterbot.neural_net import NeuralNet


class Bot:
    def __init__(self, location, name):
        self.first_turn = True
        self._name = "Testing" #name
        self._game = hlt.Game(self._name)
        self._location = location
        #self.game = hlt.Game(self._name)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self._game_map = self._game.map
        game_map_area = (self._game_map.width * self._game_map.height)
        logging.info(str(game_map_area))
        if(game_map_area > 40000):
            #model_location = os.path.join(current_directory, os.path.pardir, "models/" + game_player_count + "s", location)
            model_location = os.path.join(current_directory, os.path.pardir, "models", location)
            self._neural_net = NeuralNet(cached_model=model_location)
        
            # Run prediction on random data to make sure that code path is executed at least once before the game starts
            random_input_data = np.random.rand(PLANET_MAX_NUM, PER_PLANET_FEATURES)
            predictions = self._neural_net.predict(random_input_data)
            assert len(predictions) == PLANET_MAX_NUM
            logging.info("End of init")
        else:
            logging.info("small map")
            decision_bot(self._game)
			

    def play(self):
        """
        Play a game using stdin/stdout.
        """

        # Initialize the game.
        #game = hlt.Game(self._name)
        logging.info("before while loop")
        game_map = self._game_map
        while True:
            # Update the game map.
            if self.first_turn:
                game_map = self._game.update_map()
            self.first_turn = True
            start_time = time.time()
            logging.info("after start_time")
            # Produce features for each planet.
            features = self.produce_features(game_map)

            # Find predictions which planets we should send ships to.
            predictions = self._neural_net.predict(features)

            # Use simple greedy algorithm to assign closest ships to each planet according to predictions.
            ships_to_planets_assignment = self.produce_ships_to_planets_assignment(game_map, predictions)

            # Produce halite instruction for each ship.
            instructions = self.produce_instructions(game_map, ships_to_planets_assignment, start_time)

            # Send the command.
            logging.info("sending command")
            self._game.send_command_queue(instructions)

    def produce_features(self, game_map):
        """
        For each planet produce a set of features that we will feed to the neural net. We always return an array
        with PLANET_MAX_NUM rows - if planet is not present in the game, we set all featurse to 0.

        :param game_map: game map
        :return: 2-D array where i-th row represents set of features of the i-th planet
        """
        feature_matrix = [[0 for _ in range(PER_PLANET_FEATURES)] for _ in range(PLANET_MAX_NUM)]

        for planet in game_map.all_planets():

            # Compute "ownership" feature - 0 if planet is not occupied, 1 if occupied by us, -1 if occupied by enemy.
            if planet.owner == game_map.get_me():
                ownership = 1
            elif planet.owner is None:
                ownership = 0
            else:  # owned by enemy
                ownership = -1

            my_best_distance = 10000
            enemy_best_distance = 10000

            gravity = 0

            health_weighted_ship_distance = 0
            sum_of_health = 0

            for player in game_map.all_players():
                for ship in player.all_ships():
                    d = ship.calculate_distance_between(planet)
                    if player == game_map.get_me():
                        my_best_distance = min(my_best_distance, d)
                        sum_of_health += ship.health
                        health_weighted_ship_distance += d * ship.health
                        gravity += ship.health / (d * d)
                    else:
                        enemy_best_distance = min(enemy_best_distance, d)
                        gravity -= ship.health / (d * d)

            distance_from_center = distance(planet.x, planet.y, game_map.width / 2, game_map.height / 2)

            health_weighted_ship_distance = health_weighted_ship_distance / sum_of_health

            remaining_docking_spots = planet.num_docking_spots - len(planet.all_docked_ships())
            signed_current_production = planet.current_production * ownership

            is_active = remaining_docking_spots > 0 or ownership != 1

            feature_matrix[planet.id] = [
                planet.health,
                remaining_docking_spots,
                planet.remaining_resources,
                signed_current_production,
                gravity,
                my_best_distance,
                enemy_best_distance,
                ownership,
                distance_from_center,
                health_weighted_ship_distance,
                is_active
            ]

        return feature_matrix

    def produce_ships_to_planets_assignment(self, game_map, predictions):
        """
        Given the predictions from the neural net, create assignment (undocked ship -> planet) deciding which
        planet each ship should go to. Note that we already know how many ships is going to each planet
        (from the neural net), we just don't know which ones.

        :param game_map: game map
        :param predictions: probability distribution describing where the ships should be sent
        :return: list of pairs (ship, planet)
        """
        undocked_ships = [ship for ship in game_map.get_me().all_ships()
                          if ship.docking_status == ship.DockingStatus.UNDOCKED]

        # greedy assignment
        assignment = []
        number_of_ships_to_assign = len(undocked_ships)

        if number_of_ships_to_assign == 0:
            return []

        planet_heap = []
        ship_heaps = [[] for _ in range(PLANET_MAX_NUM)]

        # Create heaps for greedy ship assignment.
        for planet in game_map.all_planets():
            # We insert negative number of ships as a key, since we want max heap here.
            heapq.heappush(planet_heap, (-predictions[planet.id] * number_of_ships_to_assign, planet.id))
            h = []
            for ship in undocked_ships:
                d = ship.calculate_distance_between(planet)
                heapq.heappush(h, (d, ship.id))
            ship_heaps[planet.id] = h

        # Create greedy assignment
        already_assigned_ships = set()

        while number_of_ships_to_assign > len(already_assigned_ships):
            # Remove the best planet from the heap and put it back in with adjustment.
            # (Account for the fact the distribution values are stored as negative numbers on the heap.)
            ships_to_send, best_planet_id = heapq.heappop(planet_heap)
            ships_to_send = -(-ships_to_send - 1)
            heapq.heappush(planet_heap, (ships_to_send, best_planet_id))

            # Find the closest unused ship to the best planet.
            _, best_ship_id = heapq.heappop(ship_heaps[best_planet_id])
            while best_ship_id in already_assigned_ships:
                _, best_ship_id = heapq.heappop(ship_heaps[best_planet_id])

            # Assign the best ship to the best planet.
            assignment.append(
                (game_map.get_me().get_ship(best_ship_id), game_map.get_planet(best_planet_id)))
            already_assigned_ships.add(best_ship_id)

        return assignment

    def produce_instructions(self, game_map, ships_to_planets_assignment, round_start_time):
        """
        Given list of pairs (ship, planet) produce instructions for every ship to go to its respective planet.
        If the planet belongs to the enemy, we go to the weakest docked ship.
        If it's ours or is unoccupied, we try to dock.

        :param game_map: game map
        :param ships_to_planets_assignment: list of tuples (ship, planet)
        :param round_start_time: time (in seconds) between the Epoch and the start of this round
        :return: list of instructions to send to the Halite engine
        """
        command_queue = []
        # Send each ship to its planet
        for ship, planet in ships_to_planets_assignment:
            speed = hlt.constants.MAX_SPEED

            is_planet_friendly = not planet.is_owned() or planet.owner == game_map.get_me()

            if is_planet_friendly:
                if ship.can_dock(planet):
                    command_queue.append(ship.dock(planet))
                else:
                    command_queue.append(
                        self.navigate(game_map, round_start_time, ship, ship.closest_point_to(planet), speed))
            else:
                docked_ships = planet.all_docked_ships()
                assert len(docked_ships) > 0
                weakest_ship = None
                for s in docked_ships:
                    if weakest_ship is None or weakest_ship.health > s.health:
                        weakest_ship = s
                command_queue.append(
                    self.navigate(game_map, round_start_time, ship, ship.closest_point_to(weakest_ship), speed))
        return command_queue

    def navigate(self, game_map, start_of_round, ship, destination, speed):
        """
        Send a ship to its destination. Because "navigate" method in Halite API is expensive, we use that method only if
        we haven't used too much time yet.

        :param game_map: game map
        :param start_of_round: time (in seconds) between the Epoch and the start of this round
        :param ship: ship we want to send
        :param destination: destination to which we want to send the ship to
        :param speed: speed with which we would like to send the ship to its destination
        :return:
        """
        current_time = time.time()
        have_time = current_time - start_of_round < 1.2
        navigate_command = None
        if have_time:
            navigate_command = ship.navigate(destination, game_map, speed=speed, max_corrections=180)
        if navigate_command is None:
            # ship.navigate may return None if it cannot find a path. In such a case we just thrust.
            dist = ship.calculate_distance_between(destination)
            speed = speed if (dist >= speed) else dist
            navigate_command = ship.thrust(speed, ship.calculate_angle_between(destination))
        return navigate_command


def decision_bot(game):

    #TODO: remove planned_ships or loop through ships and change ship to attack
    def minePlanet(p):
        if ship.can_dock(p):
            return ship.dock(p)
        else:
            #if p not in planned_planets:
            return ship.navigate(
                ship.closest_point_to(p),
                game_map,
                speed=int(hlt.constants.MAX_SPEED))

    def attackShip(p):
        #if p not in planned_ships:
        return ship.navigate(
            ship.closest_point_to(p),
            game_map,
            speed=int(hlt.constants.MAX_SPEED))


    while True:
        game_map = game.update_map()
        command_queue = []
        planned_planets = []
        planned_ships = []
        team_ships = game_map.get_me().all_ships()
        sorted(team_ships, key=lambda ship:ship.id)
        firstTurn = False
        orderedTeamShipsByY = team_ships
        sorted(orderedTeamShipsByY, key=lambda ship:ship.y)
        modelship = team_ships[0]
        modelshipid = team_ships[0].id

        """if len(team_ships) == 3:
            for s in team_ships:
                if s.x != modelship.x:
                    break
                else:
                    firstTurn = True"""

        if len(team_ships) <= 5:
            for s in team_ships:
                if s.x != modelship.x or s.y != modelship.y:
                    firstTurn = False
                    break
                else:
                    firstTurn = True
                    continue
                
        for ship in game_map.get_me().all_ships():
            navigate_command = False
            shipid = ship.id
            if ship.docking_status != ship.DockingStatus.UNDOCKED:
                # Skip this ship
                continue

            #Taken from Sentech
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
            
            #Taken from Sentech
            closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

            #Taken from Sentech
            closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]
            
            if len(team_ships) <= 3 and ship.id != modelshipid:
                for compareShip in team_ships:
                    if ship.id == compareShip.id:
                        continue
                    elif ship.calculate_distance_between(compareShip) <= 5:
                        if ship.y > compareShip.y:
                            navigate_command = ship.thrust(
                                int(hlt.constants.MAX_SPEED),
                                120)
                            if navigate_command:
                                command_queue.append(navigate_command)
                        elif ship.y < compareShip.y:
                            navigate_command = ship.thrust(
                                int(hlt.constants.MAX_SPEED),
                                0)
                            if navigate_command:
                                command_queue.append(navigate_command)
                        else:
                            navigate_command = ship.thrust(
                                int(hlt.constants.MAX_SPEED),
                                90)
                            if navigate_command:
                                command_queue.append(navigate_command)
                    else:
                        for tship in closest_enemy_ships:
                            if tship in planned_ships:
                                continue
                            else:
                                navigate_command = attackShip(tship)

                                if navigate_command:
                                    planned_ships.append(tship)
                                    command_queue.append(navigate_command)
                                
                                break
                    break
            
            if navigate_command is False:

                if ship.id == modelship.id:
                    if len(closest_empty_planets) > 0: #To fix, when no empty planets left. I think fixed.
                        target_planet = closest_empty_planets[0]
                        navigate_command = minePlanet(target_planet)

                        if navigate_command:
                            #planned_planets.append(target_planet)
                            command_queue.append(navigate_command)
                    
                    else: #if len(closest_enemy_ships) > 0: Add planned_ships[]
                        #target_ship = closest_enemy_ships[0]
                        for tship in closest_enemy_ships:
                            if tship in planned_ships:
                                continue
                            else:
                                navigate_command = attackShip(tship)

                                if navigate_command:
                                    planned_ships.append(tship)
                                    command_queue.append(navigate_command)
                                
                                break
                else:
                    if firstTurn:
                        if len(team_ships) > 1: #and ship.id != team_ships[1].id:
                            for compareShip in team_ships:
                                if ship.id == compareShip.id:
                                    continue
                                elif ship.calculate_distance_between(compareShip) <= 10:
                                    if ship.id == orderedTeamShipsByY[0].id:
                                        navigate_command = ship.thrust(
                                            int(hlt.constants.MAX_SPEED),
                                            120)
                                        if navigate_command:
                                            command_queue.append(navigate_command)
                                    elif ship.id == orderedTeamShipsByY[2].id:
                                        navigate_command = ship.thrust(
                                            int(hlt.constants.MAX_SPEED),
                                            300)
                                        if navigate_command:
                                            command_queue.append(navigate_command)
                                    else:
                                        navigate_command = ship.thrust(
                                            int(hlt.constants.MAX_SPEED),
                                            180)
                                        if navigate_command:
                                            command_queue.append(navigate_command)
                                else:
                                    for tship in closest_enemy_ships:
                                        if tship in planned_ships:
                                            continue
                                        else:
                                            navigate_command = attackShip(tship)

                                            if navigate_command:
                                                planned_ships.append(tship)
                                                command_queue.append(navigate_command)
                                            
                                            break
                        else:
                            for tship in closest_enemy_ships:
                                if tship in planned_ships:
                                    continue
                                else:
                                    navigate_command = attackShip(tship)

                                    if navigate_command:
                                        planned_ships.append(tship)
                                        command_queue.append(navigate_command)
                                    
                                    break
                            
                    else:
                        if len(closest_enemy_ships) <= 6: #and Entity.calculate_distance_between(closest_enemy_ships[0]) < 500:
                            for tship in closest_enemy_ships:
                                if tship in planned_ships:
                                    continue
                                else:
                                    navigate_command = attackShip(tship)

                                    if navigate_command:
                                        planned_ships.append(tship)
                                        command_queue.append(navigate_command)
                                    
                                    break
                        else: 
                            if len(closest_empty_planets) > 0:
                                target_planet = closest_empty_planets[0]
                                navigate_command = minePlanet(target_planet)

                                if navigate_command:
                                    planned_planets.append(target_planet)
                                    command_queue.append(navigate_command)
                            else:
                                for tship in closest_enemy_ships:
                                    if tship in planned_ships:
                                        continue
                                    else:
                                        navigate_command = attackShip(tship)

                                        if navigate_command:
                                            planned_ships.append(tship)
                                            command_queue.append(navigate_command)
                                        
                                        break

        game.send_command_queue(command_queue)
        # TURN END
    # GAME END


