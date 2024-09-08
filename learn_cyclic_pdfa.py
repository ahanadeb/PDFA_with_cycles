from src.pdfa import PDFA
from src.utils_pdfa.adact_utils import *

from src.utils_pdfa.cyclic_utils import *


def learn_cyclic_pdfa(D, first_obs, A, a_dict,params, K, H):
    S = []
    Q = [None] * (H + 1)  # list of lists for all candidates
    Q_final = [None] * (H + 2)  # list of lists for final safe states
    Q_prev_list = [None] * (H + 1)
    Q_prev_list = initialise_Q(Q_prev_list, H + 1)
    Q = initialise_Q(Q, H + 1)
    Q_final = initialise_Q(Q_final, H + 2)
    # add initial pdfa state
    pdfa = PDFA(D, A, a_dict)
    q0 = pdfa.initial_state
    q0 = get_suffixes_q0(q0,params, K, H)
    Q_final[0].append(q0)
    # add first list of candidates
    Q, Q_prev_list, S = get_initial_candidates(D, first_obs, A, pdfa, Q, Q_prev_list, S, params)
    # after this Q_c becomes the list of all candidates
    while not_empty(Q):
        q_max, t_max = get_max_qao(Q)
        similar = get_similar_states(q_max, t_max, Q_final,params, S)
        # promote if no similar
        if not similar:
            print("not similar, removing ", q_max.name)
            Q_final = add_state_to_Q_final(Q_final, Q, t_max, q_max, pdfa, Q_prev_list)
            # printn("Q_final", Q_final)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            # add new candidates stemming from this state
            Q, Q_prev_list, S = add_new_candidates(D, t_max, q_max, Q, Q_prev_list, A,  S, params, pdfa)
            print("HERE1")
            printn("Q_prev_list", Q_prev_list)
            printn("Q", Q)

            #print("added candidates ", Q)
        else:

            print("merging ", similar[0].name, q_max.name)
            # merge candidates
            q_prev= get_prev_state(q_max, t_max, Q, Q_prev_list)
            similar[0]= merge(similar[0], q_max,q_prev, pdfa)
            Q, Q_prev_list = remove_candidate_from_Q(Q, Q_prev_list, q_max, t_max)
            if t_max!=H:
                #HERE while adding you've to add the q_prev of q_max to the prev list. not current q_max
                Q, Q_prev_list, S = add_new_candidates_merge(D, t_max, q_max,q_prev, Q, Q_prev_list, A, S, params, pdfa)
                print("HERE2")
                printn("Q_prev_list", Q_prev_list)
                printn("Q", Q)
            printn("Q_prev_list", Q_prev_list)
            printn("Q", Q)



    return pdfa