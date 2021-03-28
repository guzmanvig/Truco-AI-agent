
from human_player import HumanPlayer
from truco import Game


def main():

    game = Game()


    player1 = HumanPlayer("Guzman", game)
    player2 = HumanPlayer("Agustin", game)


    game.setPlayers(player1, player2)

    game.initGameState()


    state = game.getState()

    while state.winner is None:
        currentPlayer = state.playerTurn
        state = currentPlayer.play(state)
        

    print("\n" + state.winner.name + " has won!!")


main()