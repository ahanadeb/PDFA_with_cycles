from src.utils_pdfa.render import render
from learn_pdfa import learn_pdfa
from src.utils_pdfa.params import Params
from src.utils_pdfa.rl_solve import solve_mdp, get_optimal_policy
from env.get_env import get_env
from env.test_t_maze import Tmaze_test
from learn_cyclic_pdfa import learn_cyclic_pdfa

if __name__ == "__main__":
    K = 10
    H = 4
    A = 2
    env = "loop-domain"

    alpha = 1.6
    params = Params(0.8, 4, 2, 2, 0.1, alpha, 20, 20, 5)
    #get Dataset D
    D, first_obs, a_dict= get_env(env, K, H)
    pdfa = learn_cyclic_pdfa(D, first_obs, A, a_dict, K, H)
    #pdfa, t, sta = learn_pdfa(K, H, D, first_obs, params, a_dict1, a_dict, A)
    #brek
    print(pdfa.transitions)
    #render pdfa
    pdfa = solve_mdp(pdfa, a_dict)
    for s in pdfa.states:
        print(s.VA)
    #pdfa = get_optimal_policy(pdfa, a_dict1)
    #print("optimal policy ", pdfa.policy)
    gr = render(pdfa, a_dict)
    #generate graph (change location)
    gr.render("./graphs/test_" + env + "_alpha_" + str(alpha))

    #test_pdfa(pdfa, 100, 5)
