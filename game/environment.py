import math

import numpy as np
import gym
from gym import spaces

class TrucoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, game, player):

        self.player = player

        # [ play_card1, play_card2, play_card3, envido, truco, accept, decline, fold ]
        self.action_space = spaces.Discrete(8)

        # [
        # card1, ranking1, card2, ranking2, card3, ranking3, ...
        # envido_played, truco_played, envido_answered, truco_ answered,...
        # round1card1, round1ranking1, round1card2, round1ranking2,...
        # round2card1, round2ranking1, round2card2, round2ranking2,...
        # round3card1, round3ranking1, round3card2, round3ranking2
        # ]
        #self.observation_space = spaces.Box(low=0, high=np.inf, shape=(22,))
        self.observation_space = spaces.Box(low=-1, high=20, shape=(22,))

        self.game = game

    def getActionByIndex(self, index):
        actions = ["playCard 1", "playCard 2", "playCard 3", "envido", "truco", "accept", "decline", "fold"]
        return actions[index]


    def step(self, action):

        action = self.getActionByIndex(action)
        splitAction = action.split(" ")
        currentState = self.game.getState()
        legalActions = self.game.getLegalActions(self.player, currentState)
        if splitAction[0] not in legalActions:
            observation = np.array(currentState.getObservation(self.player))
            return observation, -9999, True, {}

        if splitAction[0] == "playCard":
            playerHand = currentState.hands[self.player]
            index = int(splitAction[1]) - 1
            if index >= len(playerHand):
                observation = np.array(currentState.getObservation(self.player))
                return observation, -9999, True, {}
            card = playerHand[index]
        else:
            card = None


        nextState = self.game.playAction(self.player, currentState, splitAction[0], card)
        nextPlayer = nextState.playerTurn
        nextNextState = nextPlayer.play(nextState)

        done = nextNextState.getWinner() is not None
        reward = self.game.evaluateState(nextNextState, self.player)
        observation = np.array(nextNextState.getObservation(self.player))

        return observation, reward, done, {}




    def reset(self):
        self.game.reset()
        currentState = self.game.getState()
        observation = np.array(currentState.getObservation(self.player))
        return observation
