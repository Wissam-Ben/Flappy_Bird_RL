import tools
import arcade
import random

class Environment:
    def __init__(self, str_map):
        self.__states = {}
        self.__reward_wall = -2 * self.__reward_goal
        self.__reward_ground = -3 * self.__reward_goal
        self.pipeVelX = -4
        self.playery = 3
        self.playerx = 3
        self.playerVelY = 0  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerFlapAcc = -9  # players speed on flapping
        self.playerFlapped = False  # True when player flaps

    def do(self, state, action):
        self.agent.step()
        if (self.agent.best_action() == 'U'):
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
        # self.agent.update(delta_time)
        self.agent_list.update()

        if self.agent.center_x >= self.walls_sprites[0].center_x and not self.walls_sprites[0].agent_passed:
            self.score += 1
            self.walls_sprites[0].agent_passed = True
            self.walls_sprites[1].agent_passed = True
            # self.agent.jump()
            print(self.score)
            reward = 1

            maxQ = max(self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))].values())
            delta = self.agent.alpha * (reward + self.agent.gamma * maxQ -
                                        self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))][
                                            self.agent.best_action()])
            self.agent.qtable[(self.agent.center_x, int(self.agent.center_y))]['U'] += delta



    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

