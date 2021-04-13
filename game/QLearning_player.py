import random

import numpy as np
from stable_baselines3 import DQN


class QLearningPlayer:

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.model = DQN.load(path="QLearning_model.zip")

    def play(self, state):
        observation = np.array(state.getObservation(self))
        action_index, _states = self.model.predict(observation)

        action = self.getActionByIndex(action_index)
        splitAction = action.split(" ")

        playAction = splitAction[0]
        playCard = None

        legalActions = self.game.getLegalActions(self, state)
        hand = state.getPlayerHand(self)

        if playAction not in legalActions:
            playAction = random.choice(legalActions)
            if playAction == 'playCard':
                playCard = random.choice(hand)

        elif playAction == "playCard":
            index = int(splitAction[1]) - 1
            if index >= len(hand):
                playCard = random.choice(hand)
            else:
                playCard = hand[index]
        else:
            playCard = None

        cardString = "" if playCard is None else str(playCard)
        print("\n" + self.name + " played " + playAction + " " + cardString)

        nextState = self.game.playAction(self, state, playAction, playCard)
        return nextState

    def getActionByIndex(self, index):
        actions = ["playCard 1", "playCard 2", "playCard 3", "envido", "truco", "accept", "decline", "fold"]
        return actions[index]
