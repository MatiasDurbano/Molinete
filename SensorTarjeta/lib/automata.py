def accepts(transitions, initial, accept, stream):
    state = initial
    for symbol in stream:
        try:
            state = transitions[state][symbol]
        except KeyError:
            return False #Esto me parece una chanchada

    return state in accept

def accepts_left(stream):
    dfa_left = {
        's0':{(0,1):'s1'},
        's1':{(1,1):'s2', 's1':(0,0), (1,0):'s3', (0,1):'s1'},
        's2':{(1,0):'s3', (1,1):'s2'},
        's3':{(1,0):'s3'},
    }

    accept_state = ['s3']
    init_state = 's0'

    return accepts(dfa_left, init_state, accept_state, stream)

def accepts_right(stream):
    dfa_right = {
        's0':{(1,0):'s1'},
        's1':{(1,1):'s2', 's1':(0,0), (0,1):'s3', (1,0):'s1'},
        's2':{(0,1):'s3', (1,1):'s2'},
        's3':{(0,1):'s3'},
    }

    accept_state = ['s3']
    init_state = 's0'

    return accepts(dfa_right, init_state, accept_state, stream)
