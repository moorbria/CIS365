import gym
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

LR = .5

env = gym.make('RocketLander-v0')
env.reset()
goal_steps = 750
score_requirement = 900
initial_games = 2500

def initial_population():
    # [OBS, MOVES]
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []


    # iterate through however many games we want:
    for episode in range(initial_games):
        if episode % 25 is 0 and episode != 0:
          print(str(episode/initial_games*100) + "% Complete")

        score = 0
        # moves specifically from this environment:
        game_memory = []
        # previous observation that we saw
        prev_observation = []
        # for each frame in 200
        for episode in range(goal_steps):
            #env.render()
            a = 0 #float(random.randrange(-100, 100))/100
            b = float(random.randrange(-100, 100))/100
            c = float(random.randrange(-100, 100))/100
            action = [a, b, c]

            # do it!
            observation, reward, done, info = env.step(action)

            # custom reward function
            reward = 0

            # if angle is low
            if abs(observation[2]) < .5: 
                reward += 1
            
            if abs(observation[2]) < .1: 
                reward += 2

            if abs(observation[9]) < 1:
                reward += 2

  
            # if you are in the middle of the map
            #reward += (1 - abs(observation[0]))*3 # x position

            # if you are near the bottom and your speed is low
            #if observation[1] < -1.2 and observation[8] > 2.5 and observation[8] < 3.8:
            #  reward += 3 

            
            #if observation[1] < -1.3 and abs(observation[8]
              
            # Reward for staying upright
            #reward = (.5 - abs(.5 - norm_observation[2]))*2
            
            #if observation[1] < -.5:
            #    reward += 3 - abs(.5 - norm_observation[2])

            # Reward for angular velocity (don't spin that fast)
            #if observation[9] < 35:
            #    reward += .5 - abs(.5 - norm_observation[9])

            #reward += .5 - abs((.5 - norm_observation[0]))
                       
            
            # Reward for low speed at the end and no spin
            #if observation[1] < -.5: # y position is in the last quadrant
            #    reward -= abs(observation[7]) 
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
            print(score)
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

def generation_population():
    # [OBS, MOVES]
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []
    score_requirement = 60
    prev_obs = []

    model = neural_network_model(10)
    model.load('runs/1.model')

    # iterate through however many games we want:
    for episode in range(initial_games):
        if episode % 25 is 0 and episode != 0:
          print(str(episode/initial_games*100) + "% Complete")

        score = 0
        # moves specifically from this environment:
        game_memory = []
        # previous observation that we saw
        prev_observation = []
        # for each frame in 200
        for episode in range(goal_steps):
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
                #print(action)

            observation, reward, done, info = env.step(action)

            prev_obs = observation
            game_memory.append([observation, action])
            # custom reward function
            reward = 0

            # if angle is low
            if abs(observation[2]) < .3: 
                reward += 3

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
        print(score)
        if score >= score_requirement:
            print(score)
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
    np.save('saved2.npy',training_data_save)
    
    # some stats here, to further illustrate the neural network magic!
    print('Average accepted score:',mean(accepted_scores))
    print('Median score for accepted scores:',median(accepted_scores))
    print("Count Accepted", len(accepted_scores))
    
    return training_data

def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    #network = fully_connected(network, 128, activation='softmax')
    #network = dropout(network, 0.8)
    
    #network = fully_connected(network, 256, activation='softplus')
    #network = dropout(network, 0.8)

    #network = fully_connected(network, 30, activation='softmax')
    #network = dropout(network, 0.8)

    #network = fully_connected(network, 256, activation='relu')
    #network = dropout(network, 0.8)

    #network = fully_connected(network, 128, activation='tanh')
    #network = dropout(network, 0.8)

    network = fully_connected(network, 3, activation='linear')
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

# For Initial Runs
training_data = initial_population()
model = train_model(training_data)

# New Model with previous training data
#training_data = np.load('saved.npy')
#model = train_model(training_data)

# Trained Data New Model
#training_data = generation_population()
#training_data = np.load('saved2.npy')
#model = train_model(training_data)

# Rerun with saved model
#model = neural_network_model(10)
#model.load('runs/1.model')

scores = []
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
            #print(action)

                
        new_observation, reward, done, info = env.step(action)

        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score+=reward
        if done: break

    scores.append(score)


print('Average Score:',sum(scores)/len(scores))
print('Max Score:', max(scores))

model.save('2.model')

