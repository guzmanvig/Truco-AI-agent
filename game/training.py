from stable_baselines3 import A2C, DQN
from stable_baselines3.common.env_checker import check_env

from game.QLearning_player import QLearningPlayer
from game.alphabeta_player import AlphaBetaPlayer
from game.environment import TrucoEnv
from game.random_player import RandomPlayer
from game.truco import Game

game = Game()

player1 = QLearningPlayer("QLearning", game)
player2 = RandomPlayer("Random", game)

game.setPlayers(player1, player2)
game.initGameState()

env = TrucoEnv(game, player1)
# It will check your custom environment and output additional warnings if needed
# check_env(env)

# model = A2C('MlpPolicy', env).learn(total_timesteps=1000)
model = DQN("MlpPolicy", env, learning_rate=0.001, batch_size=20)
model.learn(total_timesteps=1000000)
model.save("QLearning_model")


