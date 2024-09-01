from src.utils_pdfa.State import State


class PDFA:
    def __init__(self, D, A, a_dict):
        self.transitions = {}
        self.states = []
        self.c_states = []
        self.initial_state = State('q0', D, A, 0, None)  #s, t,A,c, h=None):
        self.states.append(self.initial_state)
        self.D = D
        self.count = 1
        self.a_dict = a_dict
        self.policy = {}
        self.end_state = State('q', [], A, 0, None)

    def add_state(self, s):
        if self.check_existence_states(s):
            raise ValueError("Naming isse, state already present in pdfa.")
        else:
            self.states.append(s)
            self.count = self.count + 1

    def add_transition(self, s, a, s1, p, r, merge=False):
        if s != self.initial_state:
            #s.A[self.a_dict[a]] = r

            # if s1 not in self.states:
            s.A[a] = r


        if check_existence(s.name, self.transitions):
            # add
            if check_existence(a, self.transitions[s.name]):
                # replaces p
                if not check_existence(s1.name, self.transitions[s.name][a]):
                    self.transitions[s.name][a].update({s1.name: []})
            else:
                self.transitions[s.name].update({a: {s1.name: []}})
        else:
            self.transitions.update({s.name: {a: {s1.name: []}}})

        if p not in self.transitions[s.name][a][s1.name]:
            self.transitions[s.name][a][s1.name].append(p)
        if not merge:
            if not self.check_existence_states(s1):
                self.add_state(s1)
            if not self.check_existence_states(s):
                self.add_state(s)

    def merge_transition(self, s1, s2):
        for s in self.states:

            if check_existence(s.name, self.transitions):
                for a in self.transitions[s.name]:

                    if check_existence(s2.name, self.transitions[s.name][a]):
                        self.transitions[s.name][a] = {s1.name: self.transitions[s.name][a][s2.name]}

    def check_existence_states(self, s):
        for i in self.states:
            if i.name == s.name:
                return True
        return False

    def get_count(self):
        r = str(self.count)
        self.count = self.count + 1
        return r


def check_existence(key, dic):
    if key in dic:
        return True
    return False
