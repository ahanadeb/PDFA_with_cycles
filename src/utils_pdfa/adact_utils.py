import numpy as np
from numpy.linalg import norm



def get_suffixes(D, q, q_prev, h):
    d1 = D[:, h, :]
    a = np.where(np.all(d1 == q, axis=1))
    a = remove_nc(a, q_prev.hist)
    d_new = (D[:, h:, :]).astype(int)
    d_new2 = d_new[a[0], 1, :]
    fr = np.unique(d_new2, axis=0)
    l = []
    for r in range(fr.shape[0]):
        l.append(str(fr[r, 0]) + str(fr[r, 1])+ str(fr[r, 3]) + str(fr[r, 4]))
    return l


def test_distinct(Q1, Q2):
    # Test similarity between candidates and safe state
    # for basic domain just check next action observation
    print("comparing ", Q1.name, Q2.name)
    print("suffixes ", Q1.X, Q2.X)
    # if Q1.X==Q2.X:
    if set(Q1.X) <= set(Q2.X) or set(Q1.X) <= set(Q2.X):
        print("same")
        return True, 0, 0
    else:
        print("different")
        return False, 0, 0

# def cosine_similarity(a, b):
#     return np.dot(a, b) / (norm(a) * norm(b))



def merge_history(q1, q2):
    new_hist = np.unique(np.concatenate((q1.hist[0], q2.hist[0]), 0))
    q1.hist = []
    q1.hist.append(new_hist)
    return q1



def get_first_suffixes(D, O, q):
    a = np.where(np.all(O == q, axis=1))
    d_new2 = D[a[0], 0, :].astype(int)
    # d_new2 = d_new2.reshape((d_new2.shape[0], d_new2.shape[2]))
    fr = np.unique(d_new2, axis=0)
    l = []
    for r in range(fr.shape[0]):
        l.append(str(fr[r, 0]) + str(fr[r, 1])+ str(fr[r, 3]) + str(fr[r, 4]))
    return l



def get_first_obs(first_obs):
    unq, cnt = np.unique(first_obs, axis=0, return_counts=True)
    return unq


def remove_nc(trajs, hist):
    xy = np.intersect1d(trajs, hist, return_indices=False)
    return (np.array(xy),)


def get_suffixes_q0(q0):
    l = []
    for i in range(q0.X.shape[0]):
        for j in range(q0.X.shape[1]):
            l.append(str(q0.X[i, j, 0]) + str(q0.X[i, j, 1]) + str(q0.X[i, j, 2]))
    q0.X = ['0']
    return q0
