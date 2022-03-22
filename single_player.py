import pygame
import numpy as np
import random

import functions as fn
import classes


def run(rows, columns, square_size=4):

    state = fn.new_state(rows, columns)

    pygame.init()
    display = pygame.display.set_mode((columns*square_size, rows*square_size))
    pygame.display.set_caption('Test')
    clock = pygame.time.Clock()
    running = True

    snake_list = []
    snake_list.append(classes.Player())
    apple = classes.Apple(rows, columns)

    while running:

        # Quit
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        snake_list[0].set_direction(keys)

        for snake in snake_list:
            snake.move()

        state = fn.update_state(snake_list, apple, rows, columns)
        fn.update_display(state, display, square_size, rows, columns)

        for snake in snake_list:

            if fn.get_distance(snake.body[0], apple.loc) <= 1:
                print("Yum!")
                apple.set_loc(rows, columns)
                snake.eat_apple()

            for i in snake.body[1:]:

                if snake.body[0] == i:
                    print("You tried to eat yourself!!!")
                    #end_game()
                    running = False

            if state[snake.body[0][0], snake.body[0][1]] == -5:
                print("You went off the edge!!!")
                running = False

        pygame.display.update()
        clock.tick()
