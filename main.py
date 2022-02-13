from os import path
import random
import pygame
import neat
import math

from data import BestData, decodeCommand
from NNdraw import NN

# Pygame costants
WIDTH, HEIGHT = 1200, 500
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
pygame.display.set_icon(pygame.image.load(path.join("Assets", "Ball.png")))

# Font
pygame.font.init()
START_FONT = pygame.font.Font(path.join("Assets", "font.ttf"), 40)
SCORE_FONT = pygame.font.Font(path.join("Assets", "font.ttf"), 40)

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Costants
MIDDLE_CUBES_SIDE = 20
GAME_WIN = WIDTH / 2

# MAKE IT BETTER
MIN_VALUES = [5, 0]
MAX_VALUES = [395, 500 - 20]

# Classes
class Ball:
    SIDE = 20
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.randint(20, 50) # In degrees
        self.vel = random.choice([-2, 2])
    
    def move(self):
        vertical_movement = math.tan(math.radians(self.angle)) * self.vel
        self.y += vertical_movement
        self.x += self.vel

    def change_vertical_dir(self):
        self.angle *= -1

    def change_horizontal_dir(self):
        self.vel *= -1

    def increment_vel(self):
        if self.vel > 0:
            self.vel += 0.001
        else:
            self.vel -= 0.001

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.SIDE, self.SIDE)

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.get_rect())

class Side:
    VEL = 5
    WIDTH = 15
    HEIGHT = 100
    OFFSET = 5

    def __init__(self, x, color):
        self.x = x
        self.y = HEIGHT/2 - self.HEIGHT/2
        self.color = color

    def move(self, direction):
        if direction == "up" and self.y > self.OFFSET:
            self.y -= self.VEL
        elif direction == "down" and self.y + self.HEIGHT  < HEIGHT - self.OFFSET:
            self.y += self.VEL

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.get_rect())

# Functions
def normalize_inputs(inputs):
    normalized = []
    for i, input_value in enumerate(inputs):
        normalized.append((input_value - MIN_VALUES[i]) / (MAX_VALUES[i] - MIN_VALUES[i]))
    
    return normalized

def get_input_nodes(side, ball):
    return (side.y, ball.y)

def left_lane():
    width = 5
    pygame.draw.line(WIN, GRAY, (GAME_WIN - width, 0), (GAME_WIN - width, HEIGHT), width)

def middle_lane():
    i = 0
    while (i*MIDDLE_CUBES_SIDE)/2 < WIDTH:
        if i % 2 == 0:
            pygame.draw.rect(WIN, GRAY, (GAME_WIN + GAME_WIN/2 - MIDDLE_CUBES_SIDE/2, i*MIDDLE_CUBES_SIDE, MIDDLE_CUBES_SIDE, MIDDLE_CUBES_SIDE))
        i += 1

gen = 0

def main(genomes, config):
    global gen
    gen += 1
    # Neat variables 
    nets = []
    ge = []
    balls = []
    sides = []
    NNs = []
    ## Best player
    best_index = 0
    max_fit = 0
    best = BestData(WIN)

    # Neat adder
    for _, g in genomes: # (id, object)
        # Net
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        # Objects
        color = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))
        balls.append(Ball(3*GAME_WIN/2- Ball.SIDE/2, HEIGHT/2 - Ball.SIDE/2, color))
        sides.append([Side(GAME_WIN + Side.OFFSET, color), Side(WIDTH - Side.OFFSET - Side.WIDTH, color)])
        # Genome
        g.fitness = 0
        ge.append(g)
        NNs.append(NN(config, g, (140, 250)))


    # Reset variables
    run = True
    clock = pygame.time.Clock()

    # Draw function
    def draw():
        WIN.fill((0, 0, 0))
        middle_lane()
        left_lane()
        generation_txt = SCORE_FONT.render(f"Generation: {gen}", True, GRAY)
        alive_txt = SCORE_FONT.render(f"Alive: {len(balls)*2}", True, GRAY)

        WIN.blit(generation_txt, (GAME_WIN + GAME_WIN/4  - generation_txt.get_width()/2 , 50))
        WIN.blit(alive_txt, ((GAME_WIN + (GAME_WIN/4)*3) - alive_txt.get_width()/2, 50))

        for couple in sides:
            couple[0].draw()
            couple[1].draw()
        
        for ball in balls:
            ball.draw()
        
        # Draw neural network
        bestNN.draw(best)

        pygame.display.update()

    # Mainloop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Skip gen for a bug
                    balls = []

        # New gen
        if len(balls) == 0:
            run = False
            break

        for index, ball in enumerate(balls):
            # UP and DOWN window collision
            if ball.y <= 0 or ball.y + ball.SIDE >= HEIGHT: 
                ball.change_vertical_dir()
                ge[index].fitness += 0.1

            # LEFT and RIGHT window collision
            if ball.x <= GAME_WIN or ball.x + ball.SIDE >= WIDTH:
                ge[index].fitness -= 5
                balls.pop(index)
                sides.pop(index)
                nets.pop(index)
                ge.pop(index)
                NNs.pop(index)
                continue

            # SIDE collision
            c = sides[index]
            for couple in c:
                if (ball.get_rect()).colliderect((couple.get_rect())):
                    ge[index].fitness += 2
                    ball.change_horizontal_dir()
                    ball.change_vertical_dir()

        # INPUT / OUTPUT
        for index, couple in enumerate(sides):
            # In
            output_left = nets[index].activate(get_input_nodes(couple[0], balls[index]))
            output_right = nets[index].activate(get_input_nodes(couple[1], balls[index]))

            # Out
            # Left Side
            if decodeCommand(output_left, 0):
                couple[0].move("up")
            elif decodeCommand(output_left, 1):
                couple[0].move("down")
            # Right side
            if decodeCommand(output_right, 0):
                couple[1].move("up")
            elif decodeCommand(output_right, 1):
                couple[1].move("down")

        # Get best player 
        max_fit = 0
        for index, genome in enumerate(ge):
            if genome.fitness > max_fit:
                max_fit = genome.fitness
                best_index = index

        if len(NNs) != 0:
            bestNN = NNs[best_index]
            inputs =  get_input_nodes(couple[0], balls[index])
            best.bestInputs = normalize_inputs(inputs)
            best.bestCommands = nets[best_index].activate(inputs)

        for ball in balls:
            ball.move()
            ball.increment_vel()

        draw()

def run(config_path):
    # Config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Population
    p = neat.Population(config)

    # CMD output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    # Winner players
    winner = p.run(main, 100)

if __name__ == '__main__':
    local_dir = path.dirname(__file__)
    config_path = path.join(local_dir, "config-feedforward.txt")
    run(config_path)