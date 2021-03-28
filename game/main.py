from game.human_player import HumanPlayer
from game.truco import Game


def main():

    player1 = HumanPlayer("Guzman")
    player2 = HumanPlayer("Agustin")
    game = Game(player1, player2)

    print("Player 1 hand: \n")
    print(player1.printHand())
    print("\n Player 2 hand: \n")
    print(player2.printHand())
    print("\n GAME STARTING: \n")

    print("Your cards are: " + player1.printHand())
    print(player1.name + " type any of the following: ")
    action = input(str(game.getLegalActions(player1, game.getState())) + "\n")
    splitAction = action.split(" ")
    if splitAction[0] == "playCard":
        card = player1.getCardFromHand(splitAction[1])
    else:
        card = None
    newState = game.playAction(player1, game.getState(), splitAction[0], card)
    #print(newState.history)


    while newState.winner is None:
        currentPlayer = newState.playerTurn
        print("Your cards are: " + currentPlayer.printHand())
        print(currentPlayer.name + " type any of the following:")
        action = input(str(game.getLegalActions(currentPlayer, newState)) + "\n")
        splitAction = action.split(" ")
        if splitAction[0] == "playCard":
            card = currentPlayer.getCardFromHand(splitAction[1])
        else:
            card = None
        newState = game.playAction(currentPlayer, newState, splitAction[0], card)
        #print(newState.history)

    print("\n" + newState.winner.name + " has won!!")


main()