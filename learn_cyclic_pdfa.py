import time
from src.pdfa import PDFA
from src.utils_pdfa.adact_utils import *
from src.utils_pdfa.State import State

def get_initial_candidates(D, first_obs,A,pdfa, Q_c):
    candidates = get_first_obs(first_obs)
    print("candidates", candidates)
    for i in range(candidates.shape[0]):
        q_c = candidates[i, :]
        X = get_first_suffixes(D, first_obs, q_c)
        trajs = np.where(np.all(first_obs == q_c, axis=1))
        Q_c.append(State('q' + pdfa.get_count(), X, 0, A, trajs))
    return Q_c

def learn_cyclic_pdfa(D, first_obs, A, a_dict, K, H):
    Q = [] #list of lists
    Q_c = [] #Full candidate list
    #add initial pdfa state
    pdfa = PDFA(D, A, a_dict)
    q0 = pdfa.initial_state
    q0.hist = list(range(K + 1))
    #add first list of candidates
    Q_c = get_initial_candidates(D, first_obs,A,pdfa, Q_c)
    Q.append(Q_c)
    while Q_c:
        #get most occuring qao across all times
        #the time t wouldn't matter in the first case, you're not supposed to have all the q states from the start


    return pdfa