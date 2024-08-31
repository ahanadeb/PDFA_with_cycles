
#see paper https://papers.nips.cc/paper_files/paper/2001/file/a38b16173474ba8b1a95bcbc30d3b8a5-Paper.pdf
import numpy as np
import random
np.set_printoptions(suppress=True)
a_dict = {'N': 0, 'S': 1, 'E':2, 'W': 3}
class Tmaze:
    def __init__(self, l):
        self.l = l
        self.inital_obs = [1011, 1110]
        self.corridor_obs = 1101
        self.T_obs = 1010
        self.current_state=[0,0]
        self.g_pos = [1, -1]
        self.goal = 0

    def get_allowed_actions(self, s):

        if s[1] == self.l:
            A = ['N', 'S']
        else:
            if s[1]<1:
                A=['E']
            else:
                #change this to restrict actions
                A = ['E']
                # A = ['W', 'E']
        #return ['N','S','E','W']
        return A

    def initialise(self):
        a= random.choice([0,1])
        self.goal = self.g_pos[a]
        return  self.inital_obs[a], self.g_pos[a]


    def get_next_state(self, a,s):
        r=0
        if s[1]<self.l:
            o = self.corridor_obs
            if a =='E':
                next_s = [s[0], s[1]+1]
            elif a=='W':
                next_s = [s[0], max(0,s[1]-1)]
            else:
                next_s = s
        if s[1] == self.l:
            o = self.T_obs
            if a == 'N':
                next_s=[1, self.l]
            elif a == 'S':
                next_s = [-1, self.l]
            else:
                if a == 'E':
                    next_s=s
                elif a == 'W':
                    next_s = next_s = [s[0], s[1]-1]



        if next_s[1] == self.l and (a=='N' or a=='S') :
            if next_s[0] == self.goal:
                r = 4
            else:
                r = -1
        if np.all(next_s==s):
            r =-1




        return next_s, o, r



    def simulate(self, K, H):
        D = np.zeros((K, H, 3))
        first_obs = np.zeros((K, 1))

        for k in range(K):


            o1,g = self.initialise()
            first_obs[k, :] = o1
            next_s = [0,0]
            # print("goal position ", g)
            for h in range(H):
                #initialise first observation
                A = self.get_allowed_actions(next_s)
                a = random.choice(A)
                next_s, o,r = self.get_next_state(a, next_s)
                # if next_s[1]==1:
                #     o = o1

                D[k, h, :]= np.array([a_dict[a], o, r])
                #print("action: ", a, " next_s: ", next_s, "reward: ", r)


            #print("final position ", next_s[0], " reward, ", r)
        return D, first_obs

def main():
    l=3
    pg = Tmaze(l)
    D = pg.simulate(10, l+1)


if __name__ == "__main__":
    main(
    )

