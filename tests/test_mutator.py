"""test_mutator.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the Mutator class

"""
#!/usr/bin/env python3

import unittest
import numpy as np

from gastop import Mutator


class TestMutator_pseudo_bit_flip(unittest.TestCase):  # Amlan
    """Tests the pseudo bit flip method of the Mutator class."""
    def test_basic(self):
        """Tests whether the method runs without errors"""
        array = np.ones((10, 3))
        bit_flip_params = {'boundaries': np.array(
            [[0, 0, 0], [10, 10, 10]]), 'proportions': 0.5, 'int_flag': False}
        child = Mutator.pseudo_bit_flip(array, **bit_flip_params)

    def test_datatype(self):
        """Tests the functionality of the int_flag argument."""
        array = np.ones((10, 3))
        bit_flip_params = {'boundaries': np.array(
            [[0, 0, 0], [10, 10, 10]]), 'proportions': 0.5, 'int_flag': True}
        child = Mutator.pseudo_bit_flip(array, **bit_flip_params)

        check = np.ones((1, 1), dtype=int)

        np.testing.assert_string_equal(str(child.dtype), str(check.dtype))


class TestMutator_shuffle_index(unittest.TestCase):  # Amlan
    """Tests the shuffle index method of the Mutator class."""
    def test_basic(self):
        """Tests whether the method runs without errors."""
        array = np.random.rand(2, 3)
        shuffle_index_params = {}
        child = Mutator.shuffle_index(array, **shuffle_index_params)

        # check = child != array

        # np.testing.assert_string_equal(str(np.any(check)), 'True')


class TestMutator_gaussian(unittest.TestCase):  # Paul
    """Tests the gaussian method of the mutator class."""
    
    def test_boundary(self):
        """Tests whether the mutator method keeps all values inside the specified boundary."""
        array = np.random.uniform(-10.0, 10.0, [10, 3])
        gaussian_params = {'boundaries': np.array(
            [[0, -10, -5], [10, 0, 5]]), 'int_flag': False, 'std': 0.5}
        child = Mutator.gaussian(array, **gaussian_params)

        bounds = gaussian_params['boundaries']
        if (np.any(child[:, 0] < bounds[0, 0]) or np.any(child[:, 0] > bounds[1, 0])):
            raise Exception(
                "A value was mutated out of bounds by gaussian mutator!")
        elif (np.any(child[:, 1] < bounds[0, 1]) or np.any(child[:, 1] > bounds[1, 1])):
            raise Exception(
                "A value was mutated out of bounds by gaussian mutator!")
        elif (np.any(child[:, 2] < bounds[0, 2]) or np.any(child[:, 2] > bounds[1, 2])):
            raise Exception(
                "A value was mutated out of bounds by gaussian mutator!")

    def test_int_flag(self):
        """Tests the functionality of the int_flag argument."""
        array = np.random.uniform(-10.0, 10.0, [10, 3])
        gaussian_params = {'boundaries': np.array(
            [[0, -10, -5], [10, 0, 5]]), 'int_flag': True, 'std': 0.5}
        child = Mutator.gaussian(array, **gaussian_params)

        check = np.ones((1, 1), dtype=int)
        np.testing.assert_string_equal(str(child.dtype), str(check.dtype))


if __name__ == '__main__':
    unittest.main()
