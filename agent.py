import tools
import pickle
import arcade
import random

class Agent(arcade.AnimatedTimeBasedSprite):
    JUMP_PIXELS = 13
    INITIAL_Y_POSITION = 256

    def __init__(self, center_x, center_y, alpha=1, gamma=0.3):
        super().__init__()
        self.qtable = {}
        self.center_x = center_x
        self.center_y = center_y
        self.texture = arcade.load_texture(tools.BIRD)
        self.__alpha = alpha
        self.gamma = gamma
        self.__history = []
        self.dead = False
        self.jumped = False
        self.reward = 0
        self.reset(True)

    def set_reward(self, reward):
        self.reward = reward

    def jump(self):

        self.center_y += self.JUMP_PIXELS
        self.jumped = True

    def die(self):
        self.dead = True

    def reset(self, store_history=True):
        if store_history:
            self.__history.append(self.reward)
        self.reward = 0

    def best_action(self):
        q = self.qtable[(self.center_x, int(self.center_y))]
        return max(q, key=q.get)

    def step(self):
        self.best_action()


    @property
    def score(self):
        return self.reward

    @property
    def history(self):
        return self.__history

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.qtable, self.__history = pickle.load(file)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.qtable, self.__history), file)

    def __repr__(self):
        res = f'Agent {agent.state}\n'
        res += str(self.qtable)
        return res
