import arcade

import tools
import environment
import agent
import window
import time
import os
import matplotlib.pyplot as plt

FILE_AGENT = 'agent_flappy.txt'

if __name__ == "__main__":

    window = window.Window(288, 512)
    window.setup()
    arcade.run()

    plt.plot(window.history)
    plt.show()
