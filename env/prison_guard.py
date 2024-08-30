import random

import numpy as np

initial_states = [0, 1]
A = ['a0', 'a1']
a_dict = {'a0': 0, 'a1': 1}
R = [0, 1]


class Prison_guard():
    def __init__(self, p, m):
        self.p0_initial = p
        self.p0 = p  # probability of observing guard at 0th row
        self.p1 = 1 - p
        self.m = m  # number of columns
        self.current_state = None
        self.guard_pos = 0
        self.guard_pos = None

    def set_guard_pos(self):
        if random.uniform(0, 1) > self.p0:
            self.guard_pos = 1
        else:
            self.guard_pos = 0


    def switch_prob(self):
        p = self.p1
        self.p1 = self.p0
        self.p0 = p

    def set_initial_state(self):
        self.current_state = [random.choice(initial_states), 0]
        self.p0 = self.p0_initial
        self.p1 = 1-self.p0

    def get_next_state(self, a):
        r = 0
        next_s = [a_dict[a], self.current_state[1] % self.m + 1]
        if next_s[0] != self.guard_pos:
            r = 1
            enemy = 0
        else:
            enemy = 1
        self.current_state = next_s
        return next_s, r, enemy

    def ifenemy(self):
        if self.current_state[0] == self.guard_pos:
            return 1
        return 0

    def simulate(self, K, H):

        D = np.zeros((K, H+1, 5))
        first_obs = np.zeros((K, 3))
        for k in range(K):
            self.guard_pos = None
            self.set_initial_state()
            first_obs[k, :] = np.array([self.current_state[0], self.current_state[1], self.ifenemy()])
            self.set_guard_pos()
            for h in range(H):
                a = random.choice(A)
                next_s, r, enemy = self.get_next_state(a)
                D[k, h, :] = np.array([a_dict[a], next_s[0], next_s[1], enemy, r])
                if enemy == 1:
                    self.switch_prob()
                    self.set_guard_pos()
            self.current_state = None

        return D.astype(int), first_obs.astype(int)


def main():
    pg = Prison_guard(1, 5)
    D = pg.simulate(2, 10)
    print(D)


if __name__ == "__main__":
    main(
    )
