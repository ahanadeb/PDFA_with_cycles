def get_a(q):
    return q.c[0]


def get_o(q):
    if len(q.c) > 1:
        return q.c[1]
    else:
        obs= ' '
        return obs


def get_r(q):
    if len(q.c) > 1:
        return q.c[2]
    return 0
