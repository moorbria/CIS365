import gym
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

LR = 1e-3

env = gym.make('RocketLander-v0')
env.reset()
goal_steps = 500
score_requirement = 3500
initial_games = 100000

def some_random_games():

    for episode in range(initial_games):
      observation = env.reset()
      total_reward = 0
      print(episode % 10)
      if episode % 1000 is 0:
        print(str((initial_games/episode)*100) + "% Complete")
      for t in range(goal_steps):
        #env.render()
        action = env.action_space.sample()
        
        observation, reward, done, info = env.step(action)

        total_reward += reward
        #print("Action: {} Observations Size:{} score: {}".format(action,observation.shape,reward))
        if done:
          break
      print("Total Reward: " + str(total_reward))

#some_random_games()

def initial_population():
    # [OBS, MOVES]
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []


    # iterate through however many games we want:
    for episode in range(initial_games):
        if episode % 1000 is 0 and episode != 0:
          print(str(episode/initial_games*100) + "% Complete")

        score = 0
        # moves specifically from this environment:
        game_memory = []
        # previous observation that we saw
        prev_observation = []
        # for each frame in 200
        for episode in range(goal_steps):
            a = float(random.randrange(-100, 100))/100
            b = float(random.randrange(0, 100))/100
            c = float(random.randrange(-100, 100))/100
            action = [a, b, c]

            # do it!
            observation, reward, done, info = env.step(action)


            # normailize data
            norm_observation = normalize(observation)
            #print(norm_observation)

            # custom reward function
            reward = 0
            # Reward for staying upright
            reward = 2 - abs(.5 - norm_observation[2])
            
            if observation[1] < -.5:
                reward += 3 - abs(.5 - norm_observation[2])

            # Reward for angular velocity (don't spin that fast)
            if observation[9] < 35:
                reward += 4 - abs(.5 - norm_observation[9])

            reward += 2 - abs((.5 - norm_observation[0]))
                       
            
            # Reward for low speed at the end and no spin
            #if observation[1] < -.5: # y position is in the last quadrant
                #reward -= abs(observation[7]) 
            # notice that the observation is returned FROM the action
            # so we'll store the previous observation here, pairing
            # the prev observation to the action we'll take.
            if len(prev_observation) > 0 :
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score+=reward
            if done: break

        # IF our score is higher than our threshold, we'd like to save
        # every move we made
        # NOTE the reinforcement methodology here. 
        # all we're doing is reinforcing the score, we're not trying 
        # to influence the machine in any way as to HOW that score is 
        # reached.
        #print(score)
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
                if data[1] == 1:
                    output = [0,1]
                elif data[1] == 0:
                    output = [1,0]
                else:
                    output = data[1]
                    
                # saving our training data
                training_data.append([data[0], output])

        # reset env to play again
        env.reset()
        # save overall scores



    # just in case you wanted to reference later
    training_data_save = np.array(training_data)
    np.save('saved.npy',training_data_save)
    
    # some stats here, to further illustrate the neural network magic!
    print('Average accepted score:',mean(accepted_scores))
    print('Median score for accepted scores:',median(accepted_scores))
    print("Count Accepted", len(accepted_scores))
    
    return training_data

def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='softmax')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='softmax')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='softmax')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='softmax')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='softmax')
    network = dropout(network, 0.8)

    network = fully_connected(network, 3, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

def train_model(training_data, model=False):
    #print(training_data[0])
    X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
    y = [i[1] for i in training_data]
  
    #print(X)
    #print(len(X[0]))
    #print(y)

    if not model:
        print("here")
        model = neural_network_model(input_size = len(X[0]))
    
    model.fit({'input': X}, {'targets': y}, n_epoch=5, snapshot_step=500, show_metric=True, run_id='openai_learning')
    return model


def normalize(observation):
  observation[0] = (observation[0] - (-3.5))/(3.5 - (-3.5))
  observation[1] = (observation[1] - (-1.5))/(1.7 - (-1.5))
  observation[2] = (observation[2] - (-12))/(12 - (-12))
# observation[3] = (observation[3] - (-3.5))/(3.5 - (-3.5))
# observation[4] = (observation[4] - (-3.5))/(3.5 - (-3.5))
  observation[5] = (observation[5] - (-1.3))/(1 - (-1.3))
  observation[6] = (observation[6] - (-1))/(1 - (-1))
  observation[7] = (observation[7] - (-14))/(14 - (-14))
  observation[8] = (observation[8] - (-2.7))/(0 - (-2.7))
  observation[9] = (observation[9] - (-36))/(36 - (-36))

  return observation


training_data = initial_population()
#training_data = np.load('saved.npy')
model = train_model(training_data)
#model = neural_network_model(10)
#model.load('1.model')

scores = []
choices = []
x_position = []
y_position = []
angle = []
first_leg = []
second_leg = []
throttle = []
gimbal = []
x_vel = []
y_vel = []
angle_vel = []

for each_game in range(10):
    


    score = 0
    game_memory = []
    prev_obs = []
    env.reset()
    for _ in range(goal_steps):
        env.render()
        #print(prev_obs)
        if len(prev_obs)==0:
            a = float(random.randrange(-100, 100))/100
            b = float(random.randrange(-100, 100))/100
            c = float(random.randrange(-100, 100))/100
            action = [a, b, c]
        else:
            #print(prev_obs)
            #print(model.predict(prev_obs.reshape(-1,len(prev_obs),1)))
            action = model.predict(prev_obs.reshape(-1,len(prev_obs), 1))
            action = action.tolist()[0]

        choices.append(action)
                
        new_observation, reward, done, info = env.step(action)
        x_position.append(new_observation[0])
        y_position.append(new_observation[1])
        angle.append(new_observation[2])
        first_leg.append(new_observation[3])
        second_leg.append(new_observation[4])
        throttle.append(new_observation[5])
        gimbal.append(new_observation[6])
        x_vel.append(new_observation[7])
        y_vel.append(new_observation[8])
        angle_vel.append(new_observation[9])

        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score+=reward
        if done: break

    scores.append(score)

print("x_position min" + str(min(x_position)) + " | max: " + str(max(x_position)))
print("y_position min" + str(min(y_position)) + " | max: " + str(max(y_position)))
print("angle min" + str(min(angle)) + " | max: " + str(max(angle)))
print("first_leg min" + str(min(first_leg)) + " | max: " + str(max(first_leg)))
print("second_leg min" + str(min(second_leg)) + " | max: " + str(max(second_leg)))
print("throttle min" + str(min(throttle)) + " | max: " + str(max(throttle)))
print("gimbal min" + str(min(gimbal)) + " | max: " + str(max(gimbal)))
print("x_vel min" + str(min(x_vel)) + " | max: " + str(max(x_vel)))
print("y_vel min" + str(min(y_vel)) + " | max: " + str(max(y_vel)))
print("angle_vel min" + str(min(angle_vel)) + " | max: " + str(max(angle_vel)))

print('Average Score:',sum(scores)/len(scores))
print('Max Score:', max(scores))

#model.save('1.model')





