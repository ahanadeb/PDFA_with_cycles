
#see paper https://papers.nips.cc/paper_files/paper/2001/file/a38b16173474ba8b1a95bcbc30d3b8a5-Paper.pdf
import numpy as np
import random
a_dict = {'N': 0, 'S': 1, 'E':2, 'W': 3}
class Tmaze_test:
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
                A = ['E','W']
        return ['N','S','E','W']

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
                    next_s = [s[0], s[1]-1]
        if next_s[1] == self.l and (a=='N' or a=='S') :
            if next_s[0] == self.goal:
                r = 4
            else:
                r = -1
        if np.all(next_s==s):
            r =-1
        return next_s, o, r



    def test(self, pdfa, a_dict1, K, H):

        R = 0
        for k in range(K):
            q = 'q0'
            o,g = self.initialise()
            next_s = [0,0]
            for h in range(H+1):
                #get first q
                if h==0:

                    for o1 in pdfa.transitions[q]:

                        if int(o1) == int(o):
                            q = next(iter(pdfa.transitions[q][o1]))
                else:
                    #get action
                    a = pdfa.policy[q]
                    next_s, o, r = self.get_next_state(a, next_s)
                    a1 =a_dict1[a]
                    for q1 in pdfa.transitions[q][a1]:
                        if int(pdfa.transitions[q][a1][q1][0]) == int(o):
                            q = q1
                    R = R + r
                    #print(q, " a: ", a)
        print("average reward: ", R/K)
        return R / K





