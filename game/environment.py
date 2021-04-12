import math

import numpy as np
import gym
from gym import spaces

class TrucoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, game):
        # [ play_card1, play_card2, play_card3, envido, truco, accept, decline, fold ]
        self.action_space = spaces.Discrete(8)

        # [
        # card1, ranking1, card2, ranking2, card3, ranking3, ...
        # envido_played, truco_played, ...
        # round1card1, round1ranking1, round1card2, round1ranking2,...
        # round2card1, round2ranking1, round2card2, round2ranking2,...
        # round3card1, round3ranking1, round3card2, round3ranking2
        # ]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(20,))

        self.game = game

    def getActionByIndex(self, index):
        actions = ["playCard 1", "playCard 2", "playCard 3", "envido", "truco", "accept", "decline", "fold"]
        return actions[index]


    def step(self, action):

        action = self.getActionByIndex(action)
        splitAction = action.split(" ")
        currentState = self.game.getState()
        legalActions = self.game.getLegalActions(self, currentState)
        if splitAction[0] not in legalActions:
            return None, -math.inf, True, None

        if splitAction[0] == "playCard":
            playerHand = currentState.state.hands[self]
            index = int(splitAction[1])
            if index > len(playerHand):
                return None, -math.inf, True, None
            card = playerHand[index]
        else:
            card = None


        nextState = self.game.playAction(self, currentState, splitAction[0], card)
        nextPlayer = nextState.playerTurn
        nextNextState = nextPlayer.play(nextState)
        done = nextNextState.getWinner() is not None

        #TODO: create getObservation, getReward()
        return nextNextState.getObservation(), nextNextState.getReward(), done, None




    def reset(self):
        #TODO: create reset
        self.game.reset()
