from src.pdfa import PDFA
from src.utils_pdfa.adact_utils import *
from src.utils_pdfa.State import State
from env.get_ao import get_r, get_o, get_a

def get_initial_candidates(D, first_obs, A, pdfa, Q_c, Q_prev_list):
    Q_prev_list[0] = []
    candidates = get_first_obs(first_obs)
    print("candidates", candidates)
    for i in range(candidates.shape[0]):
        q_c = candidates[i, :]
        X = get_first_suffixes(D, first_obs, q_c)
        trajs = np.where(np.all(first_obs == q_c, axis=1))
        print("trajs", trajs, len(trajs[0]))
        Q_c.append(State('q' + pdfa.get_count(), X, A, q_c, trajs))
        Q_prev_list[0].append(pdfa.initial_state)
    return Q_c, Q_prev_list


def get_max_qao(Q):
    state = t = None
    n = -1
    for i in range(len(Q)):
        if Q[i]:
            for q in Q[i]:
                if q.n > n:
                    t = i
                    state = q
    return state, t


def remove_candidate_from_Q(Q, Q_c, Q_prev_list, q, t):
    Q_c.remove(q)
    del Q_prev_list[t][Q[t].index(q)]
    Q[t].remove(q)

    return Q, Q_c


def add_state_to_Q_final(Q_final, Q, t, q, pdfa, Q_prev_list):
    if Q_final[t] == None:
        Q_final[t] = []
    Q_final[t].append(q)
    pdfa.add_transition(Q_prev_list[t][Q[t].index(q)], get_a(q), q, get_o(q), get_r(q))
    #remove candidate from list
    return Q_final, Q


def learn_cyclic_pdfa(D, first_obs, A, a_dict, K, H):
    Q = [None] * H  #list of lists for all candidates
    Q_final = [None] * H  # list of lists for final safe states
    Q_prev_list = [None] * H
    Q_c = []  # Full candidate list
    # add initial pdfa state
    pdfa = PDFA(D, A, a_dict)
    q0 = pdfa.initial_state
    q0.hist = list(range(K + 1))
    # add first list of candidates
    Q_c, Q_prev_list = get_initial_candidates(D, first_obs, A, pdfa, Q_c, Q_prev_list)
    Q[0] = Q_c
    # after this Q_c becomes the list of all candidates
    while Q_c:
        # get most occurring qao across all times
        # the time t wouldn't matter in the first case, you're not supposed to have all the q states from the start
        q_max, t_max = get_max_qao(Q)
        # remove it after promoting
       # Q, Q_c = remove_candidate_from_Q(Q, Q_c, Q_prev_list, q_max, t_max)
        # get similar states by comparing to all times till t_max
        similar = []
        # promote if no similar
        if not similar:
            Q_final = add_state_to_Q_final(Q_final, Q, t_max, q_max, pdfa, Q_prev_list)
            Q, Q_c = remove_candidate_from_Q(Q, Q_c, Q_prev_list, q_max, t_max)
            # add new candidates stemming from this state
            add_new_candidates(q_max,D, ) #how to know where the next candidate comes from
    return pdfa
