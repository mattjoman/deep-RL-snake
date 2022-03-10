import pygame
import numpy as np
import random


class Snake():
    def __init__(self):
        self.direction = 'd'
        self.body = [[3, 3]]
        self.apple = False

    def set_direction(self):
        return

    def add_to_body(self):
        if self.direction == 'u':
            new_head = [self.body[0][0] - 1, self.body[0][1]]
        elif self.direction == 'd':
            new_head = [self.body[0][0] + 1, self.body[0][1]]
        elif self.direction == 'l':
            new_head = [self.body[0][0], self.body[0][1] - 1]
        else:
            new_head = [self.body[0][0], self.body[0][1] + 1]
        self.body.insert(0, new_head)
        return

    def remove_from_body(self):
        del self.body[-1]
        return

    def move(self):
        self.add_to_body()
        if not self.apple:
            self.remove_from_body()
        else:
            self.apple = False
        return

    def eat_apple(self):
        self.apple = True
        return


class Player(Snake):
    def set_direction(self, keys):
        if keys[pygame.K_LEFT]:
            self.direction = 'l'
        elif keys[pygame.K_RIGHT]:
            self.direction = 'r'
        elif keys[pygame.K_UP]:
            self.direction = 'u'
        elif keys[pygame.K_DOWN]:
            self.direction = 'd'
        return


class AI(Snake):
    pass


class Apple():
    def __init__(self, rows, columns):
        self.set_loc(rows, columns)

    def set_loc(self, rows, columns):
        self.loc = [random.randint(1, rows-2), random.randint(1, columns-2)]
        return


if __name__ == "__main__":
    snake = Snake()
    player = Player()
    ai = AI()
    apple = Apple(100, 100)
    print(player.direction)
