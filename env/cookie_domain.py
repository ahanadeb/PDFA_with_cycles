import random
class Cookie():
    def __init__(self):
        self.O =['r', 'b', 'g', 'w', 'rB', 'bC', 'gC']
        self.A = ['pB', 'up', 'dw', 'left', 'right']
        self.R = [0, 1]
        self.initial_states= [1,2,3,4]
        self.current_state = 2
        self.state = {'button': False, 'cookie': False}
        self.actions = {1:['right', 'eat'], 2:['right', 'left','up'],3:['left', 'eat'], 4: ['press', 'down']}
        self.colors = {1: 'blue', 2:'white', 3:'green', 4:'red'}

    def get_action(self):
        actions = self.actions[self.current_state]
        if self.state['button']==True:
            if 'press' in actions:
                actions.remove('press')
        if self.state['cookie']==False or self.state['cookie']!=self.current_state:
            if 'eat' in actions:
                actions.remove('eat')
        # if self.state['cookie'] == self.current_state:
        #     actions  = ['eat']
        if self.current_state == 4 and self.state['button']==False:
            actions = ['press']
        if self.current_state == 4 and self.state['button']==True:
            actions = ['down']

        return actions

    def do_action(self):
        actions = self.get_action()
        a = random.choice(actions)
        r = 0
        if a == 'right':
            if self.current_state ==1:
                o='white'
                self.current_state = 2
                return a , o , r
            else:
                o = 'green'
                if self.state['cookie'] == 3:
                    o = o + " cookie"
                self.current_state = 3
                return a , o , r
        if a == 'left':
            if self.current_state ==3:
                o='white'
                self.current_state = 2
                return a , o, r
            else:
                o = 'blue'
                if self.state['cookie'] == 1:
                    o = o + " cookie"
                self.current_state = 1
                return a , o , r

        if a == 'up':
            o = 'red'
            self.current_state = 4
            return a, o , r
        if a == 'down':
            o = 'white'
            self.current_state = 2
            return a, o , r
        if a == 'eat':
            o = self.colors[self.current_state]
            self.state['cookie']=False
            self.state['button']=False
            r = 1
            return a , o , r
        if a == 'press':
            self.state['button'] = True
            if random.uniform(0, 1) > 0.5:
                self.state['cookie']=1
                #print("cookie set at 1")
            else:
                self.state['cookie'] = 3
                #print("cookie set at 3")
            o = self.colors[self.current_state]
            return a , o, r









