import gym
import numpy as np

env = gym.make("FrozenLake-v1")
n_observations = env.observation_space.n
n_actions = env.action_space.n

#Initialize the Q-table to 0
Q_table = np.zeros((n_observations,n_actions))
print(Q_table)

