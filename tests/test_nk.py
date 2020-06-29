import math
import nkmodel as nk
import unittest

stub_values = [
    {(0,0):1/8, (0,1):3/8, (1,0):5/8, (1,1):7/8},
    {(0,0):4/8, (0,1):4/8, (1,0):5/8, (1,1):3/8},
    {(0,0):3/8, (0,1):6/8, (1,0):1/8, (1,1):6/8},
    {(0,0):2/8, (0,1):3/8, (1,0):8/8, (1,1):3/8},
]

stub_dependence = [
    [0,2],
    [1,3],
    [1,2],
    [2,3]
]

stub_state = (1,0,1,1)
stub_max_state = (1,1,1,0)
stub_max_value = (7/8 + 5/8 + 6/8 + 8/8) / 4.0

stub_value = (7/8 + 4/8 + 6/8 + 3/8) / 4.0

stub_all_state_values = {
    (0,0,0,0): 10/32, (0,0,0,1): 11/32, (0,0,1,0): 21/32, (0,0,1,1): 16/32,
    (0,1,0,0): 9/32, (0,1,0,1): 8/32, (0,1,1,0): 22/32., (0,1,1,1): 15/32,
    (1,0,0,0): 14/32, (1,0,0,1): 15/32, (1,0,1,0): 25/32, (1,0,1,1): 20/32,
    (1,1,0,0): 13/32, (1,1,0,1): 12/32, (1,1,1,0): 26/32, (1,1,1,1): 19/32
}

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
    
    def test_get_global_max(self):
        m = nk.NK(4, 1)
        m.values = stub_values
        m.dependence = stub_dependence
        self.assertEqual(m.get_global_max(), (stub_max_state, stub_max_value))
        
    def test_all_state_values(self):
        m = nk.NK(4, 1)
        m.values = stub_values
        m.dependence = stub_dependence
        state_values = m.get_all_state_values()
        self.assertEqual(state_values,stub_all_state_values)
        
    def test_exponent(self):
        m = nk.NK(4, 1, exponent=2)
        m.values = stub_values
        m.dependence = stub_dependence
        self.assertEqual(m.get_value(stub_state), math.pow(stub_value, 2))
        
        
if __name__ == '__main__':
    unittest.main()
