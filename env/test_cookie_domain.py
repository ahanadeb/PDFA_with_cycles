
from env.cookie_domain import Cookie
import numpy as np
import json
import random

def test_cookie_domain(K,H,o_dict,a_dict, o_dict1):

    D =np.zeros((K, H+1, 3))
    text  = []
    first_obs = np.zeros((K,1))

    for k in range(0,K):
        cookie_domain = Cookie()
        cookie_domain.current_state = random.choice(cookie_domain.initial_states)
        t = o_dict1[cookie_domain.current_state]+" ,"
        first_obs[k] = cookie_domain.current_state
        for h in range(0,H):

            a , o, r= cookie_domain.do_action()
            a_n = a_dict[a]
            o_n = o_dict[o]
            t = t+" "+ a + "  " + o + " "+ str(r) + ","

            D[k,h+1,:] = np.array([a_n, o_n, r])
        text.append(t+'--------------------------------------------')
        # write data to file (change location)
    with open("/Users/ahanadeb/Documents/books/RL/PhD/bisimulation/countminsketch/graphs/text.txt",
              'w') as filehandle:
        json.dump(text, filehandle)
    return D, first_obs

