import unittest

import nk

stub_values = [
    {(0,0):0.2, (0,1):0.3, (1,0):0.7, (1,1):0.1},
    {(0,0):0.3, (0,1):0.3, (1,0):0.4, (1,1):0.9},
    {(0,0):0.9, (0,1):0.1, (1,0):0.1, (1,1):0.8},
    {(0,0):0.5, (0,1):0.6, (1,0):0.6, (1,1):0.9},
]

stub_dependence = [
    [0,3],
    [1,2],
    [0,3],
    [2,3]
]

stub_state = (1,0,1,1)

stub_value = (0.1 + 0.3 + 0.8 + 0.9) / 4.0

class TestNK(unittest.TestCase):
    
    def test_new(self):
        m = nk.NK(10,2)
        self.assertEqual(len(m.values), 10)
        self.assertEqual(len(m.dependence), 10)
    
    def test_value(self):
        m = nk.NK(4, 1)
        m.values = stub_values
        m.dependence = stub_dependence
        self.assertEqual(m.get_value(stub_state), stub_value)
    
if __name__ == '__main__':
    unittest.main()
