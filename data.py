import pygame

# Database Class
class Database:
    # Colors
    WHITE = (0, 0, 0)
    GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE = (0,0,255)
    GREEN = (0, 200, 0)
    DARK_RED = (100, 0, 0)
    DARK_BLUE = (100, 100, 150)
    DARK_GREEN = (0, 100, 0)
    ## Colors Pale
    RED_PALE = (250, 200, 200)
    DARK_RED_PALE = (150, 100, 100)
    GREEN_PALE = (200, 250, 200)
    DARK_GREEN_PALE = (100, 150, 100)
    BLUE_PALE = (200, 200, 255)

    # Font
    pygame.font.init()
    NODE_FONT = pygame.font.SysFont("comicsans", 15)
    STAT_FONT = pygame.font.SysFont("comicsans", 50)

    # Visualization parameters
    NODE_RADIUS = 20
    NODE_SPACING = 5
    LAYER_SPACING = 100
    INPUT_NEURONS = 2
    OUTPUT_NEURONS = 2
    CONNECTION_WIDTH = 2
    INPUT_NAMES = ["Player Y", "Ball Y"]
    OUTPUT_NAMES = ["Move up", "Move down"]

    # Internal parameters
    INPUT = 0
    MIDDLE = 1
    OUTPUT = 2
    ACTIVATION_TRESHOLD = 0.5

# Best genome database
class BestData:
    def __init__(self, win) -> None:
        self.win = win
        self.bestInputs = 0
        self.bestCommands = 0

# function that decode inputs
def decodeCommand(commands, type):
    if commands[type] > Database.ACTIVATION_TRESHOLD:
        if type == 0 and commands[type] > commands[1]:
            return True
        elif type == 1 and commands[type] > commands[0]:
            return True
    return False