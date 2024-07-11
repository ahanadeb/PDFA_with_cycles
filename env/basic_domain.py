import numpy as np
import random

O = ['o1', 'o2', 'o3', 'o4']
O_first = ['o1', 'o2']
A = ['a1', 'a2']


def test_basic_domain(K,o_dict, a_dict):
    D = np.zeros((K,2,3))
    first_obs=np.zeros((K,1))
    for k in range(K):
        o = random.choice(O_first)
        if o=='o1':
            a = 'a1'
        if o == 'o2':
            a = 'a2'

        first_obs[k]= o_dict[o]

        #a = random.choice(A)

        o1, r= get_reward(o,a)

        D[k,1, :]=[a_dict[a], o_dict[o1], r]
    print(D)


    return D, first_obs,






def get_reward(o, a):
    if o == O[0] and a == A[0]:
        return O[2], 1
    elif o == O[1] and a == A[1]:
        return O[2],1
    return O[2], 0
