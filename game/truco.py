import random
from itertools import combinations
from copy import copy, deepcopy
from collections import defaultdict


class CardSuit:
    BATON = "Baton"
    COIN = "Coin"
    CUP = "Cup"
    SWORD = "Sword"


class ActionScore:
    TRUCO_WON = 4
    TRUCO_DECLINED = 1
    PLAYER_FOLDED = 1
    ENVIDO_WON = 2
    ENVIDO_DECLINED = 1

class Card:

    def __init__(self, number, suit, rank):
        self.number = number
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{}-{}: {}".format(self.number, self.suit, self.rank)


class Actions:
    PLAY_CARD = "playCard"
    ENVIDO = "envido"
    TRUCO = "truco"
    ACCEPT = "accept"
    DECLINE = "decline"
    FOLD = 'fold'


class GameState:
    def __init__(self, firstPlayer, secondPlayer, firstPlayerHand, secondPlayerHand):
        self.round = 1
        self.playerTurn = firstPlayer
        self.trucoCalled = False
        self.trucoAnswered = False
        self.envidoCalled = False
        self.envidoAnswered = False
        self.history = [[], [], []]
        self.winner = None

        self.playersScore = {
            firstPlayer: 0,
            secondPlayer: 0
        }

        self.hands = {
            firstPlayer: firstPlayerHand,
            secondPlayer: secondPlayerHand
        }

    def removeCardFromHand(self, player, card):
        playerHand = copy(self.hands[player])
        playerHand.remove(card)
        self.hands[player] = playerHand

    def getPlayerHand(self, player):
        return copy(self.hands[player])

    def getPlayerScore(self, player):
        return self.playersScore[player]
    
    def incrementPlayerScore(self, player, score):
        self.playersScore[player] += score


class Game:

    def __init__(self):
        # Create deck
        self.deck = None
        self.generateDeck()
        self.shuffleDeck()

        # Deal cards to player
        self.player1 = None
        self.player2 = None

    def getState(self):
        return self.state

    def setPlayers(self, player1, player2):

        self.player1 = player1
        self.player2 = player2

    def initGameState(self):
        handPlayer1 = self.getHand()
        handPlayer2 = self.getHand()

        self.state = GameState(self.player1, self.player2,
                               handPlayer1, handPlayer2)

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
        # Calculate points of envido.
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
        if not state.envidoCalled and state.round == 1:
            if not state.trucoCalled:
                return [Actions.PLAY_CARD, Actions.ENVIDO, Actions.FOLD, Actions.TRUCO]
            return [Actions.PLAY_CARD, Actions.ENVIDO, Actions.FOLD]
        if not state.trucoCalled:
            return [Actions.PLAY_CARD, Actions.TRUCO, Actions.FOLD]

        return [Actions.PLAY_CARD, Actions.FOLD]
    
    def calculateEnvidoWinner(self, state):
        
        player1 = self.player1
        player2 = self.player2
        player1Hand = state.hands[player1]
        player2Hand = state.hands[player2]
        player1EnvidoScore = self.getEnvidoScore(player1Hand)
        player2EnvidoScore = self.getEnvidoScore(player2Hand)

        if(player1EnvidoScore >= player2EnvidoScore):
            state.incrementPlayerScore(player1, ActionScore.ENVIDO_WON)
        else:
            state.incrementPlayerScore(player2, ActionScore.ENVIDO_WON)


    def playAction(self, player, state, action, card=None):
        if player != state.playerTurn:
            raise ValueError('Wrong player')
        legalActions = self.getLegalActions(player, state)
        if action not in legalActions:
            raise ValueError('Invalid action')

        nextState = copy(state)

        if player == self.player1:
            otherPlayer = self.player2
        else:
            otherPlayer = self.player1

        if action == Actions.TRUCO:
            nextState.trucoCalled = True
            nextState.playerTurn = otherPlayer

        if action == Actions.ENVIDO:
            nextState.envidoCalled = True
            nextState.playerTurn = otherPlayer

        if action == Actions.ACCEPT and state.trucoCalled:
            nextState.trucoAnswered = True
            nextState.playerTurn = otherPlayer

        if action == Actions.DECLINE and state.trucoCalled:
            nextState.winner = otherPlayer
            nextState.playerTurn = otherPlayer

        if action == Actions.ACCEPT and state.envidoCalled:
            nextState.envidoAnswered = True
            nextState.playerTurn = otherPlayer

            self.calculateEnvidoWinner(state)
            
            
        if action == Actions.DECLINE and state.envidoCalled:
            nextState.envidoAnswered = True
            nextState.playerTurn = otherPlayer

        if action == Actions.FOLD:
            nextState.winner = otherPlayer
            nextState.playerTurn = otherPlayer

        if action == Actions.PLAY_CARD:

            nextState.removeCardFromHand(player, card)

            index = nextState.round - 1
            gameRound = nextState.history[index]
            gameRound.append((card, player))
            nextState.playerTurn = otherPlayer
            if len(gameRound) == 2:
                round_winner = self.getRoundWinner(gameRound)
                gameRound.append(round_winner)
                if round_winner != otherPlayer:
                    nextState.playerTurn = player
                nextState.round += 1
                winner = self.getWinner(nextState.history)
                if winner is not None:
                    nextState.winner = winner
        return nextState

    def getRoundWinner(self, gameRound):
        
        firstPlay = gameRound[0]
        secondPlay = gameRound[1]

        firstCard = firstPlay[0]  # (card , player)
        firstCardPlayer = firstPlay[1]
        secondCard = secondPlay[0]
        secondCardPlayer = secondPlay[1]

        if firstCard.rank > secondCard.rank:
            return secondCardPlayer
        elif firstCard.rank < secondCard.rank:
            return firstCardPlayer
        else:  # Draw
            return None

    def getWinner(self, history):

        player1 = self.player1
        player2 = self.player2

        roundsWonPerPlayer = {
            player1: 0,
            player2: 0    
        }

        lastRound = 1
        for entry in history:
            # [(card, player) (card, player) winner]
            if len(entry) == 3:

                lastRound += 1

                roundWinner = entry[2]

                if(roundWinner != None):
                    roundsWonPerPlayer[roundWinner] += 1
                else:
                    roundsWonPerPlayer[player1] += 1
                    roundsWonPerPlayer[player2] += 1

        if (lastRound == 2):

            if(roundsWonPerPlayer[player1] > roundsWonPerPlayer[player2]):
                return player1
            elif(roundsWonPerPlayer[player1] < roundsWonPerPlayer[player2]):
                return player2

        elif (lastRound == 3):
            
            if(roundsWonPerPlayer[player1] > roundsWonPerPlayer[player2]):
                return player1
            elif(roundsWonPerPlayer[player1] < roundsWonPerPlayer[player2]):
                return player2
            else: 
                return player1
        
        return None


    def getHand(self):
        hand = []
        for i in range(3):
            hand.append(self.deck.pop(0))

        return hand

    def printDeck(self):
        for card in self.deck:
            print(card)
