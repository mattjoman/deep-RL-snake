import pygame
import numpy as np
import random
import matplotlib.pyplot as plt

import functions as fn
import classes


def train_ai(rows=20, columns=20, square_size=16):

    GAMES = 1000

    returns = np.empty(GAMES)

    # initialise network with random weights
    snake = classes.AI()

    ## sequence of the last 3 states
    state_sequence = np.empty([1, 3, rows, columns])
    state_sequence[0, 0, :, :] = fn.new_state(rows, columns)
    state_sequence[0, 1, :, :] = fn.new_state(rows, columns)
    state_sequence[0, 2, :, :] = fn.new_state(rows, columns)


    for game in range(GAMES):

        rtrn = 0

        ## initialise state
        state = fn.new_state(rows, columns)
        apple = classes.Apple(rows, columns)

        # New episode, re-initialise snake
        snake.init_body(rows, columns)
        snake.init_score()
        snake.init_timestep_counter()
        snake.game_count += 1


        pygame.init()
        display = pygame.display.set_mode((columns*square_size, rows*square_size))
        pygame.display.set_caption('Test')
        clock = pygame.time.Clock()

        playing = True
        while playing:


            ## CHOOSE ACTION AND EXECUTE THE ACTION
            ## select action
            # give state to the network, get the resulting action
            snake.set_direction(state_sequence)
            a0 = snake.direction

            ## execute action
            snake.move()

            ## observe next state
            s0 = state_sequence
            if fn.get_distance(snake.body[0], apple.loc) <= 1:
                apple.set_loc(rows, columns)
                snake.eat_apple()

            ## get the next state
            state = fn.update_state(snake, apple, rows, columns)

            ## add to state sequence
            state_sequence[0, 0, :, :] = state_sequence[0, 1, :, :]
            state_sequence[0, 1, :, :] = state_sequence[0, 2, :, :]
            state_sequence[0, 2, :, :] = state

            fn.update_display(state, display, square_size, rows, columns)

            ## observe reward
            reward = -1
            if snake.apple:
                reward = 50
            for i in snake.body[1:]:
                if snake.body[0] == i:
                    reward = 0
                    playing = False
            if state[snake.body[0][0], snake.body[0][1]] == -5:
                reward = 0
                playing = False
            rtrn += reward

            ## store experience in replay-memory
            snake.update_replay_mem(s0, a0, reward, state_sequence)



            pygame.display.update()
            clock.tick()




            ## LEARNING
            snake.learn_from_mem()


        print(f"Game {game}: Score {snake.score}, Survival time {snake.timestep_counter}, Epsilon {snake.epsilon}, Memory length {len(snake.replay_mem)}")
        returns[game] = rtrn
    plt.figure()
    plt.plot(range(GAMES), returns)
    plt.savefig("test.png")


if __name__ == "__main__":
    train_ai(10, 10)
