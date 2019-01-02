#!/usr/bin/env python3

import unittest
import numpy as np
import gastop.__main__


class TestCLParse(unittest.TestCase):
    def test_parser(self):
        clargs = '-t 2 -p 1000 -g 100 folder/test_file_path.txt'
        clargs = clargs.split()
        args = gastop.__main__.parse_args(clargs)
        self.assertEqual(args.num_threads, 2)
        self.assertEqual(args.pop_size, 1000)
        self.assertEqual(args.num_gens, 100)
        self.assertEqual(args.config_path, 'folder/test_file_path.txt')


class TestMain(unittest.TestCase):
    def test_main(self):
        clargs1 = '-t 2 -p 50 -g 10 gastop-config/struct_making_test_init.txt'.split()
        gastop.__main__.main(clargs1)
        clargs2 = 'gastop-config/main_test.txt'.split()
        gastop.__main__.main(clargs2)


if __name__ == '__main__':
    unittest.main()
