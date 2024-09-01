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


def get_initial_candidates(D, first_obs, A, pdfa, Q, Q_prev_list, S, params):
    candidates = get_first_obs(first_obs)
    for i in range(candidates.shape[0]):
        q_c = candidates[i, :]
        X, S, n , f = get_first_suffixes(D, first_obs, q_c, S, params)
        trajs = np.where(np.all(first_obs == q_c, axis=1))
        q= State('q' + pdfa.get_count(), X, A, q_c, n, trajs)
        q.X2 = f
        Q[0].append(q)
        Q_prev_list[0].append(pdfa.initial_state)

    return Q, Q_prev_list, S


def add_new_candidates(D, t, q, Q, Q_prev_list, A, S, params, pdfa):
    candidates = np.unique(D[q.hist[0], t, :], axis=0)  #t or t-1?
    for i in range(candidates.shape[0]):
        X, S , n , f = get_suffixes(D, candidates[i, :], q, t, S, params)
        trajs = np.where(np.all(D[q.hist[0], t, :] == candidates[i, :], axis=1))
        q_new = State('q' + pdfa.get_count(), X, A, candidates[i, :],n, trajs)
        q_new.X2 = f
        Q[t + 1].append(q_new)
        Q_prev_list[t + 1].append(q)
    return Q, Q_prev_list, S

def add_new_candidates_merge(D, t, q,q_prev, Q, Q_prev_list, A, S, params, pdfa):
    candidates = np.unique(D[q.hist[0], t, :], axis=0)  #t or t-1?
    for i in range(candidates.shape[0]):
        X, S , n , f = get_suffixes(D, candidates[i, :], q, t, S, params)
        trajs = np.where(np.all(D[q.hist[0], t, :] == candidates[i, :], axis=1))
        q_new = State('q' + pdfa.get_count(), X, A, candidates[i, :],n, trajs)
        q_new.X2 = f
        Q[t + 1].append(q_new)
        Q_prev_list[t + 1].append(q_prev)
    return Q, Q_prev_list, S
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
    #THERE is a mismatch in the location where we're adding q in Q CHECK
    del Q_prev_list[t][Q[t].index(q)]
    Q[t].remove(q)

    return Q, Q_prev_list

def get_prev_state(q,t,Q, Q_prev_list):
    ind = Q[t].index(q)
    return Q_prev_list[t][ind]



def add_state_to_Q_final(Q_final, Q, t, q, pdfa, Q_prev_list):
    Q_final[t + 1].append(q)
    pdfa.add_transition(Q_prev_list[t][Q[t].index(q)], get_a(q), q, get_o(q), get_r(q))
    #remove candidate from list
    return Q_final


def get_similar_states(q_max, t_max, Q_final, params, S):
    similar = []
    for t in range(0, t_max+1):
        if Q_final[t]:
            for q in Q_final[t]:
                sim, threshold, v = test_distinct(q_max, q, params, S)
                if sim:
                    similar.append(q)
                    print("similar here ", q_max.name, q.name, threshold, v)
    return similar


def merge(q1, q2, q_prev, pdfa):
    if q1.name == 'q1' and q2.name== 'q6':
        #print("before", pdfa.transitions)
        pdfa.add_transition(q1, get_a(q2), q1, get_o(q2), get_r(q2))
        #print("after", pdfa.transitions)

    q1 = merge_history(q1, q2)
    if q_prev == q1:
        pdfa.add_transition(q1, get_a(q2), q1, get_o(q2), get_r(q2))

    else:
        # if q1.name == 'q1' and q2.name == 'q6':
        #     #print("HERE", q1.name, q2.name, q_prev.name)
        pdfa.add_transition(q_prev, get_a(q2), q1, get_o(q2), get_r(q2))
    return q1


def printn(s, Q):
    print(s)
    for i in range(len(Q)):
        if Q[i]:
            print("t: ", i)
            for q in Q[i]:
                print(q.name)


def learn_cyclic_pdfa(D, first_obs, A, a_dict,params, K, H):
    S = []
    Q = [None] * (H + 1)  # list of lists for all candidates
    Q_final = [None] * (H + 1)  # list of lists for final safe states
    Q_prev_list = [None] * (H + 1)
    Q_prev_list = initialise_Q(Q_prev_list, H + 1)
    Q = initialise_Q(Q, H + 1)
    Q_final = initialise_Q(Q_final, H + 1)
    # add initial pdfa state
    pdfa = PDFA(D, A, a_dict)
    q0 = pdfa.initial_state
    q0 = get_suffixes_q0(q0,params, K, H)
    Q_final[0].append(q0)
    # add first list of candidates
    Q, Q_prev_list, S = get_initial_candidates(D, first_obs, A, pdfa, Q, Q_prev_list, S, params)
    # after this Q_c becomes the list of all candidates
    while not_empty(Q):
        printn("Q_prev_list", Q_prev_list)
        printn("Q", Q)
        q_max, t_max = get_max_qao(Q)
        similar = get_similar_states(q_max, t_max, Q_final,params, S)

        # promote if no similar
        if not similar:
            print("not similar, removing ", q_max.name)
            print("different adding", pdfa.transitions)
            Q_final = add_state_to_Q_final(Q_final, Q, t_max, q_max, pdfa, Q_prev_list)
            print("done different adding", pdfa.transitions)
            # printn("Q_final", Q_final)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            # add new candidates stemming from this state
            Q, Q_prev_list, S = add_new_candidates(D, t_max, q_max, Q, Q_prev_list, A,  S, params, pdfa)
            # printn("Q_prev_list", Q_prev_list)
            # printn("Q", Q)

            #print("added candidates ", Q)
        else:

            print("merging ", similar[0].name, q_max.name)
            # merge candidates
            q_prev= get_prev_state(q_max, t_max, Q, Q_prev_list)
            if q_max.name == 'q4':
                print("HERERE", q_prev.name)
            similar[0]= merge(similar[0], q_max,q_prev, pdfa)
            print(pdfa.transitions)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            if t_max!=H:
                #HERE while adding you've to add the q_prev of q_max to the prev list. not current q_max
                Q, Q_prev_list, S = add_new_candidates_merge(D, t_max, q_max,q_prev, Q, Q_prev_list, A, S, params, pdfa)
            print(pdfa.transitions)
            # printn("Q_prev_list", Q_prev_list)
            # printn("Q", Q)
        #print("Q_final after adding ", Q_final)
        # lp = lp +1
        # if lp ==2:
        #     brek
    # print("pdfa transitions: ", pdfa.transitions)
    #print("suffixes")
    # for q in pdfa.states:
    #     print(q.name, q.X)
    #     print(q.hist)
    printn("Q_final", Q_final)
    return pdfa