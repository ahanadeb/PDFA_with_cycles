import numpy as np
from numpy.linalg import norm


def get_suffixes(D, q, q_prev, h):
    d1 = D[:, h, :]
    a = np.where(np.all(d1 == q, axis=1))
    a = remove_nc(a, q_prev.hist)
    d_new = (D[:, h+1:, :]).astype(int)
    d_new2 = d_new[a[0], :, :]
    d_new2 = d_new2.reshape((d_new2.shape[0] * d_new2.shape[1], d_new2.shape[2]))
    fr = np.unique(d_new2, axis=0)
    l = []
    for r in range(fr.shape[0]):
        l.append(str(fr[r, 0]) + str(fr[r, 1]) + str(fr[r, 2]))
    return l


def test_distinct(Q1, Q2):
    # Test similarity between candidates and safe state
    # for basic domain just check next action observation
    if Q1.name == 'q0' or Q2.name == 'q0':
        return False, 0, 0
    print("comparing ", Q1.name, Q2.name)
    print("suffixes ", Q1.X, Q2.X)
    # if (not Q1.X and Q2.X) or (not Q2.X and Q1.X):
    #     return False, 0, 0
    #S1 = Q1.X +Q2.X+ list(set(Q1.X) - set(Q2.X))
    S = Q1.X + list(set(Q2.X) - set(Q1.X))
    print("S", S)
    if not S:
        return True, 0, 0
    for s in S:
        if (s in Q1.X and s not in Q2.X) or (s in Q2.X and s not in Q1.X):
            return False, 0, 0
    return True, 0, 0
    # if (not Q1.X and Q2.X) or (not Q2.X and Q1.X):
    #     return True, 0, 0
    # if set(Q1.X) <= set(Q2.X) or set(Q1.X) <= set(Q2.X):
    #     print("same")
    #     return True, 0, 0
    # else:
    #     print("different")
    #     return False, 0, 0


# def cosine_similarity(a, b):
#     return np.dot(a, b) / (norm(a) * norm(b))


def merge_history(q1, q2):
    new_hist = np.unique(np.concatenate((q1.hist[0], q2.hist[0]), 0))
    q1.hist = []
    q1.hist.append(new_hist)
    return q1


def get_first_suffixes(D, O, q):
    a = np.where(np.all(O == q, axis=1))
    d_new2 = D[a[0], 0:, :].astype(int)
    d_new2 = d_new2.reshape((d_new2.shape[0] * d_new2.shape[1], d_new2.shape[2]))
    fr = np.unique(d_new2, axis=0)
    l = []
    for r in range(fr.shape[0]):
        l.append(str(fr[r, 0]) + str(fr[r, 1]) + str(fr[r, 2]))
    return l


def get_first_obs(first_obs):
    unq, cnt = np.unique(first_obs, axis=0, return_counts=True)
    return unq


def remove_nc(trajs, hist):
    xy = np.intersect1d(trajs, hist, return_indices=False)
    return (np.array(xy),)


def get_suffixes_q0(q0):
    q0.X = ['0']
    return q0
