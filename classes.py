import pygame
import numpy as np
import random
import torch
from torch import nn
from torch.nn import functional as F






class CNN(torch.nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        torch.manual_seed(50)
        self.layer1 = nn.Sequential(
            # input: (1, 1, 10, 10)
            # output: (1, 8, 18, 18)
            nn.Conv2d(3, 32, (3, 3), stride=1),
            nn.ReLU())
        self.layer2 = nn.Sequential(
            # input: (8, 8, 8, 8)
            # output: (8, 8, 6, 6)
            nn.Conv2d(32, 64, (3, 3), stride=1),
            nn.ReLU())
        self.layer3 = nn.Sequential(
            # input: (8, 8, 6, 6)
            # output: (8, 8, 4, 4)
            nn.Conv2d(64, 32, (3, 3), stride=1),
            nn.ReLU())
        self.layer4 = nn.Sequential(
            # input: (32*4*4)
            nn.Linear(512, 128, bias=True),
            nn.ReLU())
        self.layer5 = nn.Sequential(
            nn.Linear(128, 4, bias=True))

        #self.optimiser = torch.optim.SGD(self.parameters(), lr=1)
        self.optimiser = torch.optim.Adam(self.parameters(), lr=1)

    def forward(self, x):
        out = self.layer1(x.to(torch.float32))
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0), -1) # flatten
        out = self.layer4(out)
        out = self.layer5(out)
        #print(out)
        return out






class Snake():
    def __init__(self, rows=10, columns=10):
        self.direction = 3
        self.init_body(rows, columns)
        self.apple = False
        self.init_score()
        self.init_timestep_counter()

    def set_direction(self):
        return

    def add_to_body(self):
        if self.direction == 2:
            new_head = [self.body[0][0] - 1, self.body[0][1]]
        elif self.direction == 3:
            new_head = [self.body[0][0] + 1, self.body[0][1]]
        elif self.direction == 0:
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
        self.timestep_counter += 1
        if not self.apple:
            self.remove_from_body()
        else:
            self.apple = False
        return

    def eat_apple(self):
        self.apple = True
        self.score += 1
        return

    def init_score(self):
        self.score = 0
        return

    def init_timestep_counter(self):
        self.timestep_counter = 0
        return

    def init_body(self, rows, columns):
        # make start location random
        self.body = [[np.random.random_integers(1, rows-2), np.random.random_integers(1, columns-2)]]





class Player(Snake):
    def set_direction(self, keys):
        if keys[pygame.K_LEFT]:
            self.direction = 0 # left
        elif keys[pygame.K_RIGHT]:
            self.direction = 1 # right
        elif keys[pygame.K_UP]:
            self.direction = 2 # up
        elif keys[pygame.K_DOWN]:
            self.direction = 3 # down
        return





class AI(Snake):
    def __init__(self):
        super().__init__()
        self.epsilon = 0.1
        self.gamma = 0.3
        self.Q_net = CNN()
        self.target_Q_net = self.Q_net
        self.replay_mem = []
        self.replay_mem_limit = 500
        self.batch_size = 64
        self.game_count = 0

    def set_direction(self, state):
        Q_vals = self.get_Q_vals(state)
        self.direction, _ = self.select_action(Q_vals)
        return

    def select_action(self, Q_vals):
        max_ = Q_vals.max().item()
        for i in range(4):
            if Q_vals[0][i].item() == max_:
                greedy_direction = i
        random_num = np.random.uniform(0, 1)
        self.epsilon = 1 / (self.game_count ** (1/2.5))
        if random_num > self.epsilon:
            return greedy_direction, max_
        else:
            return np.random.random_integers(0, 3), Q_vals[0][i].item()

    def get_Q_vals(self, state, rows=10, columns=10):
        return self.Q_net.forward(torch.from_numpy(state))

    def get_target_Q_vals(self, state, rows=10, columns=10):
        return self.target_Q_net.forward(torch.from_numpy(state))

    def learn_from_mem(self):
        if self.timestep_counter % 5 == 0:
            self.target_Q_net = self.Q_net

        if len(self.replay_mem) < self.batch_size:
            return

        #cum_loss = 0
        for b in range(self.batch_size):

            # select the memory
            mem = self.select_mem()

            # get reward for this transition
            reward = mem[2]

            Q_0_vals = self.get_Q_vals(mem[0])
            Q_1_vals = self.get_target_Q_vals(mem[3])

            Q_0 = Q_0_vals[0][mem[1]] # get Q val for the action taken
            Q_1 = Q_1_vals.max().detach()   # get the maximum Q val for the next state

            # need Q_0 and Q_1 to be tensors?
            loss = F.smooth_l1_loss(Q_0, (self.gamma * Q_1) + reward)
            #cum_loss += loss.item()
            self.Q_net.optimiser.zero_grad()
            loss.backward()
            #print(); print(); print()
            for param in self.Q_net.parameters():
                param.grad.data.clamp_(-1, 1)
            self.Q_net.optimiser.step()
        #print(cum_loss/64)
        return

    def update_replay_mem(self, s0, a0, r, s1):
        if len(self.replay_mem) >= self.replay_mem_limit:
            del self.replay_mem[0]
        self.replay_mem.append([s0, a0, r, s1])
        return

    def select_mem(self):
        index = np.random.random_integers(0, len(self.replay_mem)-1)
        return self.replay_mem[index]







class Apple():
    def __init__(self, rows, columns):
        self.set_loc(rows, columns)

    def set_loc(self, rows, columns):
        #self.loc = [random.randint(1, rows-2), random.randint(1, columns-2)]
        self.loc = [5, 5]
        return


if __name__ == "__main__":
    """
    """
    ai = AI()
    state = np.random.rand(20, 20)
    ai.set_direction(state)
    print(ai.direction)
    print(ai.body[0])
    ai.move()
    print(ai.body[0])
