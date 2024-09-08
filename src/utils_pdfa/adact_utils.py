import numpy as np
from numpy.linalg import norm
from countminsketch import CountMinSketch


def get_suffixes(D, q, q_prev, h, S, params):
    hist = q_prev.hist
    f=[]
    n=0
    cms = CountMinSketch(params.m, params.d)
    d1 = D[:, h, :]
    a = np.where(np.all(d1 == q, axis=1))
    a = remove_nc(a, hist)
    d_new = (D[:, h + 1:, :]).astype(int)
    for i in a[0]:
        # single trajectory of shape hx2
        # make it into single string

        for j in range(0, d_new.shape[1]):
            traj = ''
            for p in range(0, d_new.shape[2]):
                traj = traj + str(d_new[i, j, p])
            #print(traj, params.k)

            if len(traj) <= params.k:

                if n < len(traj):
                    n = len(traj)
                #print("Dvwdvws", traj)

                if traj != '':
                    cms.add(traj)
                    if traj not in f:

                        f.append(traj)
                    if traj not in S:
                        S.append(traj)
            # else:
            #     return cms, S, n, f
    return cms, S, n, f



def test_distinct(Q1, Q2, params, S):
    # Test similarity between candidates and safe state
    print("S", S)
    print("comparing, ", Q1.name, Q2.name, Q1.X2, Q2.X2)

    if Q1.name == 'q0' or Q2.name == 'q0':
        return False, 0,0
    if not S:
        return True, 0, 0

    # each X is a cms
    v1 = []
    v2 = []
    S.sort(key=len)

    thres = np.sqrt(.5 * np.log(2.04 / params.alpha)) * (1 / np.sqrt(Q1.n) + 1 / np.sqrt(Q2.n))
    print(Q1.max_traj, Q2.max_traj)

    for s in S:
        print("erg")

        #print("s", s, len(s),Q1.max_traj ,Q2.max_traj)
        if min(Q1.max_traj, Q2.max_traj) == 0:
            return True, 0, 0

        if len(s) < min(Q1.max_traj, Q2.max_traj):
            print("13qfwe")

            # get upperbounds on how many times s occurs in X
            c1 = Q1.X.query(s)
            c2 = Q2.X.query(s)
            print("ververerehere",s, c1, c2, Q1.n, Q2.n)
            #print(Q1.name, Q1.hist)
            print(np.abs(c1 / Q1.n - c2 / Q2.n))
            print(thres)



            if np.abs(c1 / Q1.n - c2 / Q2.n) > thres:
                print("NOT SIMILAR ", Q1.name, Q2.name,np.abs(c1 / Q1.n - c2 / Q2.n), thres)
                #brek
                print( Q1.X2)
                print( Q2.X2)

                return False, thres, np.abs(c1 / Q1.n - c2 / Q2.n)

            v1.append(c1 / Q1.n)
            v2.append(c2 / Q2.n)
    return True, thres, 0
    #return True, thres, np.abs(c1 / Q1.n - c2 / Q2.n)


# def cosine_similarity(a, b):
#     return np.dot(a, b) / (norm(a) * norm(b))


def merge_history(q1, q2):
    new_hist = np.unique(np.concatenate((q1.hist[0], q2.hist[0]), 0))
    q1.hist = []
    q1.hist.append(new_hist)
    return q1


def get_first_suffixes(D, O, q, S, params):
    # n is used to keep track of the max_trajectory length
    n= 0
    f= []
    cms = CountMinSketch(params.m, params.d)
    d_new = (D[:, 0:, :]).astype(int)
    a = np.where(np.all(O == q, axis=1))
    for i in a[0]:

        for j in range(0, d_new.shape[1]):
            traj = ''
            for t in range(0, d_new.shape[2]):
                traj = traj + str(d_new[i, j, t])
            if len(traj) <= params.k:
                if n<len(traj):
                    n = len(traj)
                if traj != '':
                    cms.add(traj)
                    if traj not in f:
                        f.append(traj)
                    if traj not in S:
                        S.append(traj)
            else:
                return cms, S, n, f

    return cms, S, n, f


def get_first_obs(first_obs):
    unq, cnt = np.unique(first_obs, axis=0, return_counts=True)
    return unq


def remove_nc(trajs, hist):
    xy = np.intersect1d(trajs, hist, return_indices=False)
    return (np.array(xy),)


def get_suffixes_q0(q0, params, K, H):
    cms = CountMinSketch(params.m, params.d)
    n=0
    for i in range(q0.X.shape[0]):
        l = ''
        for j in range(q0.X.shape[1]):
            l= l +str(9)
        cms.add(l)
        if n<len(l):
            n = len(l)

    q0.X = cms
    q0.hist = (np.array(list(range(K + 1))),)
    q0.n = K
    q0.max_traj = n
    return q0
