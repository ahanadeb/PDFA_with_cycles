import numpy as np
from numpy.linalg import norm

def remove_candidate(candidates, r, q_prev_list, q_prev):
    pos = np.where(np.all(candidates == r, axis=1))
    pos = pos[0].tolist()
    if len(q_prev_list) > 1:
        pos2 = np.array([i for i, x in enumerate(q_prev_list) if x == q_prev])
    diff = list(set(pos) - set(list(set(pos) - set(pos2))))
    nc = np.delete(candidates, np.array(diff), 0)
    q_prev_list2 = q_prev_list
    if len(diff) > 0:
        for index in sorted(diff, reverse=True):
            del q_prev_list2[index]
    return nc, q_prev_list2



def get_suffixes(D, q,q_prev, h):
    d1 = D[:, h, :]
    a = np.where(np.all(d1 == q, axis=1))
    a = remove_nc(a, q_prev.hist)
    d_new = (D[:, h:, :]).astype(int)
    d_new2 = d_new[a[0],0,:]
    # print(d_new2.shape)
    # brek
    # d_new2 = d_new2.reshape((d_new2.shape[0] * d_new2.shape[1], d_new2.shape[2]))
    fr = np.unique(d_new2, axis=0)
    l=[]
    for r in range(fr.shape[0]):
        l.append(str(fr[r,0])+str(fr[r,1])+str(fr[r,2]))
    return l


def test_distinct(Q1, Q2):
    # Test similarity between candidates and safe state
    #for basic domain just check next action observation
    print("comparing ", Q1.name, Q2.name)
    print("suffixes ", Q1.X, Q2.X)
    #if Q1.X==Q2.X:
    if set(Q1.X) <= set(Q2.X) or set(Q1.X) <= set(Q2.X):
        return True, 0, 0
    else:
        return False, 0, 0
    # S = Q1.X + list(set(Q1.X) - set(Q2.X))
    # if not S:
    #     return True, 0, 0
    # for s in S:
    #     if (s in Q1.X and s not in Q2.X) or (s in Q2.X and s not in Q1.X):
    #         return False, 0, 0
    #return True, 0, 0


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def get_argmax(Q_t, h, D):
    max_count1 = 0
    trajs = []
    for q in Q_t:
        d = D[q.hist[0], h, :]
        unq, cnt = np.unique(d, axis=0, return_counts=True)
        count = max(cnt)
        q_check = unq[np.argmax(cnt),:]

        if count >= max_count1:
            max_count1 = count
            q_max = q_check
            trajs = np.where(np.all(D[q.hist[0], h, :] == q_check, axis=1))
            q_prev = q
    return q_max, trajs, q_prev, 0


def merge_history(q1, q2):
    new_hist = np.unique(np.concatenate((q1.hist[0], q2.hist[0]), 0))
    q1.hist = []
    q1.hist.append(new_hist)
    return q1


def get_candidates2(Q_t, d):
    final_c = np.zeros((d.shape[0],3))
    k=0
    q_encountered=[]
    hist=[]
    for q in Q_t:
        if len(q_encountered)>0:
            if q not in q_encountered:
                x = np.unique(d[q.hist[0], :], axis=0)
                final_c[k:k+x.shape[0], :] = x
                k = k + x.shape[0]
                q_encountered += ([q] * x.shape[0])
                hist = hist + q.hist
        else:
            x = np.unique(d[q.hist[0], :], axis=0)
            final_c[k:k+x.shape[0], :] = x
            k = k + x.shape[0]
            q_encountered += ([q] * x.shape[0])

    final_c = final_c[0:k, :]

    return final_c, q_encountered


def get_max_o(O):
    unq, cnt = np.unique(O, axis=0, return_counts=True)
    q_max = unq[np.argmax(cnt), :]
    trajs = np.where(np.all(O == q_max, axis=1))
    return q_max, trajs, 0


def get_first_suffixes(D, O, q):

    a = np.where(np.all(O == q, axis=1))
    d_new2 = D[a[0], 0:, :].astype(int)
    d_new2 = d_new2.reshape((d_new2.shape[0] * d_new2.shape[1], d_new2.shape[2]))
    fr = np.unique(d_new2, axis=0)
    l = []
    for r in range(fr.shape[0]):
        l.append(str(fr[r, 0]) + str(fr[r, 1]) + str(fr[r, 2]))
        return l


def remove_candidate_first(candidates, r):
    pos= np.where(np.all(candidates == r, axis=1))
    c=np.delete(candidates, pos[0], axis=0)
    return c


def get_first_obs(first_obs):
    unq, cnt = np.unique(first_obs, axis=0, return_counts=True)
    return unq

def remove_nc(trajs, hist):
    xy= np.intersect1d(trajs, hist, return_indices=False)
    return (np.array(xy),)

def get_suffixes_q0(q0):
    l=[]
    for i in range(q0.X.shape[0]):
        for j in range(q0.X.shape[1]):
            l.append(str(q0.X[i,j,0])+str(q0.X[i,j,1])+str(q0.X[i,j,2]))
    q0.X = ['0']
    return q0