import numpy as np
import random


class LoopDomain:
    def __init__(self):
        self.states = ['q0', 'q1']
        self.actions = ['a0', 'a1']
        self.initial_state = 'q0'
        self.current_state = None

    def intialise(self):
        self.current_state = self.initial_state

    def get_next_state(self, a):
        self.current_state = self.states[self.actions.index(a)]

    def simulate(self, K, H):
        for k in range(K):
            self.intialise()
            print(self.current_state)
            for h in range(H):
                a = random.choice(self.actions)
                print("action: ", a)
                self.get_next_state(a)
                print(self.current_state)

    def get_reward(prev_state, b, a):
        if b == 'q0' and a == 'a0':
            return 4
        elif b == 'q1' and a == 'a1':
            return 4
        return 0

    def generate_trajs(self, K, H):
        D = np.zeros((K, H, 3))
        first_obs = np.zeros((K, 1))
        for k in range(K):
            self.intialise()
            first_obs[k, 0] = self.states.index(self.current_state)
            for h in range(H):
                prev_state = self.current_state
                a = random.choice(self.actions)
                self.get_next_state(a)
                r = self.get_reward(prev_state, a)
                D[k, h, :] = np.array([self.actions.index(a), self.states.index(self.current_state), r])
        return D.astype(int), first_obs.astype(int)
