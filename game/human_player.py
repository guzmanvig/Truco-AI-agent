class HumanPlayer:

    def __init__(self, name, game):
        self.name = name
        self.game = game

    def play(self, state):

        playerHand = state.hands[self]
        game = self.game

        print("Your cards are: " + self.printHand(playerHand))
        print(self.name + " type any of the following: ")
        
        action = input(str(game.getLegalActions(self, state)) + "\n")

        splitAction = action.split(" ")

        if splitAction[0] == "playCard":
            card = self.getCardFromHand(splitAction[1], playerHand)
        else:
            card = None

        nextState = game.playAction(
            self, state, splitAction[0], card)

        return nextState        

    def getCardFromHand(self, cardString, hand):
        for card in hand:
            if cardString in str(card):
                return card
        raise ValueError("You don't have that card!")

    def printHand(self, hand):
        string = "||"
        for card in hand:
            string += " " + str(card) + " ||"
        return string
