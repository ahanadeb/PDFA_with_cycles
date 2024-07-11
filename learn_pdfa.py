import time
from src.pdfa import PDFA
from src.utils_pdfa.adact_utils import *
from src.utils_pdfa.State import State

def get_obs(q):
    return str(int(q[1]))#[1:]#+","+str(q[2])
def get_obs_o(q):
    return str(int(q[0]))#[1:]
def get_r(q):
    return str(q[2])


def learn_pdfa(K,H,D,first_obs, params, a_dict1,a_dict, A):
    start = time.time()
    # initialise empty automata
    pdfa = PDFA(D, A, a_dict)


    # ADACT-H
    q = pdfa.initial_state
    trajs = list(range(K + 1))
    q.hist = trajs

    Q_t = []

    for h in range(H+1):
        # list of all strings observed at step h (for similarity comparison in CMS)
        d = D[:, h, :]
        q_prev_list = []
        if h > 0:
            # previous candidates are in Q_t
            candidates, q_prev_list = get_candidates2(Q_t, d)

            q_max, trajs, q_prev, r = get_argmax(Q_t, h, D)
            X= get_suffixes(D, q_max,q_prev, h)
            q_s = State('q' + pdfa.get_count(), X, 0, A, trajs)
            # promote
            pdfa.add_state(q_s)
            # add transition
            pdfa.add_transition(q_prev, a_dict1[q_max[0]], q_s, get_obs(q_max), q_max[2])
            #remove candidate
            candidates, q_prev_list = remove_candidate(candidates, q_max, q_prev_list, q_prev)



        else:
            q_prev_list.append(pdfa.initial_state)
            #get candidates
            candidates = get_first_obs(first_obs)
            #get max first o
            q_max, trajs, r = get_max_o(first_obs) #q_max is a single observation
            #get suffixes
            X = get_first_suffixes(D,first_obs,q_max)
            q_s = State('q'+ pdfa.get_count(), X, 0, A, trajs)
            #promote
            pdfa.add_state(q_s)
            pdfa.add_transition(q, get_obs_o(q_max) , q_s, " ", 0)
            #remove candidate
            candidates = remove_candidate_first(candidates, q_max)

            q_prev_list.append(pdfa.initial_state)


        # reset current Q list before first promotion
        Q_t = []
        Q_t.append(q_s)

        for i in range(candidates.shape[0]):
            q_c = candidates[i, :]
            # get previous q
            if h == 0:
                r = 0
                X1 = get_first_suffixes(D, first_obs, q_c)
                trajs = np.where(np.all(first_obs == q_c, axis=1))
                q_prev = pdfa.initial_state
            else:

                q_prev = q_prev_list[i]

                X1= get_suffixes(D, q_c,q_prev, h)
                trajs = np.where(np.all(D[:, h, :] == q_c, axis=1))  # get indexes
                trajs = remove_nc(trajs, q_prev.hist)

            # TESTDISTINCT
            for Q in Q_t:
                Q_tocheck = State('q' + pdfa.get_count(), X1, 0, A, trajs)

                #check intersection
                #if len(np.intersect1d(Q_tocheck.hist[0],Q.hist[0]))>0:


                similar, threshold, v = test_distinct(Q_tocheck, Q)

                if similar:
                    #print("h: ",h, "merge occurs between: ", Q.name, "and ", Q_tocheck.name)
                    # merges cms tables
                    #Q.X.merge(Q_tocheck.X)
                    # merge history
                    Q = merge_history(Q, Q_tocheck)
                    if h==0:
                        pdfa.add_transition(q_prev, get_obs_o(q_c), Q, " ", 0)
                        print(pdfa.transitions)

                    else:

                        pdfa.add_transition(q_prev, a_dict1[q_c[0]], Q, get_obs(q_c), q_c[2], True)
                    break
                else:
                    #print("dissimilar: ", Q.name, Q_tocheck.name, " thres: ", threshold, " value: ", v)
                    # promote candidate
                    if Q == Q_t[-1]:  #if you've checked all other Q options
                        #print("h: ",h, "promoting: ", Q_tocheck.name)
                        # promote
                        pdfa.add_state(Q_tocheck)
                        # add transition
                        if h==0:
                            pdfa.add_transition(q_prev, get_obs_o(q_c) , Q_tocheck, " ", 0)

                        else:

                            pdfa.add_transition(q_prev, a_dict1[q_c[0]], Q_tocheck, get_obs(q_c), q_c[2])
                        Q_t.append(Q_tocheck)

    end = time.time()
    ti = end-start
    # print("TOTAL TIME ", end - start, ", no of states: ", len(pdfa.states))
    #brek
    # for s in pdfa.states:
    #     np.set_printoptions(suppress=True)
    #     print(s.name, s.hist)



    return pdfa, ti, len(pdfa.states)

