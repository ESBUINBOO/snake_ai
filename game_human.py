# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
import neat
import os
pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 50)
GEN = 0
FITNESS_LEVEL = 1000


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle_2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)


class Snake(object):
    body = []
    turns = {}
    move_done = ""

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.move_done == "right":
                    continue
                self.move_left()
                # self.dirnx = -1
                # self.dirny = 0
                # self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                if self.move_done == "left":
                    continue
                self.move_right()
                # self.dirnx = 1
                # self.dirny = 0
                # self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                if self.move_done == "down":
                    continue
                self.move_up()
                # self.dirnx = 0
                # self.dirny = -1
                # self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                if self.move_done == "up":
                    continue
                self.move_down()
                # self.dirnx = 0
                # self.dirny = 1
                # self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def move_left(self):
        self.move_done = "left"
        self.dirnx = -1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move_right(self):
        self.move_done = "right"
        self.dirnx = 1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move_up(self):
        print("Snack.move_up()")
        self.move_done = "up"
        self.dirnx = 0
        self.dirny = -1
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move_down(self):
        self.move_done = "down"
        self.dirnx = 0
        self.dirny = 1
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def calc_distance(food_pos, snake_pos):
    x_distance = snake_pos[0] - food_pos[0]
    y_distance = snake_pos[1] - food_pos[1]
    return x_distance, y_distance


def draw_grid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def draw_board(surface, score):
    text = STAT_FONT.render("Score: " + str(score - 1), 1, (255, 255, 255))
    surface.blit(text, (510, 10))


def redraw_window(surface, score):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    draw_board(surface=surface, score=score)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


# def main(genomes, config):
def main():
    """fitness function for NEAT"""
    global width, rows, s, snack
    global GEN
    global FITNESS_LEVEL
    # neat vars
    GEN += 1
    nets = []
    ge = []
    # pygame vars
    fps = 15
    width = 500
    height = 500
    rows = 20

    # for _, g in genomes:
    #     net = neat.nn.FeedForwardNetwork.create(g, config)
    #     nets.append(net)
    #     birds.append(Bird(230, 250))
    #     g.fitness = 0
    #     ge.append(g)

    window = pygame.display.set_mode((height, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, s), color=(0, 255, 0))
    print("food pos: ", snack.pos)
    running = True
    clock = pygame.time.Clock()

    while running:
        pygame.time.delay(50)
        clock.tick(fps)
        if s.body[0].pos[0] > 19 or s.body[0].pos[1] > 19 or s.body[0].pos[0] < 1 or s.body[0].pos[1] < 1:
            print('Score: ', len(s.body) - 1)
            print('You Lost!', 'Play again...')
            s.reset((10, 10))
            running = False
        s.move()
        ####  uncomment for inputs #######
        # distance = calc_distance(snack.pos, s.body[0].pos)
        # if distance[0] < 0:
        #     s.move_right()
        # elif distance[0] > 0:
        #     s.move_left()
        # elif distance[1] > 0:
        #     s.move_up()
        # elif distance[1] < 0:
        #     s.move_down()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color=(0, 255, 0))
            print("food pos: ", snack.pos)

        for x in range(len(s.body)):
            try:
                if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                    print('Score: ', len(s.body))
                    print('You Lost!', 'Play again...')
                    s.reset((10, 10))
                    running = False
            except IndexError:
                pass

        redraw_window(surface=window, score=len(s.body))


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(main, 15)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    # run(config_file=config_path)
    main()
