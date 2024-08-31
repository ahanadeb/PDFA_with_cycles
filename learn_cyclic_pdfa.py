from src.pdfa import PDFA
from src.utils_pdfa.adact_utils import *
from src.utils_pdfa.State import State
from env.get_ao import get_r, get_o, get_a
from typing import Iterable

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
        trajs = np.where(np.all(D[:, t, :] == candidates[i, :], axis=1))
        trajs = remove_nc(trajs, q.hist[0])
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
    q_prev = get_prev_state(q, t, Q, Q_prev_list)
    Q_prev_list[t].remove(q_prev)
    Q[t].remove(q)
    return Q, Q_prev_list

def get_prev_state(q,t,Q, Q_prev_list):
    ind = Q[t].index(q)
    q_prev =Q_prev_list[t][ind]
    return q_prev



def add_state_to_Q_final(Q_final, Q, t, q, pdfa, Q_prev_list):
    Q_final[t + 1].append(q)
    pdfa.add_transition(Q_prev_list[t][Q[t].index(q)], get_a(q), q, get_o(q), get_r(q))
    return Q_final


def get_similar_states(q_max, t_max, Q_final):
    similar = []
    for t in range(0, t_max+2):
        if Q_final[t]:
            for q in Q_final[t]:
                sim, threshold, v = test_distinct(q_max, q)
                if sim:
                    similar.append(q)
    return similar


def merge(q1, q2, q_prev, pdfa):

    q1 = merge_history(q1, q2)
    if q_prev == q1:
            #print("here", q2.c, get_a(q2), get_r(q2))

        pdfa.add_transition(q1, get_a(q2), q1, get_o(q2), get_r(q2))


    else:
        pdfa.add_transition(q_prev, get_a(q2), q1, get_o(q2), get_r(q2))
    return q1


def printn(s, Q):
    print(s)
    for i in range(len(Q)):
        if Q[i]:
            print("t: ", i)
            for q in Q[i]:
                print(q.name)


def learn_cyclic_pdfa(D, first_obs, A, a_dict, K, H):
    Q = [None] * (H + 1)  # list of lists for all candidates
    Q_final = [None] * (H + 1)  # list of lists for final safe states
    Q_prev_list = [None] * (H + 1)
    Q_prev_list = initialise_Q(Q_prev_list, H + 1)
    Q = initialise_Q(Q, H + 1)
    Q_final = initialise_Q(Q_final, H + 1)
    # add initial pdfa state
    pdfa = PDFA(D, A, a_dict)
    q0 = pdfa.initial_state
    q0 = get_suffixes_q0(q0)
    Q_final[0].append(q0)
    q0.hist = (np.array(list(range(K + 1))),)
    # add first list of candidates
    Q, Q_prev_list = get_initial_candidates(D, first_obs, A, pdfa, Q, Q_prev_list)
    # after this Q_c becomes the list of all candidates
    while not_empty(Q):
        # printn("Q_prev_list", Q_prev_list)
        # printn("Q", Q)
        q_max, t_max = get_max_qao(Q)
        similar = get_similar_states(q_max, t_max, Q_final)
        # promote if no similar
        if not similar:
            print("not similar, removing ", q_max.name)
            Q_final = add_state_to_Q_final(Q_final, Q, t_max, q_max, pdfa, Q_prev_list)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            # add new candidates stemming from this state
            Q, Q_prev_list = add_new_candidates(D, t_max, q_max, Q, Q_prev_list, A, pdfa)
            # printn("Q_prev_list", Q_prev_list)
            # printn("Q", Q)

        else:

            print("merging ", similar[0].name, q_max.name, q_max.c)
            # merge candidates
            q_prev= get_prev_state(q_max, t_max, Q, Q_prev_list)
            similar[0]= merge(similar[0], q_max,q_prev, pdfa)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            # printn("Q_prev_list", Q_prev_list)
            # printn("Q", Q)
        #print("Q_final after adding ", Q_final)
        # lp = lp +1
        # if lp ==2:
        #     brek
    print("pdfa transitions: ", pdfa.transitions)
    print("suffixes")
    for q in pdfa.states:
        print(q.name, q.X)
    # printn("Q_final", Q_final)
    return pdfa
