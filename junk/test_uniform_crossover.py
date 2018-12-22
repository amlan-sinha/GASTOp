#!/usr/bin/env python3

import unittest
import numpy as np

import Crossover

class TestCrossoverPaul(unittest.TestCase):
    def testZeros(self):
        truss_1 = np.zeros(10, dtype=int)
        truss_2 = np.zeros(10, dtype=int)

        my_uniform_crossover = Crossover.Crossover([])
        result = my_uniform_crossover.uniform_crossover(truss_1, truss_2)

        np.testing.assert_array_equal(result[0], truss_1)
        np.testing.assert_array_equal(result[1], truss_2)

    def testOutputTypeInt(self):
        truss_1 = np.zeros(10, dtype=np.float64)
        truss_2 = np.zeros(10, dtype=np.float64)
        check = np.zeros(10, dtype=int)
        crossover_params = {'int_flag': True}
        
        my_uniform_crossover = Crossover.Crossover([])
        result = my_uniform_crossover.uniform_crossover(truss_1, truss_2, crossover_params)

        np.testing.assert_array_equal(result[0], check)
        np.testing.assert_array_equal(result[1], check)

        np.testing.assert_string_equal(str((result[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(str((result[1]).dtype), str(check.dtype))


if __name__ == "__main__":
    unittest.main()
