
from random_player import RandomPlayer
from truco import Game
from alphabeta_player import AlphaBetaPlayer
from QLearning_player import QLearningPlayer




def evaluate():
    reflexScore = 0
    alphaBetaScore = 0
    # player1Name = "Random"
    player1Name = "Reflex"
    #player1Name = "AlphaBeta"
    #player2Name = "QLearning"
    player2Name = "AlphaBeta"

    for i in range(200):

        game = Game()

        # player1 = RandomPlayer(player1Name, game)
        player1 = AlphaBetaPlayer(player1Name, game, 1)

        player2 = AlphaBetaPlayer(player2Name, game, 6)
        #player2 = QLearningPlayer(player2Name, game)


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

    print("\n\nRESULTS")
    print("----------------------------")
    print(player1Name + " final score: " + str(reflexScore))
    print(player2Name + " final score: " + str(alphaBetaScore))
    print("----------------------------")





evaluate()
