import numpy as np

from src.pdfa_learning.pdfa.base import PDFA
from src.pdfa_learning.pdfa.base import FINAL_STATE
from src.pdfa_learning.pdfa.helpers import FINAL_SYMBOL
from src.pdfa_learning.pdfa.render import to_graphviz
from src.pdfa_o import pdfa_o
from src.utils_pdfa.utils import *
from src.utils_pdfa.State import State
def make_pdfa_two_state(p1, p2):
    """Make a PDFA with two states, for testing purposes."""
    automaton = PDFA(
        3,
        2,
        {
            0: {
                0: (1, p1),
                1: (2, 1 - p1),
            },
            1: {
                0: (2, 1 - p2),
                1: (1, p2),
            },
            2: {FINAL_SYMBOL: (FINAL_STATE, 1.0)},
        },
    )
    return automaton


p1 = 0.2
p2 = 0.3
a=make_pdfa_two_state(p1,p2)
print(a)
#to_graphviz(a).render("/Users/ahanadeb/Documents/books/RL/PhD/bisimulation/countminsketch/graphs/img_o")




D=np.zeros((3,4))
a = pdfa_o(D)
print(a.transitions)
t=np.zeros((2,0))
q0=State('q0',t,0 )
q1=State('q1',t,3 )
q2=State('q2',t ,5)
a.add_transition(q0,'0',q1, 0.9)
a.add_transition(q0,'0',q1, 0.6)
a.add_transition(q1,'1',q0, 0.4)
print(a.transitions)
a.add_transition(q0,'0',q2, 0.1)
print(a.transitions)
a.add_transition(q1,'0',q2, 0.3)
print(a.transitions)




gr = render_o(a)
gr.render("/Users/ahanadeb/Documents/books/RL/PhD/bisimulation/countminsketch/graphs/img_33")



