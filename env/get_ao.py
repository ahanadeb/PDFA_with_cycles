def get_a(q):
    return q.c[0]


def get_o(q):
    if len(q.c) > 3:
        return str(q.c[1]) + "," + str(q.c[2]) + "," + str(q.c[3])
    else:
        return str(q.c[0]) + "," + str(q.c[1]) + "," + str(q.c[2])


def get_r(q):
    if len(q.c) > 4:
        return q.c[4]
    return 0
