"""test_utilities.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the Utilities class

"""
#!/usr/bin/env python3

import unittest
import numpy as np
from gastop import Truss, utilities


class TestUtilities_Cristian(unittest.TestCase):  # Cristian
    """Tests for init file parsing"""

    def testInitFileParser(self):
        """Tests that the init file is parsed correctly"""

        init_file_path = 'gastop-config/boolean_parse_test_init.txt'
        config = utilities.init_file_parser(init_file_path)
        # for key in config:
        #     print(key)
        #     print(config[key])
        self.assertTrue(isinstance(config['ga_params']['num_elite'], int))
        self.assertTrue(
            isinstance(config['ga_params']['percent_crossover'], float))
        self.assertTrue(type(config['mutator_params']['node_mutator_params']['boundaries'])
                        is type(np.array([1, 1])))
        self.assertTrue(isinstance(
            config['mutator_params']['node_mutator_params']['int_flag'], bool))
        self.assertTrue(config['general']['bool0'] is False)
        self.assertTrue(config['general']['bool1'] is True)
        self.assertTrue(config['general']['boolnone'] is None)


class TestTrussPlot(unittest.TestCase):
    """Test for plot method. Doesn't assert, visual inspection used for pass/fail"""

    def test_truss_plot(self):
        """Plots a pyramidal truss with loads and deflections."""

        user_spec_nodes = np.array([[-1, -1, 0], [-1, 1, 0]])
        rand_nodes = np.array([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
        edges = np.array([[0, 1], [1, 2], [2, 3], [3, 0],
                          [0, 4], [1, 4], [2, 4], [3, 4]])
        properties = np.zeros(8)
        loads = np.concatenate((np.zeros((4, 6)), np.array(
            [[-100, 0, -100, 0, 0, 0]])), axis=0).reshape(5, 6, 1)
        fixtures = np.concatenate(
            (np.ones((4, 6)), np.zeros((1, 6))), axis=0).reshape(5, 6, 1)
        load_scale = .005
        def_scale = 10
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        truss.deflection = np.concatenate((np.zeros((4, 6)), np.array(
            [[-.01, 0, -.01, 0, 0, 0]])), axis=0).reshape(5, 6, 1)
        domain = np.array([[-1.5, 1.5], [-1.5, 1.5], [0, 1.5]]).T
        truss.plot(domain, loads, fixtures, True, load_scale, def_scale)


if __name__ == "__main__":
    unittest.main()
