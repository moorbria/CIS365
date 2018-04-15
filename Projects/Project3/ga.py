import gym
import random
import numpy as np
from deap import creator, base, tools, algorithms


creator.create("FBar", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FBar)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def fitness(reward):
  print(reward)

# register the evaluation of the fitness function
toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

env = gym.make('RocketLander-v0')
env.reset()
goal_steps = 500
NGEN = 3
def some_random_games():
    for episode in range(NGEN):
        observation = env.reset()
      for t in range(goal_steps):
        population = toolbox.population(n=300)
        fits = toolbox.map(toolbox.evaluate,offspring)
        env.render()
        # action = env.action_space.sample()
        gimbal = calc_gimbal(observation)
        throttle = calc_throttle(observation)
        thruster = calc_thruster(observation)
        
        action = [gimbal, throttle, thruster]
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
          ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population)) 
        observation, reward, done, info = env.step(action)
        fitness(reward)
        print("Action: {} Observations Size:{} score: {}".format(action,observation.shape,reward))
        if done:
          break


def calc_gimbal(observation):
  gimbal = 0 # default change nothing 
 
  return gimbal

def calc_throttle(observation):
  throttle= 0 # default change nothing 
 
  return throttle

def calc_thruster(observation):
  thruster = 0 # default change nothing  
  return observation[0]


some_random_games()
