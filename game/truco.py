import random
from itertools import combinations
from copy import copy


class CardSuit:
    BATON = "Baton"
    COIN = "Coin"
    CUP = "Cup"
    SWORD = "Sword"


class Card:

    def __init__(self, number, suit, rank):
        self.number = number
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{}-{}: {}".format(self.number, self.suit, self.rank)

class Actions:
    PLAY_CARD = "play"
    ENVIDO = "envido"
    TRUCO = "truco"
    ACCEPT = "accept"
    DECLINE = "decline"
    FOLD = 'fold'

class GameState:
    def __init__(self, firstPlayer):
        self.round = 0
        self.playerTurn = firstPlayer
        self.score = dict()
        self.trucoCalled = False
        self.trucoAnswered = False
        self.envidoCalled = False
        self.envidoAnswered = False
        self.cardPlayedPerRound = []
        self.isTerminal = False




class Game:
    def __init__(self, player1, player2):
        # Create deck
        self.deck = None
        self.generateDeck()
        self.shuffleDeck()

        # Deal cards to player
        self.player1 = player1
        self.player2 = player2
        self.dealCards(player1)
        self.dealCards(player2)

        self.state = GameState(player1)



    def generateDeck(self):
        # SWORDS
        self.deck = list()

        self.deck.append(Card(1, CardSuit.SWORD, 1))
        self.deck.append(Card(2, CardSuit.SWORD, 6))
        self.deck.append(Card(3, CardSuit.SWORD, 5))
        self.deck.append(Card(4, CardSuit.SWORD, 14))
        self.deck.append(Card(5, CardSuit.SWORD, 13))
        self.deck.append(Card(6, CardSuit.SWORD, 12))
        self.deck.append(Card(7, CardSuit.SWORD, 3))
        self.deck.append(Card(10, CardSuit.SWORD, 10))
        self.deck.append(Card(11, CardSuit.SWORD, 9))
        self.deck.append(Card(12, CardSuit.SWORD, 8))

        # CUPS
        self.deck.append(Card(1, CardSuit.CUP, 7))
        self.deck.append(Card(2, CardSuit.CUP, 6))
        self.deck.append(Card(3, CardSuit.CUP, 5))
        self.deck.append(Card(4, CardSuit.CUP, 14))
        self.deck.append(Card(5, CardSuit.CUP, 13))
        self.deck.append(Card(6, CardSuit.CUP, 12))
        self.deck.append(Card(7, CardSuit.CUP, 11))
        self.deck.append(Card(10, CardSuit.CUP, 10))
        self.deck.append(Card(11, CardSuit.CUP, 9))
        self.deck.append(Card(12, CardSuit.CUP, 8))

        # BATONS
        self.deck.append(Card(1, CardSuit.BATON, 2))
        self.deck.append(Card(2, CardSuit.BATON, 6))
        self.deck.append(Card(3, CardSuit.BATON, 5))
        self.deck.append(Card(4, CardSuit.BATON, 14))
        self.deck.append(Card(5, CardSuit.BATON, 13))
        self.deck.append(Card(6, CardSuit.BATON, 12))
        self.deck.append(Card(7, CardSuit.BATON, 11))
        self.deck.append(Card(10, CardSuit.BATON, 10))
        self.deck.append(Card(11, CardSuit.BATON, 9))
        self.deck.append(Card(12, CardSuit.BATON, 8))

        # COINS
        self.deck.append(Card(1, CardSuit.COIN, 7))
        self.deck.append(Card(2, CardSuit.COIN, 6))
        self.deck.append(Card(3, CardSuit.COIN, 5))
        self.deck.append(Card(4, CardSuit.COIN, 14))
        self.deck.append(Card(5, CardSuit.COIN, 13))
        self.deck.append(Card(6, CardSuit.COIN, 12))
        self.deck.append(Card(7, CardSuit.COIN, 4))
        self.deck.append(Card(10, CardSuit.COIN, 10))
        self.deck.append(Card(11, CardSuit.COIN, 9))
        self.deck.append(Card(12, CardSuit.COIN, 8))

    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    def getEnvidoScore(self, hand):
        #Calculate points of envido.
        pairCombinations = list(combinations(hand, 2))
        
        envidoScore = 0

        # We compute the score for each possible pair combination of the 3 hand cards. And we return the maximum one.
        for pair in pairCombinations:
            firstCard = pair[0]
            secondCard = pair[1]

            # If card number is greater or equal than 10, then its score is 0 for the envido.
            firstCardScore = firstCard.number if firstCard.number < 10 else 0
            secondCardScore = secondCard.number if secondCard.number < 10 else 0

            combinationScore = None
            
            # If both cards have the same suit, then we add 20 to their sum. Otherwise, we get the largest one.
            if firstCard.suit == secondCard.suit:
                combinationScore = 20 + firstCardScore + secondCardScore
            else:
                combinationScore = max([firstCardScore, secondCardScore])

            envidoScore = max([combinationScore, envidoScore])
        
        return envidoScore

    def getLegalActions(self, player, state):

        if player != state.playerTurn:
            raise ValueError('Wrong player')

        if state.trucoCalled and not state.trucoAnswered:
            return [Actions.ACCEPT, Actions.DECLINE]
        if state.envidoCalled and not state.envidoAnswered:
            return [Actions.ACCEPT, Actions.DECLINE]
        if not state.envidoCalled and state.round == 0:
            return [Actions.PLAY_CARD, Actions.ENVIDO, Actions.FOLD]
        if not state.trucoCalled:
            return [Actions.PLAY_CARD, Actions.TRUCO, Actions.FOLD]

        return [Actions.PLAY_CARD, Actions.FOLD]


    def playAction(self, player, state, action, card = None):
        if player != state.playerTurn:
            raise ValueError('Wrong player')
        legalActions = self.getLegalActions(player, state)
        if action not in legalActions:
            raise ValueError('Invalid action')

        nextState = copy(state)
        # TODO: if  last round was bla bla
        if state.playerTurn == self.player1:
            nextState.playerTurn = self.player2
        else:
            nextState.playerTurn = self.player1

        if action == Actions.TRUCO:
            nextState.trucoCalled = True
        if action == Actions.ENVIDO:
            nextState.envidoCalled = True
        if action == Actions.ACCEPT and state.trucoCalled:
            nextState.trucoAnswered = True
        if action == Actions.DECLINE and state.trucoCalled:
            nextState.isTerminal = True
        if action == Actions.ACCEPT and state.envidoCalled:
            nextState.envidoAnswered = True
        if action == Actions.DECLINE and state.envidoCalled:
            nextState.envidoAnswered = True
        if action == Actions.FOLD:
            nextState.isTerminal = True
        if action == Actions.PLAY_CARD:











    def dealCards(self, player):
        hand = []
        for i in range(3):
            hand.append(self.deck.pop(0))
        player.hand = hand

    def printDeck(self):
        for card in self.deck:
            print(card)

