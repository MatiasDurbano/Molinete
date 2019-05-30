import unittest
from automata import accepts

class AutomataTest(unittest.TestCase):

    def test_accepts(self):
        dfa_left = {
            's0':{(0,1):'s1'},
            's1':{(1,1):'s2', (1,0):'s3', (0,1):'s1'},
            's2':{(1,0):'s3', (1,1):'s2'},
            's3':{(1,0):'s3'},
        }

        accept_state = ['s3']
        init_state = 's0'

        stream = [(0,1), (0,1), (0,1), (0,1), (1,1), (1,1), (1,1), (1,1), (1,0)]
        stream2 = [(1,0), (1,0), (1,0), (1,0), (1,1), (1,1), (1,1), (1,1), (0,1)]
        stream3 = [(0,1), (0,1), (0,1), (0,1), (1,1), (1,1)]
        stream4 = [(0,1), (0,1), (0,1), (0,1), (1,0), (1,0), (1,0)]

        self.assertTrue(accepts(dfa_left, init_state, accept_state, stream))
        self.assertTrue(accepts(dfa_left, init_state, accept_state, stream4))
        self.assertFalse(accepts(dfa_left, init_state, accept_state, stream2))
        self.assertFalse(accepts(dfa_left, init_state, accept_state, stream3))

if __name__ == '__main__':
    unittest.main()
