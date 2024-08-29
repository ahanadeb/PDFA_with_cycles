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
        traj = ''
        for j in range(0, d_new.shape[1]):
            for p in range(0, d_new.shape[2]):
                traj = traj + str(d_new[i, j, p])
            if len(traj) <= params.k:
                if n < len(traj):
                    n = len(traj)
                cms.add(traj)
                f.append(traj)
                if traj != '':
                    if traj not in S:
                        S.append(traj)
            else:
                return cms, S, n, f
    return cms, S, n, f


def test_distinct(Q1, Q2, params, S):
    # Test similarity between candidates and safe state
   # print("S", S)
    if not S:
        return True, 0, 0
    # each X is a cms
    v1 = []
    v2 = []
    S.sort(key=len)

    thres = np.sqrt(.5 * np.log(2.04 / params.alpha)) * (1 / np.sqrt(Q1.n) + 1 / np.sqrt(Q2.n))
    for s in S:
        if len(s) < min(Q1.max_traj, Q2.max_traj):
            # get upperbounds on how many times s occurs in X
            c1 = Q1.X.query(s)
            c2 = Q2.X.query(s)
            if np.abs(c1 / Q1.n - c2 / Q2.n) > thres:
                print("NOT SIMILAR ", Q1.name, Q2.name,np.abs(c1 / Q1.n - c2 / Q2.n), thres )
                print( Q1.X2)
                print( Q2.X2)
                return False, thres, np.abs(c1 / Q1.n - c2 / Q2.n)

            v1.append(c1 / Q1.n)
            v2.append(c2 / Q2.n)

    return True, thres, np.abs(c1 / Q1.n - c2 / Q2.n)

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))



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
        traj = ''
        for j in range(1, d_new.shape[1]):
            for t in range(0, d_new.shape[2]):
                traj = traj + str(d_new[i, j, t])
            if len(traj) <= params.k:
                if n<len(traj):
                    n = len(traj)
                cms.add(traj)
                f.append(traj)
                if traj not in S:
                    S.append(traj)
            else:
                return cms, S, n, f
    return cms, S, n, f


def remove_candidate_first(candidates, r):
    pos = np.where(np.all(candidates == r, axis=1))
    c = np.delete(candidates, pos[0], axis=0)
    return c


def get_first_obs(first_obs):
    unq, cnt = np.unique(first_obs, axis=0, return_counts=True)
    return unq


def remove_nc(trajs, hist):
    xy = np.intersect1d(trajs, hist, return_indices=False)
    return (np.array(xy),)


#CHANGE THIS FOR OTHER DOMAINS
def get_suffixes_q0(q0, params, K, H):
    cms = CountMinSketch(params.m, params.d)
    for i in range(q0.X.shape[0]):
        l = ''
        for j in range(q0.X.shape[1]):
            l= l + str('9')#str(q0.X[i, j, 0]) + str(q0.X[i, j, 1]) + str(q0.X[i, j, 2])
        cms.add(l)

    q0.X = cms
    q0.hist = (np.array(list(range(K + 1))),)
    q0.n = K
    q0.max_traj = H
    return q0
