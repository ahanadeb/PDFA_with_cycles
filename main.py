import json
from src.utils_pdfa.render import render
from env.test_cookie_domain import test_cookie_domain
from learn_pdfa import learn_pdfa
from src.utils_pdfa.params import Params
from src.utils_pdfa.rl_solve import solve_mdp, get_optimal_policy
from env.get_env import get_env
from env.test_t_maze import Tmaze_test


if __name__ == "__main__":

    #set environment
    # env = "cookie-domain"
    # env ="basic-domain"
    #env = "prison-guard"

    env = "t-maze"
    #env="mini-hall"
    K = 5000 #number of episodes
    H = 5 #episode length
    k_length = 100
    A = 4  #action space
    # set parameters
    alpha = 1.6
    params = Params(0.8, 4, 2, 2, 0.1, alpha, 20,20, k_length)
    #get Dataset D
    D, first_obs, a_dict1, a_dict = get_env(env,K, H)
    m = 100
    for i in range(1):
        pdfa, t, sta = learn_pdfa(K,H,D,first_obs, params, a_dict1,a_dict, A)
        if t < m:
            m=t
            print("time ", m)
            ns = sta
    print("Time: ", m,  " States: ", ns)
    #brek
    print(pdfa.transitions)
    #render pdfa
    pdfa= solve_mdp(pdfa, a_dict)
    for s in pdfa.states:
        print(s.VA)
    pdfa = get_optimal_policy(pdfa,a_dict1)
    print("optimal policy ", pdfa.policy)
    gr = render(pdfa, a_dict)
    #generate graph (change location)
    gr.render("/Users/ahanadeb/Documents/books/RL/PhD/bisimulation/countminsketch/graphs/test_"+env+"_alpha_"+str(alpha))
    tmaze = Tmaze_test(H - 1)
    tmaze.test(pdfa, 100, H)


    #test_pdfa(pdfa, 100, 5)