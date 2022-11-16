import random

import arcade

import tools

wall = tools.PIPES[0]

class Wall(arcade.Sprite):
    def __init__(self, image, scale=1):
        super().__init__(image, scale)
        self.scrolling_speed = -7
        self.agent_passed = False

    gap_index = 0
    @classmethod
    def create_new_wall(cls, sprites, height):

        wall_bottom = cls(wall)
        wall_bottom.top = 200
        #wall_bottom.top = random.randrange(sprites['ground'].height + 50, height - 120 - 50)
        wall_bottom.left = sprites['background'].width

        wall_top = cls(wall)
        reversed_angle = 180
        wall_top.angle = reversed_angle
        wall_top.bottom = wall_bottom.top + 120
        wall_top.left = sprites["background"].width
        cls.gap_index = cls.gap_index + 1

        return wall_bottom, wall_top

    def step(self):
        self.center_x += self.scrolling_speed