class HumanPlayer:

    def __init__(self, name):
        self.name = name
        self.hand = None
        self.score = 0

    def getCardFromHand(self, cardString):
        # 12-Coin
        for card in self.hand:
            if cardString in str(card):
                self.hand.remove(card)
                return card
        raise ValueError("You don't have that card!")

    def printHand(self):
        string = "||"
        for card in self.hand:
            string += " " + str(card) + " ||"
        return string