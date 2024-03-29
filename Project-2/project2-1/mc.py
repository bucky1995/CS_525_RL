#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import random
from collections import defaultdict

# -------------------------------------------------------------------------
'''
    Monte-Carlo
    In this problem, you will implememnt an AI player for Blackjack.
    The main goal of this problem is to get familar with Monte-Carlo algorithm.
    You could test the correctness of your code 
    by typing 'nosetests -v mc_test.py' in the terminal.
    
    You don't have to follow the comments to write your code. They are provided
    as hints in case you need. 
'''


# -------------------------------------------------------------------------

def initial_policy(observation):
    """A policy that sticks if the player score is >= 20 and his otherwise
    
    Parameters:
    -----------
    observation:
    Returns:
    --------
    action: 0 or 1
        0: STICK
        1: HIT
    """
    ############################
    # YOUR IMPLEMENTATION HERE #
    # get parameters from observation
    if observation[0] >= 20:
        action = 0
    else:
        action = 1

    # action

    ############################
    return action


def mc_prediction(policy, env, n_episodes, gamma=1.0):
    """Given policy using sampling to calculate the value function 
        by using Monte Carlo first visit algorithm.
    
    Parameters:
    -----------
    policy: function
        A function that maps an obversation to action probabilities
    env: function
        OpenAI gym environment
    n_episodes: int
        Number of episodes to sample
    gamma: float
        Gamma discount factor
    Returns:
    --------
    V: defaultdict(float)
        A dictionary that maps from state to value
    """
    # initialize empty dictionaries
    returns_sum = defaultdict(float)
    returns_count = defaultdict(float)
    # a nested dictionary that maps state -> value
    V = defaultdict(float)

     ############################
    # YOUR IMPLEMENTATION HERE #
    # loop each episode
    for e in range(0, n_episodes):
        # initialize the episode
        episode = []
        # generate empty episode list
        state = env.reset()  # player score, dealer score, terminate condition
        # loop until episode generation is done
        done = False
        while not done:
            # select an action
            action = policy(state)
            # return a reward and new state
            next_state, reward, done, _ = env.step(action)
            # append state, action, reward to episode
            episode.append((state, action, reward))
            # update state to new state
            state = next_state
        # loop for each step of episode, t = T-1, T-2,...,0
        for step in episode:
            state = step[0]
            # compute G
            for i, x in enumerate(episode):
                if x[0] == state:
                    first_visit = i
                    break
            G = 0
            for i, item in enumerate(episode[first_visit:]):
                G += item[2] * (gamma ** i)
            # unless state_t appears in states
            # update return_count
            returns_count[state] += 1
            # update return_sum
            returns_sum[state] += G
            # calculate average return for this state over all sampled episodes
            V[state] = returns_sum[state] / returns_count[state]
    ############################
    return V


def epsilon_greedy(Q, state, nA, epsilon=0.1):
    """Selects epsilon-greedy action for supplied state.
    
    Parameters:
    -----------
    Q: dict()
        A dictionary  that maps from state -> action-values,
        where Q[s][a] is the estimated action value corresponding to state s and action a. 
    state: int
        current state
    nA: int
        Number of actions in the environment
    epsilon: float
        The probability to select a random action, range between 0 and 1
    
    Returns:
    --------
    action: int
        action based current state
    Hints:
    ------
    With probability (1 − epsilon) choose the greedy action.
    With probability epsilon choose an action at random.
    """
    ############################
    # YOUR IMPLEMENTATION HERE #
    A = np.ones(nA, dtype=float) * epsilon / nA
    best_action = np.argmax(Q[state])
    A[best_action] += (1 - epsilon)
    action = np.random.choice(nA, 1, p=A)
    ############################
    return action


def mc_control_epsilon_greedy(env, n_episodes, gamma=1.0, epsilon=0.1):
    """Monte Carlo control with exploring starts. 
        Find an optimal epsilon-greedy policy.
    
    Parameters:
    -----------
    env: function
        OpenAI gym environment
    n_episodes: int
        Number of episodes to sample
    gamma: float
        Gamma discount factor
    epsilon: float
        The probability to select a random action, range between 0 and 1
    Returns:
    --------
    Q: dict()
        A dictionary  that maps from state -> action-values,
        where Q[s][a] is the estimated action value corresponding to state s and action a.
    Hint:
    -----
    You could consider decaying epsilon, i.e. epsilon = epsilon-(0.1/n_episodes) during each episode
    and episode must > 0.    
    """

    returns_sum = defaultdict(float)
    returns_count = defaultdict(float)
    # a nested dictionary that maps state -> (action -> action-value)
    # e.g. Q[state] = np.darrary(nA)
    Q = defaultdict(lambda: np.zeros(env.action_space.n))

    ############################
    # YOUR IMPLEMENTATION HERE #
    nA = env.action_space.n
    # define decaying epsilon
    epsilon = epsilon - (0.1 / n_episodes)
    for _ in range(n_episodes):
        # initialize the episode
        episode = []
        # generate empty episode list
        state = env.reset()
        # loop until one episode generation is done
        done = False
        while not done:
            # get an action from epsilon greedy policy
            action = epsilon_greedy(Q, state, nA, epsilon)[0]
            # return a reward and new state
            next_state, reward, done, _ = env.step(action)
            # append state, action, reward to episode
            episode.append((state, action, reward))
            # update state to new state
            state = next_state
        # loop for each step of episode, t = T-1, T-2, ...,0
        for step in episode:
            state = step[0]
            action = step[1]
            for i, item in enumerate(episode):
                if item[0] == state and item[1] == action:
                    first_visit = i
                    break
            # compute G
            G = 0
            for i, item in enumerate(episode[first_visit:]):
                G += item[2] * (gamma ** i)
            # unless the pair state_t, action_t appears in <state action> pair list
            # update return_sum
            returns_sum[(state, action)] += G
            # update return_count
            returns_count[(state, action)] += 1.0
            # calculate average return for this state over all sampled episodes
            Q[state][action] = returns_sum[(state, action)] / returns_count[(state, action)]

    return Q
