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

        self.observation_space = spaces.Box(low=-1, high=20, shape=(22,))

        self.game = game

    def getActionByIndex(self, index):
        actions = ["playCard 1", "playCard 2", "playCard 3", "envido", "truco", "accept", "decline", "fold"]
        return actions[index]


    def step(self, action):

        # Get the action that the NN says we should take
        action = self.getActionByIndex(action)
        splitAction = action.split(" ")
        currentState = self.game.getState()

        # If action is not legal, episode is Done, and Reward is very Low
        legalActions = self.game.getLegalActions(self.player, currentState)
        if splitAction[0] not in legalActions:
            observation = np.array(currentState.getObservation(self.player))
            return observation, -9999, True, {}

        if splitAction[0] == "playCard":
            playerHand = currentState.hands[self.player]
            index = int(splitAction[1]) - 1
            # If the action is legal, but the card is already played, episode is Done, and Reward is very Low
            if index >= len(playerHand):
                observation = np.array(currentState.getObservation(self.player))
                return observation, -9999, True, {}

            card = playerHand[index]
        else:
            card = None

        # Play the action from the NN
        nextState = self.game.playAction(self.player, currentState, splitAction[0], card)
        observation = np.array(nextState.getObservation(self.player))

        # If the action ends the game, episode is Done, and Reward is the subtraction of the scores
        if nextState.getWinner() is not None:
            # opponent = self.game.getOpponent(self.player)
            reward = self.game.evaluateState(nextState, self.player)
            # reward = nextState.getPlayerScore(self.player) - nextState.getPlayerScore(opponent)
            return observation, reward, True, {}

        # Here it get's trick because a player might have to play twice:

        # If the action doesn't end the game, and it's our turn again, return with reward 0
        nextPlayer = nextState.playerTurn
        if nextPlayer == self.player:
            reward = self.game.evaluateState(nextState, self.player)
            return observation, reward, False, {}
        else:
            # If it's the other player turn, make it play (Random agent)
            nextNextState = nextPlayer.play(nextState)
            observation = np.array(nextNextState.getObservation(self.player))

            # If the action ends the game, episode is Done, and Reward is the subtraction of the scores
            if nextNextState.getWinner() is not None:
                # opponent = self.game.getOpponent(self.player)
                reward = self.game.evaluateState(nextNextState, self.player)
                # reward = nextState.getPlayerScore(self.player) - nextState.getPlayerScore(opponent)
                return observation, reward, True, {}
            else:
                # If the action doesn't end the game, and it's our turn, return with reward 0
                nextNextPlayer = nextNextState.playerTurn
                if nextNextPlayer == self.player:
                    reward = self.game.evaluateState(nextNextState, self.player)
                    return observation, reward, False, {}
                else:
                    # If it's the other player turn again, make it play (Random agent)
                    nextNextNextState = nextPlayer.play(nextNextState)
                    observation = np.array(nextNextNextState.getObservation(self.player))
                    reward = self.game.evaluateState(nextNextNextState, self.player)
                    if nextNextNextState.getWinner() is not None:
                        # opponent = self.game.getOpponent(self.player)
                        # reward = nextNextNextState.getPlayerScore(self.player) - nextNextNextState.getPlayerScore(opponent)
                        return observation, reward, True, {}
                    else:
                        return observation, reward, False, {}

    def reset(self):
        self.game.reset()
        currentState = self.game.getState()
        observation = np.array(currentState.getObservation(self.player))
        return observation
