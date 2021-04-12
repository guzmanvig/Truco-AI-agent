import math


class AlphaBetaPlayer:

    def __init__(self, name, game, depth):
        self.name = name
        self.game = game
        self.depth = depth

    def play(self, state):

        best_value, best_action = self.alpha_beta(0, state, -math.inf, math.inf)
        action = best_action[0]
        card = best_action[1]
        cardString = "" if card is None else str(card)

        print("\n" + self.name + " played " + action + " " + cardString)

        nextState = self.game.playAction(self, state, action, card)

        return nextState        


    def alpha_beta(self, current_depth, state, alpha, beta):
        if current_depth == self.depth or state.getWinner() is not None:
            return self.game.evaluateState(state, self), None
        if state.playerTurn == self:
            best_value = -math.inf
            best_action = None
            actions = self.game.getLegalActions(self, state)
            for action in actions:
                card = None
                if action == 'playCard':
                    for cardInHand in state.getPlayerHand(self):
                        nextState = self.game.playAction(self, state, action, cardInHand)
                        temp_value, temp_action = self.alpha_beta(current_depth + 1, nextState, alpha, beta)
                        if temp_value > best_value:
                            best_value = temp_value
                            best_action = action, cardInHand
                        if best_value > beta:
                            return best_value, best_action
                        alpha = max(alpha, best_value)
                else:
                    nextState = self.game.playAction(self, state, action, card)
                    temp_value, temp_action = self.alpha_beta(current_depth + 1, nextState, alpha, beta)
                    if temp_value > best_value:
                        best_value = temp_value
                        best_action = action, card
                    if best_value > beta:
                        return best_value, best_action
                    alpha = max(alpha, best_value)

            return best_value, best_action
        else:
            best_value = math.inf
            actions = self.game.getLegalActions(state.playerTurn, state)
            for action in actions:
                card = None
                if action == 'playCard':
                    for cardInHand in self.getPossibleMinCards(state):
                        nextState = self.game.playAction(state.playerTurn, state, action, cardInHand)
                        temp_value, temp_action = self.alpha_beta(current_depth + 1, nextState, alpha, beta)
                        if temp_value < best_value:
                            best_value = temp_value
                        if best_value < alpha:
                            return best_value, None
                        beta = min(beta, best_value)
                else:
                    nextState = self.game.playAction(state.playerTurn, state, action, card)
                    temp_value, temp_action = self.alpha_beta(current_depth + 1, nextState, alpha, beta)
                    if temp_value < best_value:
                        best_value = temp_value
                    if best_value < alpha:
                        return best_value, None
                    beta = min(beta, best_value)

            return best_value, None


    def getPossibleMinCards(self, state):
        possibleCards = []
        deck = self.game.getDeck()
        agentHand = state.getPlayerHand(self)
        minCardsPlayed = state.getPlayedCardsByPlayer(state.playerTurn)
        maxCardsPlayed = state.getPlayedCardsByPlayer(self)

        for card in deck:
                if card not in agentHand and \
                    card not in minCardsPlayed and \
                    card not in maxCardsPlayed:

                    possibleCards.append(card)

        return possibleCards

