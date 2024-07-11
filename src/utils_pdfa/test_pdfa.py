from env.t_maze import Tmaze


def test_pdfa(pdfa, K, H):
    pdfa.policy['q0'] = 'E'
    tmaze = Tmaze(H - 1)
    R = 0
    for k in range(K):
        o1, g = tmaze.initialise()
        s = [0, 0]
        q = 'q1'
        for h in range(H):
            a = pdfa.policy[q]
            s, o, r = tmaze.get_next_state(a, s)
            R= R+r
            if s[1] == 1:
                o = o1
            #print('q', q, 'action', a, "obs: ", o, "reward: ", r)
            if q == 'q0':
                q = 'q1'
            else:
                for q_n in pdfa.transitions[q][a]:
                    for oc in pdfa.transitions[q][a][q_n]:
                        if int(oc) == int(o):
                            new_q = q_n
                q = new_q
    print("Average reward: ", R/K )
