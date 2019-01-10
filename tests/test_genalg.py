"""test_genalg.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the GenAlg class

"""
#!/usr/bin/env python3

import unittest
import numpy as np
from tqdm import tqdm
import time


from gastop import GenAlg, Truss, utilities, ProgMon


# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init.txt'
config = utilities.init_file_parser(init_file_path)


pop_size = int(1e3)
num_gens = int(1e2)


class TestGenAlg_Cristian(unittest.TestCase):  # Cristian
    def testUpdatePopulation(self):
        '''Tests that the population correctly updates every generation.
        '''
        # Create GenAlg object and assign random fitness scores
        pop_size = int(1e4)
        ga = GenAlg(init_file_path)
        ga.initialize_population(pop_size)
        for truss in ga.population:
            truss.fitness_score = np.random.random()

        ga.population.sort(key=lambda x: x.fitness_score)
        ga.update_population()

        # Check that population is sorted by fitness_score
        fitness = [
            truss.fitness_score for truss in ga.population][:config['ga_params']['num_elite']]
        self.assertTrue(sorted(fitness) == fitness)

        for truss in ga.population:
            self.assertTrue(isinstance(truss, Truss))
            self.assertTrue(isinstance(truss.user_spec_nodes, np.ndarray))
            self.assertTrue(isinstance(truss.rand_nodes, np.ndarray))
            self.assertTrue(isinstance(truss.edges, np.ndarray))
            self.assertTrue(isinstance(truss.properties, np.ndarray))

    def testSaveLoadState(self):
        '''Tests that config and population can be saved to and loaded from
        JSON files.
        '''
        # Parse input parameters from init file
        init_file_path = 'gastop-config/struct_making_test_init.txt'
        config = utilities.init_file_parser(init_file_path)

        # Create GenAlg object
        pop_size = int(1e4)
        ga = GenAlg(config)
        ga.initialize_population(pop_size)

        # Save and reload
        ga.save_state()
        ga_loaded = ga.load_state()
        config = ga_loaded.config
        population = ga_loaded.population

        # Test config
        self.assertTrue(isinstance(config['ga_params']['num_elite'], int))
        self.assertTrue(isinstance(
            config['ga_params']['percent_crossover'], float))
        self.assertTrue(type(config['mutator_params']['node_mutator_params']['boundaries'])
                        is type(np.array([1, 1])))
        self.assertTrue(isinstance(
            config['mutator_params']['node_mutator_params']['int_flag'], bool))

        # Test population
        for truss in population:
            self.assertTrue(isinstance(truss, Truss))
            self.assertTrue(isinstance(truss.user_spec_nodes, np.ndarray))
            self.assertTrue(isinstance(truss.rand_nodes, np.ndarray))
            self.assertTrue(isinstance(truss.edges, np.ndarray))
            self.assertTrue(isinstance(truss.properties, np.ndarray))


class TestGenAlg_Dan(unittest.TestCase):
    """Tests genetic algorithm's generate random functionality
    """

    def test_nodes_in_domain(self):
        """Tests if the created nodes are in the desired range.
        """
        # Create the Genetic Algorithm Object
        ga = GenAlg(config)
        ga.initialize_population(pop_size)

        for truss in ga.population:
            for node in truss.rand_nodes:
                self.assertTrue(node[0] > ga.random_params['domain'][0, 0])
                self.assertTrue(node[0] < ga.random_params['domain'][1, 0])
                self.assertTrue(node[1] > ga.random_params['domain'][0, 1])
                self.assertTrue(node[1] < ga.random_params['domain'][1, 1])
                self.assertTrue(node[2] > ga.random_params['domain'][0, 2])
                self.assertTrue(node[2] < ga.random_params['domain'][1, 2])


class TestGenAlg_SFR(unittest.TestCase):

    def testProgressPlotClass(self):
        user_spec_nodes = np.array([[]]).reshape(0, 3)
        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = 10
        population = [Truss(
            user_spec_nodes, nodes, edges, properties) for i in range(pop_size)]

        for truss in population:
            truss.fitness_score = np.random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        GA = GenAlg(config)

        GA.population = population
        progress_fitness = True
        progress_truss = False
        num_generations = 20

        progress = ProgMon(progress_fitness, progress_truss, num_generations)
        #

        # Loop over all generations:
        for current_gen in range(num_generations):
            progress.progress_monitor(current_gen, population)
            for truss in GA.population:
                #truss.fos = np.random.random()
                truss.fitness_score = truss.fitness_score + 5.0
        # plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        return GA.population[0], GA.pop_progress

    def testProgressBar2(self):
        # this doesnt quite work yet, showing all progress bars at the end instead of iteratively
        user_spec_nodes = np.array([[]]).reshape(0, 3)

        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = 10
        population = [Truss(user_spec_nodes, nodes, edges, properties)
                      for i in range(pop_size)]

        for truss in population:
            truss.fitness_score = np.random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        GA = GenAlg(config)

        GA.population = population
        progress_fitness = False
        progress_truss = False

        ax1 = []
        num_generations = 20
        progress = ProgMon(progress_fitness, progress_truss, num_generations)

        #t = tqdm(total=num_generations,leave=False)
        # Loop over all generations:
        for current_gen in tqdm(range(num_generations), desc='Generation', position=0):
            progress.progress_monitor(current_gen, population)
            # t.update(current_gen)
            time.sleep(0.05)
            for truss in tqdm(GA.population, desc='truss', position=1):
                #truss.fos = np.random.random()
                truss.fitness_score = truss.fitness_score + 5.0
        # t.close()
        return GA.population[0], GA.pop_progress

    def testProgressBar(self):
        # this doesnt quite work yet, showing all progress bars at the end instead of iteratively
        user_spec_nodes = np.array([[]]).reshape(0, 3)

        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = 10
        population = [Truss(user_spec_nodes, nodes, edges, properties)
                      for i in range(pop_size)]

        for truss in population:
            truss.fitness_score = np.random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        GA = GenAlg(config)

        GA.population = population
        progress_truss = False
        progress_fitness = False
        # dumb GA run
        num_generations = 20
        progress = ProgMonprogress = ProgMon(
            progress_fitness, progress_truss, num_generations)
        #t = tqdm(total=num_generations,leave=False)
        # Loop over all generations:
        for current_gen in tqdm(range(num_generations)):
            progress.progress_monitor(current_gen, population)
            # t.update(current_gen)
            time.sleep(0.05)
            for truss in GA.population:
                #truss.fos = np.random.random()
                truss.fitness_score = truss.fitness_score + 5.0
        # t.close()
        return GA.population[0], GA.pop_progress

    # def testProgressPlot(self):
    #     user_spec_nodes = np.array([[]]).reshape(0, 3)
    #     nodes = np.array([[1, 2, 3], [2, 3, 4]])
    #     edges = np.array([[0, 1]])
    #     properties = np.array([[0, 3]])
    #
    #     pop_size = 10
    #     population = [Truss(
    #         user_spec_nodes, nodes, edges, properties) for i in range(pop_size)]
    #
    #     for truss in population:
    #         truss.fitness_score = np.random.random()
    #
    #     population.sort(key=lambda x: x.fitness_score)
    #     # print([x.fitness_score for x in population])
    #
    #     GA = GenAlg(config)
    #
    #     GA.population = population
    #     progress_display = 2
    #     num_generations = 20
    #     # dumb GA run
    #     fig = plt.figure()
    #     ax1 = fig.add_subplot(1, 1, 1)
    #     plt.ylabel('fitscore')
    #     plt.xlabel('iteration')
    #     plt.xlim(0,num_generations)
    #
    #     #
    #
    #     # Loop over all generations:
    #     for current_gen in range(num_generations):
    #         GA.progress_monitor(current_gen, progress_display, ax1)
    #         for truss in GA.population:
    #             #truss.fos = np.random.random()
    #             truss.fitness_score = truss.fitness_score + 5.0
    #     plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
    #     return GA.population[0], GA.pop_progress
    #
    #     #GA = GenAlg()
    #     #pop_test = GA.initialize_population(10)
    #
    #     # fos = [i.fos for i in population] #extracts fos for each truss object in population
    #
    #     # note to susan: look up map() and filter()


class TestGenAlgRC(unittest.TestCase):
    """Weird edge cases for inheritance"""

    def testInvalidCrossover(self):
        """Tests genalg when % crossover + % mutation >1"""

        config = utilities.init_file_parser(init_file_path)
        config['ga_params']['percent_crossover'] = .6
        config['ga_params']['percent_mutation'] = .6
        ga = GenAlg(config)
        ga.initialize_population(100)
        for t in ga.population:
            t.fitness_score = np.random.random()
        self.assertRaises(RuntimeError, ga.update_population)

        bad_path = 'gastop-config/error_config.txt'
        self.assertRaises(RuntimeError, utilities.init_file_parser, bad_path)

    def testOddNumCrossover(self):
        """Tests genalg when crossover number is odd
        to make sure it still return the correct population size
        """

        config = utilities.init_file_parser(init_file_path)
        config['ga_params']['percent_crossover'] = 1
        config['ga_params']['percent_mutation'] = 0
        config['ga_params']['num_elite'] = 5
        ga = GenAlg(config)
        ga.initialize_population(100)
        ga.run(num_generations=2)
        self.assertAlmostEqual(len(ga.population), 100)

        # test zero crossover
        config['ga_params']['percent_crossover'] = 0
        config['ga_params']['percent_mutation'] = 1
        ga = GenAlg(config)
        ga.initialize_population(100)
        ga.run(num_generations=2)
        self.assertAlmostEqual(len(ga.population), 100)


if __name__ == "__main__":
    unittest.main()
