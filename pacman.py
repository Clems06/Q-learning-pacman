import random

import pygame
import pickle
import numpy as np
import sys

import json
print(sys.maxsize)

class Ghost:
    def __init__(self, game, name, pos=None):
        self.game = game
        self.name = name

        if not pos:
            self.pos= len(self.game.map)
        else:
            self.pos = pos

        self.last_move = (0,0)

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]



    def move_to_target(self, target_pos):
        actual_pos = self.game.map[self.pos]
        distances = [100] * len(self.directions)

        for i in range(len(self.directions)):
            x_move, y_move = self.directions[i]
            if (-x_move, -y_move) == self.last_move:
                continue
            potential_pos = (actual_pos[0] + x_move, actual_pos[1] + y_move)
            if potential_pos not in self.game.map:
                continue
            else:
                distances[i] = ((potential_pos[0] - target_pos[0]) ** 2 + (
                            potential_pos[1] - target_pos[1]) ** 2) ** 0.5

        return distances.index(min(distances))

    def move(self):
        if self.pos == len(self.game.map):
            return
        x, y = self.game.map[self.pos]
        if x == 0 and self.last_move==(-1,0):
            self.pos = self.game.map.index((27,y))
        elif x == 27 and self.last_move==(1,0):
            self.pos = self.game.map.index((0, y))
        if (x,y) not in self.game.ghost_decision_points:
            for x_move,y_move in self.directions:

                if (-x_move, -y_move) != self.last_move and (x+x_move,y+y_move) in self.game.map:
                    self.pos = self.game.map.index((x+x_move,y+y_move))
                    self.last_move = (x_move,y_move)
                    break
        else:

            pac_pos = self.game.map[self.game.pacman_pos]
            if self.name == "red":
                target_pos = pac_pos
            elif self.name == "pink":
                target_pos = (pac_pos[0]+self.directions[self.game.heading][0]*4,pac_pos[1]+self.directions[self.game.heading][1]*4)
            elif self.name == "blue":
                red_pos = self.game.map[self.game.ghosts[0].pos]
                infront_of_pac_man_pos = (pac_pos[0]+self.directions[self.game.heading][0]*2,pac_pos[1]+self.directions[self.game.heading][1]*2)
                target_pos = (2*infront_of_pac_man_pos[0]-red_pos[0],2*infront_of_pac_man_pos[1]-red_pos[1])
            elif self.name == "orange":
                distance = ((x - pac_pos[0]) ** 2 + (y - pac_pos[1]) ** 2) ** 0.5
                if distance<8:
                    target_pos = (0,31)
                else:
                    target_pos = pac_pos



            chosen_mov = self.move_to_target(target_pos)
            self.last_move = self.directions[chosen_mov]
            x,y = self.game.map[self.pos]
            self.pos = self.game.map.index((x+self.last_move[0],y+self.last_move[1]))





class Pac_Man_Game:
    def __init__(self, alpha=0.4, gamma=0.8, epsilon=0.4, decrease_epsilon=0.995):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.decrease_epsilon = decrease_epsilon

        self.map = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1), (24, 1), (25, 1), (26, 1), (1, 2), (6, 2), (12, 2), (15, 2), (21, 2), (26, 2), (1, 3), (6, 3), (12, 3), (15, 3), (21, 3), (26, 3), (1, 4), (6, 4), (12, 4), (15, 4), (21, 4), (26, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (16, 5), (17, 5), (18, 5), (19, 5), (20, 5), (21, 5), (22, 5), (23, 5), (24, 5), (25, 5), (26, 5), (1, 6), (6, 6), (9, 6), (18, 6), (21, 6), (26, 6), (1, 7), (6, 7), (9, 7), (18, 7), (21, 7), (26, 7), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (9, 8), (10, 8), (11, 8), (12, 8), (15, 8), (16, 8), (17, 8), (18, 8), (21, 8), (22, 8), (23, 8), (24, 8), (25, 8), (26, 8), (6, 9), (12, 9), (15, 9), (21, 9), (6, 10), (12, 10), (15, 10), (21, 10), (6, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (16, 11), (17, 11), (18, 11), (21, 11), (6, 12), (9, 12), (18, 12), (21, 12), (6, 13), (9, 13), (18, 13), (21, 13), (0, 14), (1, 14), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14), (23, 14), (24, 14), (25, 14), (26, 14), (27, 14), (6, 15), (9, 15), (18, 15), (21, 15), (6, 16), (9, 16), (18, 16), (21, 16), (6, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (21, 17), (6, 18), (9, 18), (18, 18), (21, 18), (6, 19), (9, 19), (18, 19), (21, 19), (1, 20), (2, 20), (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20), (11, 20), (12, 20), (15, 20), (16, 20), (17, 20), (18, 20), (19, 20), (20, 20), (21, 20), (22, 20), (23, 20), (24, 20), (25, 20), (26, 20), (1, 21), (6, 21), (12, 21), (15, 21), (21, 21), (26, 21), (1, 22), (6, 22), (12, 22), (15, 22), (21, 22), (26, 22), (1, 23), (2, 23), (3, 23), (6, 23), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23), (13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23), (19, 23), (20, 23), (21, 23), (24, 23), (25, 23), (26, 23), (3, 24), (6, 24), (9, 24), (18, 24), (21, 24), (24, 24), (3, 25), (6, 25), (9, 25), (18, 25), (21, 25), (24, 25), (1, 26), (2, 26), (3, 26), (4, 26), (5, 26), (6, 26), (9, 26), (10, 26), (11, 26), (12, 26), (15, 26), (16, 26), (17, 26), (18, 26), (21, 26), (22, 26), (23, 26), (24, 26), (25, 26), (26, 26), (1, 27), (12, 27), (15, 27), (26, 27), (1, 28), (12, 28), (15, 28), (26, 28), (1, 29), (2, 29), (3, 29), (4, 29), (5, 29), (6, 29), (7, 29), (8, 29), (9, 29), (10, 29), (11, 29), (12, 29), (13, 29), (14, 29), (15, 29), (16, 29), (17, 29), (18, 29), (19, 29), (20, 29), (21, 29), (22, 29), (23, 29), (24, 29), (25, 29), (26, 29)]


        self.pacman_pos = self.map.index((13,23))
        self.ghosts = [Ghost(self, "red", self.map.index((13,11))), Ghost(self, "pink"), Ghost(self,"blue"), Ghost(self,"orange")]
        self.ghost_decision_points = [(6, 1), (21, 1), (1, 5), (6, 5), (9, 5), (12, 5), (15, 5), (18, 5), (21, 5),
                                      (26, 5), (6, 8), (21, 8), (6, 14), (9, 14), (18, 14), (21, 14), (9, 17), (18, 17),
                                      (6, 20), (9, 20), (18, 20), (21, 20), (6, 23), (9, 23), (18, 23), (21, 23),
                                      (3, 26), (24, 26), (12, 29), (15, 29)]
        self.ghosts_waves_apparition = [0, 2, 30, 100]

        #self.ghosts = [Ghost(self, "red")]


        self.points = self.map.copy()
        self.wave = 0

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.heading = 0

        self.reward = 0
        #self.brain = [[0]*4]*len(self.map)**5
        self.brain = {}

        #self.brain= np.zeros((int(len(self.map)**5/1000),4),np.float16)

    def show(self):
        wide = 28
        long = 30
        print("_"*(wide+2))
        for y in range(long):
            print("|", end="")
            for x in range(wide):
                if (x,y) in self.map:
                    pos = self.map.index((x,y))
                    if pos == self.pacman_pos:
                        print("C", end="")
                    elif pos in self.ghosts:
                        print("G", end="")
                    elif (x,y) in self.points:
                        print("°", end = "")
                    else:
                        print("_", end= "")
                else:
                    print(" ", end= "")

            print("|")
        print("-" * (wide+2))




    def move_ghosts(self):
        for i in self.ghosts:
            i.move()

    def pygame_display(self, screen):
        for x,y in self.points:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect((x+0.25)*k, (y+0.25)*k, 0.25*k, 0.25*k))

        pac_x, pac_y = self.map[self.pacman_pos]
        screen.blit(pacmanImg,(pac_x*k,pac_y*k))

        for i in range(len(self.ghosts)):
            if self.ghosts[i].pos != len(self.map):
                x, y = self.map[self.ghosts[i].pos]
                screen.blit(ghost_images[i], (x * k, y * k))
            else:
                screen.blit(ghost_images[i], ((12+i) * k, 14 * k))

    def move_all(self, pac_man_move):
        self.wave += 1

        x_move, y_move = self.directions[pac_man_move] if isinstance(pac_man_move,int) else (0,0)
        x,y = self.map[self.pacman_pos]
        #print(pac_man_move, (x_move, y_move), (x,y), (x_move+x,y+y_move))
        if isinstance(pac_man_move,int) and ((x_move+x)%28,y+y_move) in self.map:
            self.pacman_pos = self.map.index(((x+x_move)%28,y+y_move))
            self.heading = self.directions.index((x_move,y_move))
        else:
            self.reward -= 3
            x_move, y_move = self.directions[self.heading]
            if ((x + x_move)%28, y + y_move) in self.map:
                self.pacman_pos = self.map.index(((x + x_move)%28, y + y_move))
                self.heading = self.directions.index((x_move, y_move))


        self.move_ghosts()

        if self.map[self.pacman_pos] in [self.map[i.pos] for i in self.ghosts if i.pos != len(self.map)]:
            self.reward -= 30
            self.reset()
        elif self.map[self.pacman_pos] in self.points:
            self.points.remove(self.map[self.pacman_pos])
            self.reward+=1
            if len(self.points)==0:
                self.reward = 50
                self.reset()
        else:
            self.reward -= 1

        eaten = len(self.map) - len(self.points)
        if eaten in self.ghosts_waves_apparition:
            self.ghosts[self.ghosts_waves_apparition.index(eaten)].pos = self.map.index((13,11))



    def calculate_situation(self):
        num_options = len(self.map)+1
        closest_point = min([((point[0]-self.map[self.pacman_pos][0]**2+point[1]-self.map[self.pacman_pos][1]**2), point) for point in self.points])
        closest_point_pos = self.map.index(closest_point[1])
        return self.pacman_pos+self.ghosts[0].pos*num_options+self.ghosts[1].pos*num_options**2+self.ghosts[2].pos*num_options**3+self.ghosts[3].pos*num_options**4+closest_point_pos**5



    def choose_and_move(self):
        #self.current_step_count += 1
        old_state = self.calculate_situation()

        if random.uniform(0, 1) < self.epsilon:
            action = random.randint(0, 3)
            self.move_all(action)
        else:
            q_values = self.brain[old_state] if old_state in self.brain else [0]*4
            print(q_values.index(max(q_values)))
            action = q_values.index(max(q_values))
            self.move_all(action)

        new_state = self.calculate_situation()
        future_q_values = self.brain[new_state] if new_state in self.brain else [0]*4
        next_max = max(future_q_values)
        # print("Q-value:",self.brain[self.current_situation], "Reward:",self.reward, "Alpha:",self.alpha,"Next_max:",next_max)
        if old_state not in self.brain:
            self.brain[old_state] = [0]*4
        old_q_value = self.brain[old_state][action]
        self.brain[old_state][action] = (1 - self.alpha) * old_q_value + self.alpha * (
                    self.reward + self.gamma * next_max - old_q_value)
        # print(self.brain[self.current_situation])

        self.reward = 0
        self.epsilon *= self.decrease_epsilon

    def reset(self):
        self.ghosts = [Ghost(self, "red", self.map.index((13, 11))), Ghost(self, "pink"), Ghost(self, "blue"),
                       Ghost(self, "orange")]
        self.points = self.map.copy()
        self.heading = 0
        self.pacman_pos = self.map.index((13, 23))
        self.wave = 0

test = Pac_Man_Game()
test.show()


pax_man_grid = (28, 31)
k = 15
sizes = (pax_man_grid[0]*k,pax_man_grid[1]*k)

for i in range(1000000):
    test.choose_and_move()

pygame.init()



bg = pygame.image.load("pac_man_background.jpg")
bg = pygame.transform.scale(bg, sizes)

pacmanImg = pygame.image.load('pac_man.png')
pacmanImg = pygame.transform.scale(pacmanImg, (k,k))

pinkImg = pygame.image.load('pink.png')
pinkImg = pygame.transform.scale(pinkImg, (k,k))
redImg = pygame.image.load('red.png')
redImg = pygame.transform.scale(redImg, (k,k))
orangeImg = pygame.image.load('orange.png')
orangeImg = pygame.transform.scale(orangeImg, (k,k))
blueImg = pygame.image.load('blue.png')
blueImg = pygame.transform.scale(blueImg, (k,k))

ghost_images = [redImg, pinkImg, blueImg, orangeImg]

#INSIDE OF THE GAME LOOP

# Set up the drawing window
screen = pygame.display.set_mode(sizes)

clock=pygame.time.Clock()
# Run until the user asks to quit
running = True

test.epsilon = 0
test.reset()
for i in range(1000):
    clock.tick(3)

    move = None
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            break

    if not running:
        break

    """keyState = pygame.key.get_pressed()
    if keyState[pygame.K_LEFT]:
        move = 1
    elif keyState[pygame.K_RIGHT]:
        move = 0
    elif keyState[pygame.K_UP]:
        move = 3
    elif keyState[pygame.K_DOWN]:
        move = 2
    pygame.event.pump()"""

    test.choose_and_move()

    screen.blit(bg, (0, 0))

    test.pygame_display(screen)
    pygame.display.flip()



pygame.quit()
