import pygame
import numpy as np
import random


def new_state(rows, columns):
    state = np.zeros((rows, columns))
    state[0, :] = -5 * np.ones(columns)
    state[-1, :] = -5 * np.ones(columns)
    state[:, 0] = -5 * np.ones(columns)
    state[:, -1] = -5 * np.ones(columns)
    return state


def update_state(snake, apple, rows, columns):
    state = new_state(rows, columns)
    #for snake in snake_list:

    # head
    if state[snake.body[0][0], snake.body[0][1]] == -5:
        pass # don't overwrite the edge with the snake head
    else:
        state[snake.body[0][0], snake.body[0][1]] = -2
    # rest of body
    for b in snake.body[1:]:
        state[b[0], b[1]] = -3

    state[apple.loc[0], apple.loc[1]] = 5
    return state


def update_display(state, display, square_size, rows, columns):
    for row in range(rows):
        for column in range(columns):
            grid_val = state[row, column]
            if grid_val == 0:
                colour = (0, 0, 0)
            elif grid_val == -2:
                colour = (255, 0, 0)
            elif grid_val == -3:
                colour = (0, 0, 255)
            elif grid_val == 5:
                colour = (0, 255, 0)
            elif grid_val == -5:
                colour = (150, 150, 150)
            pygame.draw.rect(display, colour, pygame.Rect(column*square_size, row*square_size, square_size, square_size))
    return


def get_distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return (dx ** 2 + dy ** 2) ** 0.5


def end_game():
    """Say 'YOU DIED!!!' or something"""
    while True:
        pass

