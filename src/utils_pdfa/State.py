

class State:
    def __init__(self, s, t, n,A, h=None):
        self.name = s
        self.X = t
        self.n = n
        self.V=0
        self.A =[0] * A
        self.VA = [0]*A
        if not h:
            self.hist = []
        else:
            self.hist = h
