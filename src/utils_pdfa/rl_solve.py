import numpy as np
from env.basic_domain import get_reward
#get mdp from pdfa

def solve_mdp(pdfa, a_dict, gamma =0.9):
    for i in range(2):

        for s in pdfa.states:

            #get connected states
            if s.name in pdfa.transitions:

                for a in pdfa.transitions[s.name]:

                    for q in pdfa.transitions[s.name][a]:

                        q_state = get_state_from_name(q, pdfa)
                        if a in a_dict:
                            s.VA[a_dict[a]] = s.A[a_dict[a]] + gamma*max(q_state.VA)


    return pdfa

def get_optimal_policy(pdfa,a_dict1):
    for q in pdfa.states:
        if q!=pdfa.initial_state:
            pdfa.policy[q.name]= a_dict1[(q.VA).index(max(q.VA))]

    return pdfa



def get_state_from_name(s, pdfa):
    for q in pdfa.states:
        if q.name ==s:
            return q
    raise ValueError('Incorrect state query, '+ s+ " not present in pdfa.")


def get_V_max(pdfa):
    V_max = -1000
    for q in pdfa.states:
        if q.V >= V_max:
            V_max=q.V#.copy()
    return V_max


