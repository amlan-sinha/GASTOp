#!/usr/bin/env python3

import unittest
import numpy as np

import Mutator

class TestMutator_pseudo_bit_flip(unittest.TestCase): #Amlan

    def test_basic(self):
        array = np.ones((10,3))
        bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : False}
        myMutator = Mutator.Mutator([])
        child = myMutator.pseudo_bit_flip(array,bit_flip_params)

    def test_datatype(self):
        array = np.ones((10,3))
        bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : True}
        myMutator = Mutator.Mutator([])
        child = myMutator.pseudo_bit_flip(array,bit_flip_params)

        np.testing.assert_string_equal(str(child.dtype), 'int64')


class TestMutator_gaussian(unittest.TestCase): #Paul
    def test_boundary(self):
        array = np.random.uniform(-10.0, 10.0, [10, 3])
        gaussian_params = {'boundaries': np.array([[0, 10], [-10, 0], [-5, 5]]), 'int_flag': False, 'std': 0.5}
        myMutator = Mutator.Mutator([])
        child = myMutator.gaussian(array, gaussian_params)
        
        bounds = gaussian_params['boundaries']
        if (np.any(child[:,0]<bounds[0,0]) or np.any(child[:,0]>bounds[0,1])):
            raise Exception("A value was mutated out of bounds by gaussian mutator!")
        elif (np.any(child[:,1]<bounds[1,0]) or np.any(child[:,1]>bounds[1,1])):
            raise Exception("A value was mutated out of bounds by gaussian mutator!")
        elif (np.any(child[:,2]<bounds[2,0]) or np.any(child[:,2]>bounds[2,1])):
            raise Exception("A value was mutated out of bounds by gaussian mutator!")

    def test_int_flag(self):
        array = np.random.uniform(-10.0, 10.0, [10, 3])
        gaussian_params = {'boundaries': np.array([[0, 10], [-10, 0], [-5, 5]]), 'int_flag': True, 'std': 0.5}
        myMutator = Mutator.Mutator([])
        child = myMutator.gaussian(array, gaussian_params)
        
        check = np.ones((1,1), dtype=int)
        np.testing.assert_string_equal(str(child.dtype), str(check.dtype))

        
if __name__ == '__main__':
    unittest.main()
