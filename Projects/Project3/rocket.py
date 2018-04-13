import gym
import numpy as np

env = gym.make('RocketLander-v0')
env.reset()
goal_steps = 500


def some_random_games():
    for episode in range(1):
      env.reset()
      for t in range(goal_steps):
        env.render()
        # action = env.action_space.sample()
        action = [1,1,-1]
        
        observation, reward, done, info = env.step(action)
        print("Action: {} Observations Size:{} score: {}".format(action,observation.shape,reward))
        if done:
          break

some_random_games()
