import random
from itertools import combinations

class CardSuit:
    BATON = "Baton"
    COIN = "Coin"
    CUP = "Cup"
    SWORD = "Sword"


class Card:

    number = None
    suit = None
    rank = None

    def __init__(self, number, suit, rank):
        self.number = number
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{}-{}: {}".format(self.number, self.suit, self.rank)



class Game:

    deck = None

    def generateDeck(self):
        # SWORDS
        deck = list()

        deck.append(Card(1, CardSuit.SWORD, 1))
        deck.append(Card(2, CardSuit.SWORD, 6))
        deck.append(Card(3, CardSuit.SWORD, 5))
        deck.append(Card(4, CardSuit.SWORD, 14))
        deck.append(Card(5, CardSuit.SWORD, 13))
        deck.append(Card(6, CardSuit.SWORD, 12))
        deck.append(Card(7, CardSuit.SWORD, 3))
        deck.append(Card(10, CardSuit.SWORD, 10))
        deck.append(Card(11, CardSuit.SWORD, 9))
        deck.append(Card(12, CardSuit.SWORD, 8))

        # CUPS
        deck.append(Card(1, CardSuit.CUP, 7))
        deck.append(Card(2, CardSuit.CUP, 6))
        deck.append(Card(3, CardSuit.CUP, 5))
        deck.append(Card(4, CardSuit.CUP, 14))
        deck.append(Card(5, CardSuit.CUP, 13))
        deck.append(Card(6, CardSuit.CUP, 12))
        deck.append(Card(7, CardSuit.CUP, 11))
        deck.append(Card(10, CardSuit.CUP, 10))
        deck.append(Card(11, CardSuit.CUP, 9))
        deck.append(Card(12, CardSuit.CUP, 8))

        # BATONS
        deck.append(Card(1, CardSuit.BATON, 2))
        deck.append(Card(2, CardSuit.BATON, 6))
        deck.append(Card(3, CardSuit.BATON, 5))
        deck.append(Card(4, CardSuit.BATON, 14))
        deck.append(Card(5, CardSuit.BATON, 13))
        deck.append(Card(6, CardSuit.BATON, 12))
        deck.append(Card(7, CardSuit.BATON, 11))
        deck.append(Card(10, CardSuit.BATON, 10))
        deck.append(Card(11, CardSuit.BATON, 9))
        deck.append(Card(12, CardSuit.BATON, 8))

        # COINS
        deck.append(Card(1, CardSuit.COIN, 7))
        deck.append(Card(2, CardSuit.COIN, 6))
        deck.append(Card(3, CardSuit.COIN, 5))
        deck.append(Card(4, CardSuit.COIN, 14))
        deck.append(Card(5, CardSuit.COIN, 13))
        deck.append(Card(6, CardSuit.COIN, 12))
        deck.append(Card(7, CardSuit.COIN, 4))
        deck.append(Card(10, CardSuit.COIN, 10))
        deck.append(Card(11, CardSuit.COIN, 9))
        deck.append(Card(12, CardSuit.COIN, 8))

        self.deck = deck
    
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
            if (firstCard.suit == secondCard.suit):
                combinationScore = 20 + firstCardScore + secondCardScore
            else:
                combinationScore = max([firstCardScore, secondCardScore])

            envidoScore = max([combinationScore, envidoScore])
        
        return envidoScore


        
    def dealCards(self):
        # Deal cards.
        print("NOT IMPLEMENTED")

    def printDeck(self):
        for card in self.deck:
            print(card)

def main():

    game = Game()

    game.generateDeck()
    game.shuffleDeck()
    game.printDeck()


main()
