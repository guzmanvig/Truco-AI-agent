class HumanPlayer:

    def __init__(self, name):
        self.name = name
        self.hand = None
        self.score = 0

    def printHand(self):
        for card in self.hand:
            print(card)