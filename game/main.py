from game.human_player import HumanPlayer
from game.truco import Game


def main():

    player1 = HumanPlayer("Guzman")
    player2 = HumanPlayer("Agustin")
    game = Game(player1, player2)
    # game.printDeck()
    player1.printHand()
    player2.printHand()


main()