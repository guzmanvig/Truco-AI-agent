
from human_player import HumanPlayer
from truco import Game
from minimax_player import MinimaxPlayer
from alphabeta_player import AlphaBetaPlayer



def main():

    game = Game()

    player1 = HumanPlayer("Guzman", game)
    # player2 = HumanPlayer("Agustin", game)
    # player2 = MinimaxPlayer("MiniMax", game, 6)
    player2 = AlphaBetaPlayer("AlphaBeta", game, 6)



    game.setPlayers(player1, player2)
    game.initGameState()

    state = game.getState()
    while not state.getWinner():

        currentPlayer = state.playerTurn
        state = currentPlayer.play(state)

    game.calculateEnvidoWinner(state)

    print("\n" + state.getWinnerName() + " has won truco \n")
    print("Final scores:")
    state.printScores()



main()
