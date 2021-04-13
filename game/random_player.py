import math
import random


class RandomPlayer:

    def __init__(self, name, game):
        self.name = name
        self.game = game

    def play(self, state):

        action, card = self.randomMove(state)
        cardString = "" if card is None else str(card)

        # print("\n" + self.name + " played " + action + " " + cardString)

        nextState = self.game.playAction(self, state, action, card)

        return nextState        


    def randomMove(self, state):
        
        actions = self.game.getLegalActions(self, state)
        
        randomAction = random.choice(actions)
        randomCard = None

        if randomAction == 'playCard':
            hand = state.getPlayerHand(self)
            randomCard = random.choice(hand)


        return randomAction, randomCard