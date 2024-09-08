class State:
    def __init__(self, s, t, A, c,n, h=None):
        self.name = s
        self.X = t
        self.V = 0
        self.A = [0] * A
        self.VA = [0] * A
        self.c = c
        if not h:
            self.hist = []
            self.n = 0 #number of times the state is visited
        else:
            self.hist = h
            self.n = len(self.hist[0])
        self.max_traj = n
        self.X2 = []
        self.final_state = False