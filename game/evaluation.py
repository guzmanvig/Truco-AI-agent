
from random_player import RandomPlayer
from truco import Game
from alphabeta_player import AlphaBetaPlayer



def evaluate():
    reflexScore = 0
    alphaBetaScore = 0

    for i in range(50):

        game = Game()

        player1 = RandomPlayer("Random", game)
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

        reflexScore += state.getPlayerScore(player1)
        alphaBetaScore += state.getPlayerScore(player2)

    print("Reflex final score: " + str(reflexScore))
    print("AlphaBeta final score: " + str(alphaBetaScore))





evaluate()
