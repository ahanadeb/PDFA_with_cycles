from src.utils_pdfa.render import render
from src.utils_pdfa.params import Params
from src.utils_pdfa.rl_solve import solve_mdp, get_optimal_policy
from env.get_env import get_env
from learn_cyclic_pdfa import learn_cyclic_pdfa

if __name__ == "__main__":
    K = 200
    H = 5
    A = 4
    env = "t-maze"
    alpha = 0.9
    params = Params(0.8, 4, 4, 3, 0.1, alpha, 20, 20, 100)
    #get Dataset D
    D, first_obs, a_dict1, a_dict = get_env(env, K, H)
    pdfa = learn_cyclic_pdfa(D, first_obs, A, a_dict,params, K, H)
    print(pdfa.transitions)
    #render pdfa
    pdfa = solve_mdp(pdfa, a_dict1)
    for s in pdfa.states:
        print(s.name, s.A)
    for s in pdfa.states:
        print(s.VA)
    pdfa = get_optimal_policy(pdfa, a_dict1) #a_dict1 for other cases
    print(pdfa.policy)
    print("optimal policy ", pdfa.policy)
    gr = render(pdfa, a_dict,a_dict1)
    #generate graph (change location)
    gr.render("./graphs/test_" + env + str(alpha))

