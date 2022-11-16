import arcade
import random
import time
import pickle
import matplotlib.pyplot as plt

import tools
import agent
import wall


class Window(arcade.Window):
    JUMP_PIXELS = 16

    def __init__(self, width, height):
        super().__init__(width,
                         height, "Sortie d'urgence")

        # self.__agent = agent
        self.__iteration = 0
        self.background = None
        self.sprites = None
        self.walls_sprites = None
        self.agent = None
        self.ground = None
        self.agent_list = None
        self.jumped = False
        self.score = None
        self.states = {}
        self.agent_qtable = {}
        self.reward_wall = -200
        self.__history = []

    def setup(self):

        self.score = 0
        self.walls_sprites = arcade.SpriteList()
        self.agent_list = arcade.SpriteList()
        self.background = arcade.load_texture(tools.BACKGROUND)
        self.ground = arcade.load_texture(tools.GROUND)

        self.sprites = dict()
        self.sprites['background'] = self.background
        self.sprites['ground'] = self.ground
        self.sprites['agent'] = self.agent
        self.agent = agent.Agent(50, self.height // 2)
        self.agent_list.append(self.agent)

        for i in range(self.width):
            for j in range(self.height):
                self.states[i, j] = (i, j)

        for state in self.states:
            self.agent.qtable[state] = {}
            for action in tools.ACTIONS:
                self.agent.qtable[state][action] = 0.0

        first_wall = wall.Wall.create_new_wall(self.sprites, self.height)
        self.walls_sprites.append(first_wall[0])
        self.walls_sprites.append(first_wall[1])


    def draw_background(self):
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.background.width, self.background.height,
                                      self.background, 0)

    def draw_ground(self):
        arcade.draw_texture_rectangle(self.width // 2, self.ground.height // 2, self.ground.width, self.ground.height,
                                      self.ground, 0)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * tools.SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.5) * tools.SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.draw_background()
        self.draw_ground()
        self.walls_sprites.draw()
        self.agent_list.draw()


    def on_update(self, delta_time):
        self.agent.step()
        if(self.agent.best_action() == 'U'):
           self.agent.jump()
        else:
            self.agent.center_y -= 1

        new_wall = None
        reward = 0


        for wall in self.walls_sprites:
            wall.step()
            if wall.right <= 0:
                wall.kill()

            elif len(self.walls_sprites) == 2 and wall.right <= random.randrange(self.width // 2, self.width // 2 + 15):
                new_wall = wall.create_new_wall(self.sprites, self.height)

        boom = arcade.check_for_collision_with_list(self.agent, self.walls_sprites)

        if boom:
            self.__iteration += 1
            reward = self.reward_wall
            maxQ = max(self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))].values())
            delta = self.agent.alpha * (reward + self.agent.gamma * maxQ -
                                        self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))][
                                            self.agent.best_action()])
            self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))]['/'] += delta
            self.agent.reset()
            print(self.score)
            self.history.append(self.score)
            self.setup()

        if new_wall:
            self.walls_sprites.append(new_wall[0])
            self.walls_sprites.append(new_wall[1])

        self.walls_sprites.update()
        #self.agent.update(delta_time)
        self.agent_list.update()

        if self.agent.center_x >= self.walls_sprites[0].center_x and not self.walls_sprites[0].agent_passed:
            self.score += 1
            self.walls_sprites[0].agent_passed = True
            self.walls_sprites[1].agent_passed = True
            #self.agent.jump()
            print(self.score)
            reward = 1

            maxQ = max(self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))].values())
            delta = self.agent.alpha * (reward + self.agent.gamma * maxQ -
                                        self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))][
                                            self.agent.best_action()])
            self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))]['U'] += delta


        #self.__state = state



        # if self.__agent.state in self.__walls:
        #     self.__agent.reset()
        #     self.__iteration += 1
        #
        # if self.__agent.state != self.__agent.environment.goal:
        #     self.__agent.step()
        # else:
        #     self.__agent.reset()
        #     self.__iteration += 1
        #     # self.__sound.play()
        #
        # self.__player.center_x, self.__player.center_y \
        #     = self.state_to_xy(self.__agent.state)

    @property
    def history(self):
        return self.__history

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.qtable, self.__history = pickle.load(file)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.qtable, self.__history), file)
