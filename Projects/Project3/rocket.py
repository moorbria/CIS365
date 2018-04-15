import gym
import numpy as np

env = gym.make('RocketLander-v0')
env.reset()
goal_steps = 500

initial_games = 100

def some_random_games():
    for episode in range(initial_games):
      observation = env.reset()
      total_reward = 0
      for t in range(goal_steps):
        #env.render()
        action = env.action_space.sample()
        #gimbal = calc_gimbal(observation)
        #throttle = calc_throttle(observation)
        #thruster = calc_thruster(observation)
        
        #action = [gimbal, throttle, thruster]
        
        observation, reward, done, info = env.step(action)
        total_reward += reward
        #print("Action: {} Observations Size:{} score: {}".format(action,observation.shape,reward))
        if done:
          break
      print("Total Reward: " + str(total_reward))


some_random_games()
