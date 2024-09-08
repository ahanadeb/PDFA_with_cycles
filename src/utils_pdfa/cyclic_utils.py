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
        trajs = np.where(np.all(D[:, t, :] == candidates[i, :], axis=1))
        trajs = remove_nc(trajs, q.hist[0])
        q_new = State('q' + pdfa.get_count(), X, A, candidates[i, :],n, trajs)
        q_new.X2 = f
        if not q_new.X2:
            pdfa.add_transition(q, get_a(q_new), pdfa.end_state, get_o(q_new), get_r(q_new))
        else:
            Q[t + 1].append(q_new)
            Q_prev_list[t + 1].append(q)

    return Q, Q_prev_list, S



def add_new_candidates_merge(D, t, q,q_prev, Q, Q_prev_list, A, S, params, pdfa):
    candidates = np.unique(D[q.hist[0], t, :], axis=0)  #t or t-1?
    for i in range(candidates.shape[0]):
        X, S , n , f = get_suffixes(D, candidates[i, :], q, t, S, params)
        trajs = np.where(np.all(D[:, t, :] == candidates[i, :], axis=1))
        trajs = remove_nc(trajs, q.hist[0])
        q_new = State('q' + pdfa.get_count(), X, A, candidates[i, :],n, trajs)
        q_new.X2 = f
        if not q_new.X2:
            pdfa.add_transition(q_prev, get_a(q_new), pdfa.end_state, get_o(q_new), get_r(q_new))
            return Q, Q_prev_list, S
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
                        n=q.n
            else:
                if Q[i].n > n:
                    t = i
                    state = Q[i]
                    n=q.n

    return state, t


def remove_candidate_from_Q(Q, Q_prev_list, q, t):
    ind = Q[t].index(q)
    del Q_prev_list[t][ind]
    # q_prev = get_prev_state(q, t, Q, Q_prev_list)
    # Q_prev_list[t].remove(q_prev)
    Q[t].remove(q)
    return Q, Q_prev_list

def get_prev_state(q,t,Q, Q_prev_list):
    ind = Q[t].index(q)
    q_prev =Q_prev_list[t][ind]
    return q_prev



def add_state_to_Q_final(Q_final, Q, t, q, pdfa, Q_prev_list):
    #print("Addidin state to Q_final, t=", t)
    Q_final[t + 1].append(q)
    pdfa.add_transition(Q_prev_list[t][Q[t].index(q)], get_a(q), q, get_o(q), get_r(q))
    return Q_final


def get_similar_states(q_max, t_max, Q_final, params, S):
    similar = []
    for t in range(0, t_max+2):
        if Q_final[t]:
            for q in Q_final[t]:
                sim, threshold, v = test_distinct(q_max, q, params, S)
                if sim:
                    similar.append(q)
                    print("similar here ", q_max.name, q.name, threshold, v)
    return similar


def merge(q1, q2, q_prev, pdfa):
    if (not q2.X2) and q1.X2:
        pdfa.add_transition(q_prev,  get_a(q2), pdfa.end_state, get_o(q2), get_r(q2))
        return q1
        #print("after", pdfa.transitions)

    q1 = merge_history(q1, q2)
    if q_prev == q1:
        pdfa.add_transition(q1, get_a(q2), q1, get_o(q2), get_r(q2))


    else:
        # first argument is q2, second argument is the state you want to know about
        if (q_prev.name == 'q1' and q1.name == 'q2') or (q_prev.name == 'q2' and q1.name == 'q1'):
            # print("q1 = ", q1.name, " q2= ", q2.name, " q_prev= ", q_prev.name)
            # print("Here is the issue, to be merged is ", q2.name, q2.c, q2.X)
            # print("merged with ", q1.name, q1.c, q1.X)
            if not set(q2.hist[0]) <= set(q_prev.hist[0]):
                print("IMPROPER subset")
                brek
            # check if there's already intersection between q_prev and the one q2 is being compared with
            # print("INTERSECTION: ", list(set(q_prev.hist[0]).intersection(q1.hist[0])))
            # brek
        pdfa.add_transition(q_prev, get_a(q2), q1, get_o(q2), get_r(q2))
    return q1


def printn(s, Q):
    print(s)
    for i in range(len(Q)):
        if Q[i]:
            print("t: ", i)
            for q in Q[i]:
                print(q.name, q.c)

def check_hist(s, Q, Q_prev):
    print(s)
    for i in range(len(Q)):
        for j in range(len(Q[i])):
            if not set(Q[i][j].hist[0]) <= set(Q_prev[i][j].hist[0]):
                print(Q[i][j].hist[0], Q_prev[i][j].hist[0])
                brek