import hlt
import logging
from collections import OrderedDict
game = hlt.Game("Bakesauce-V5.0")
logging.info("Starting Bakesauce")
counter = 0
while True:
    logging.info("Turn: " + str(counter))
    game_map = game.update_map()
    counter += 1	
    command_queue = []
    planned_planets = []
    planned_ships = []
    team_ships = game_map.get_me().all_ships()
    modelship = team_ships[0]
    modelshipid = team_ships[0].id
    firstTurn = True

    if len(team_ships) <= 5:
        for s in team_ships:
            if s.x != modelship.x or s.y != modelship.y:
                logging.info("not first turn")
                firstTurn = False
                break
            else:
                logging.info("first turn")
                firstTurn = True
                continue
    
    for ship in game_map.get_me().all_ships():
        navigate_command = False
        logging.info("ship: " + str(ship.id))
        logging.info("ship docking status: " + str(ship.docking_status))
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            logging.info("docked")
            # Skip this ship
            continue

        #Taken from Sentech
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        
        #Taken from Sentech
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        #Taken from Sentech
        
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]
        
        if ship.id == modelship.id:
            if len(closest_empty_planets) > 0: #To fix, when no empty planets left
                target_planet = closest_empty_planets[0]
                if ship.can_dock(target_planet):
                    logging.info("dock ship")
                    command_queue.append(ship.dock(target_planet))
                else:
                    if target_planet in planned_planets:
                        continue
                    else:
                        logging.info("1")
                        navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                        if navigate_command:
                            command_queue.append(navigate_command)
                            planned_planets.append(target_planet)
            
            else: #if len(closest_enemy_ships) > 0:
                target_ship = closest_enemy_ships[0]
                logging.info("2")
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_ship),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)
        else:
            if firstTurn:
                if len(team_ships) > 1 and ship.id != team_ships[1].id:
                    for compareShip in team_ships:
                        if ship.id == compareShip.id:
                            continue
                        elif ship.calculate_distance_between(compareShip) <= 5:
                            angle = ship.calculate_angle_between(compareShip)
                            logging.info("3")
                            navigate_command = ship.thrust(
                                int(hlt.constants.MAX_SPEED),
                                abs(angle-75))
                        else:
                            continue
                else:
                    target_ship = closest_enemy_ships[0]
                    logging.info("4")

                    navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)
                        
                if navigate_command:
                    command_queue.append(navigate_command)
            else:
                if len(closest_enemy_ships) <= 6: #and Entity.calculate_distance_between(closest_enemy_ships[0]) < 500:
                    target_ship = closest_enemy_ships[0]
                    logging.info("5")
                    navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)
                else: 
                    if len(closest_empty_planets) > 0:
                        target_planet = closest_empty_planets[0]
                        if ship.can_dock(target_planet):
                            command_queue.append(ship.dock(target_planet))
                        else:
                            logging.info("6")
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_planet),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)

                            if navigate_command:
                                command_queue.append(navigate_command)
                                planned_planets.append(target_planet)
                    else:
                        target_ship = closest_enemy_ships[0]
                        logging.info("7")
                        navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)
                        
                        if navigate_command:
                            command_queue.append(navigate_command)

        logging.info(str(navigate_command))
    game.send_command_queue(command_queue)
    # TURN END
# GAME END


