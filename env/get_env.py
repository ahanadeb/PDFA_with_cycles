
from env.test_cookie_domain import test_cookie_domain
import numpy as np
import pandas as pd
from env.basic_domain import test_basic_domain
from env.prison_guard import Prison_guard
from env.t_maze import Tmaze
from env.loop_domain import LoopDomain
def get_env(env, K, H):
    if env == "cookie-domain":
        o_dict = {'blue': 1, 'white': 2, 'green': 3, 'red': 4, 'green cookie':5, 'blue cookie': 6 }
        a_dict = {'right': 5, 'left': 6, 'up': 7, 'down': 8, 'press': 9, 'eat': 10}
        o_dict1 = {1: 'blue', 2: 'white', 3: 'green', 4: 'red', 5: 'green cookie', 6:'blue cookie'}
        a_dict1 = {5: 'right', 6: 'left', 7: 'up', 8: 'down', 9: 'press', 10: 'eat'}

        D, first_obs= test_cookie_domain(K, H, o_dict, a_dict, o_dict1)

        return D, first_obs, o_dict1, a_dict1


    elif env == "basic-domain":
        o_dict = {'o1': 0, 'o2': 1, 'o3': 2, 'o4':3}
        a_dict = {'a1': 0, 'a2': 1}
        o_dict1 = {0: 'o1', 1: 'o2', 2: 'o3', 3: 'o4'}
        a_dict1 = {0: 'a1', 1: 'a2'}
        D,first_obs =test_basic_domain(K, o_dict, a_dict)
        return D, first_obs, o_dict1, a_dict1

    elif env == "prison-guard":
        a_dict1 = {0: 'a0', 1: 'a1'}
        a_dict = {'a0':0, 'a1':1 }
        pg = Prison_guard(1, 5)
        D, first_obs = pg.simulate(K, H)
        return D.astype(int), first_obs, a_dict1, a_dict


    elif env == "t-maze":
        a_dict = {'N': 0, 'S': 1, 'E':2, 'W': 3}
        a_dict1 = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}
        T = Tmaze(H-1)
        D , first_obs = T.simulate(K, H)
        return D.astype(int),first_obs, a_dict1, a_dict

    elif env == "mini-hall":
        a_dict = {'forward': 0, 'rotate-l':1,'rotate-r':2}
        a_dict1 = {0: 'forward', 1:'rotate-l', 2:'rotate-r'}
        D = load_data("/Users/ahanadeb/Documents/books/RL/PhD/bisimulation/POMDPs-main/hallway/hallway_csv2/", K, H)

        first_obs = np.array(pd.read_csv("/Users/ahanadeb/Documents/books/RL/PhD/bisimulation/POMDPs-main/hallway/hallway_csv2/first_obs.csv", sep=',', header=None))

        return D.astype(int), first_obs, a_dict1, a_dict


    elif env == "loop-domain":
        a_dict={0:0, 1:1}
        # a_dict1 = { 0: 'a0', 1: 'a1'}
        loop = LoopDomain()
        D, first_obs = loop.generate_trajs(K, H)

        return D.astype(int), first_obs, a_dict


    else:
        raise ValueError("Environment not found")




def load_data(path, K, H):
    D = np.zeros((K, H+1, 3))  # Dataset of K episodes of H length horizons
    for k in range(K):
        path_csv = path + str(
            k) + '.csv'
        df = pd.read_csv(path_csv, sep=',', header=None)
        #df = df.drop([0, 2, 4], axis=1)
        D[k, 1:, :] = np.array(df)

    return D