from src.pdfa import PDFA
from src.utils_pdfa.adact_utils import *
from src.utils_pdfa.State import State
from env.get_ao import get_r, get_o, get_a
from typing import Iterable
# if isinstance(my_item, Iterable):
#     print(True)



def initialise_Q(Q, H):
    for h in range(H):
        Q[h] = []
    return Q


def not_empty(Q):
    if Q:
        for i in range(len(Q)):
            if Q[i]:
                return True
    return False


def get_initial_candidates(D, first_obs, A, pdfa, Q, Q_prev_list):
    candidates = get_first_obs(first_obs)
    print("candidates", candidates)
    for i in range(candidates.shape[0]):
        q_c = candidates[i, :]
        X = get_first_suffixes(D, first_obs, q_c)
        trajs = np.where(np.all(first_obs == q_c, axis=1))
        Q[0].append(State('q' + pdfa.get_count(), X, A, q_c, trajs))
        Q_prev_list[0].append(pdfa.initial_state)
    return Q, Q_prev_list


def add_new_candidates(D, t, q, Q, Q_prev_list, A, pdfa):
    candidates = np.unique(D[q.hist[0], t, :], axis=0)  #t or t-1?
    for i in range(candidates.shape[0]):
        X = get_suffixes(D, candidates[i, :], q, t)
        trajs = np.where(np.all(D[q.hist[0], t, :] == candidates[i, :], axis=1))
        Q[t + 1].append(State('q' + pdfa.get_count(), X, A, candidates[i, :], trajs))
        Q_prev_list[t + 1].append(q)
    return Q, Q_prev_list


def get_max_qao(Q):
    state = t = None
    n = -1
    for i in range(len(Q)):
        if Q[i]:
            if isinstance(Q[i], Iterable):
                for q in Q[i]:
                    if q.n > n:
                        t = i
                        state = q
            else:
                if Q[i].n > n:
                    t = i
                    state = Q[i]

    return state, t


def remove_candidate_from_Q(Q, Q_prev_list, q, t):
    print("removing", q)
    print("Q_prev", Q_prev_list)
    print("Q", Q)
    #THERE is a mismatch in the locaiton where we're adding q in Q CHECK
    del Q_prev_list[t][Q[t].index(q)]
    Q[t].remove(q)

    return Q, Q_prev_list


def add_state_to_Q_final(Q_final, Q, t, q, pdfa, Q_prev_list):
    if Q_final[t] == None:
        Q_final[t] = []
    Q_final[t].append(q)
    pdfa.add_transition(Q_prev_list[t][Q[t].index(q)], get_a(q), q, get_o(q), get_r(q))
    #remove candidate from list
    return Q_final, Q


def get_similar_states(q_max, t_max, Q):
    similar = []
    for t in range(t_max):
        if Q[t]:
            for q in Q[t]:
                sim, threshold, v = test_distinct(q_max, q)
                if sim:
                    similar.append(q)
    return similar


def merge(q1, q2, pdfa):
    q1 = merge_history(q1, q2)
    pdfa.add_transition(q1, get_a(q2), q2, get_o(q2), get_r(q2))


def learn_cyclic_pdfa(D, first_obs, A, a_dict, K, H):
    Q = [None] * H  # list of lists for all candidates
    Q_final = [None] * H  # list of lists for final safe states
    Q_prev_list = [None] * H
    Q_prev_list = initialise_Q(Q_prev_list, H)
    Q = initialise_Q(Q, H)
    # add initial pdfa state
    pdfa = PDFA(D, A, a_dict)
    q0 = pdfa.initial_state
    q0.hist = list(range(K + 1))
    # add first list of candidates
    Q, Q_prev_list = get_initial_candidates(D, first_obs, A, pdfa, Q, Q_prev_list)
    # after this Q_c becomes the list of all candidates
    print("before starting ", Q)
    while not_empty(Q):
        # get most occurring qao across all times
        # print("here", Q)
        q_max, t_max = get_max_qao(Q)
        # remove it after promoting
        # Q, Q_c = remove_candidate_from_Q(Q, Q_c, Q_prev_list, q_max, t_max)
        # get similar states by comparing to all times till t_max
        # do similarity test with all previous time steps HERE you need to change prefix and suffix
        similar = get_similar_states(q_max, t_max, Q)

        # promote if no similar

        if not similar:
            Q_final = add_state_to_Q_final(Q_final, Q, t_max, q_max, pdfa, Q_prev_list)
            print("after adding", Q)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            # add new candidates stemming from this state
            add_new_candidates(D, t_max, q_max, Q, Q_prev_list, A,
                               pdfa)  # how to know where the next candidate comes from
        else:
            # merge candidates
            merge(similar[0], q_max, pdfa)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)

    print("pdfa transitions: ", pdfa.transitions)
    return pdfa
