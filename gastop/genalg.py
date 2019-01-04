"""genalg.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the GenAlg class.

"""

#import matplotlib.pyplot as plt
#from matplotlib import style
import numpy as np
import json
from tqdm import tqdm, tqdm_notebook, tnrange
from multiprocessing import Pool
import copy
import colorama
from gastop import Truss, Mutator, Crossover, Selector, Evaluator, FitnessFunction, encoders, utilities, ProgMon
colorama.init()  # for progress bars on ms windows


class GenAlg():
    """Creates, updates, tracks, loads, and saves populations.

    The GenAlg Class orchestrates all of the other functions that perform
    functions to change the population and its elements. In this case, such
    classes are crossover, evaluator, encoders, fitness, mutator, selector, and
    truss.

    In brief, GenAlg calls many other functions in order to create a generation
    which is then analyzed to fully determine its relavant properties. These
    properties are then used to create a new generation and the process repeats
    until a final solution is reached.

    """

    def __init__(self, config):
        """Creates a GenAlg object

        Once created, the object will store all of the relavant information
        about a population. The object also contains the necessary functions to
        modify itself, evaluate its 'goodness', and then create new members for
        the next generation.

        Args:
            Either:
            config (dict): Configuration dictionary with parameters, such as one
                created by :meth:`gastop.utilities.init_file_parser`
            config (str): File path to config file to be parsed. Used
                instead of passing config dictionary directly.

        Returns:
            GenAlg callable object
        """
        if isinstance(config, str):
            config = utilities.init_file_parser(config)

        self.config = config
        self.ga_params = config['ga_params']
        self.mutator_params = config['mutator_params']
        self.random_params = config['random_params']
        self.crossover_params = config['crossover_params']
        self.selector_params = config['selector_params']
        self.population = []
        self.evaluator = Evaluator(**config['evaluator_params'])
        self.fitness_function = FitnessFunction(**config['fitness_params'])

        # progress monitor stuff
        self.pop_progress = []  # initialize as empty array
        # self.progress_display = progress_display #type of progress display
        # [0,1,2] = [no display, terminal display, plot display], change to text later
        if isinstance(self.random_params['rng_seed'], tuple):
            np.random.set_state(self.random_params['rng_seed'])
        elif isinstance(self.random_params['rng_seed'], int):
            np.random.seed(self.random_params['rng_seed'])
        else:
            np.random.seed(1729)

    def generate_random(self):  # Dan
        '''Generates and returns new truss objects with random properties

        The random method first determines the desired ranges of all values
        that will be calculated. Then, random numbers for the node locations,
        connections, and properties are all determined with the numpy.random
        methods.

        Args:
            None

        Returns:
            (Truss object): Truss object with the newly determined values
        '''
        # Generates new random chromosomes with uniform distribution
        num_rand_nodes = self.random_params['num_rand_nodes']
        num_rand_edges = self.random_params['num_rand_edges']
        user_spec_nodes = self.random_params['user_spec_nodes']
        num_user_spec_nodes = user_spec_nodes.shape[0]
        domain = self.random_params['domain']
        # First, generate the new nodes:
        # Try 1: Time: 0.579
        # Ranges = domain[1]-domain[0]
        # new_nodes = np.random.rand(num_rand_nodes, 3)
        #
        # for j in range(3):
        #     new_nodes[:, j] = new_nodes[:, j]*Ranges[j] + \
        #         domain[0][j]*np.ones(num_rand_nodes)

        # Try 2: Time: 0.499
        # nn1 = np.random.rand(num_rand_nodes, 1)*Ranges[0] + domain[0][0]
        # nn2 = np.random.rand(num_rand_nodes, 1)*Ranges[1] + domain[0][1]
        # nn3 = np.random.rand(num_rand_nodes, 1)*Ranges[2] + domain[0][2]
        # new_nodes = np.concatenate((nn1,nn2,nn3),axis=1)

        # Try 3: Time: 0.451
        # new_nodes = np.empty([num_rand_nodes,3])
        # for j in range(3):
        #     new_nodes[:,j] = np.random.rand(num_rand_nodes)*Ranges[j] + domain[0][j]

        # Try 4: Time: 0.433!
        new_nodes = np.random.uniform(
            domain[0], domain[1], (num_rand_nodes, 3))

        # 2nd, generate the new edges between the nodes:
        new_edges = np.random.randint(num_rand_nodes + num_user_spec_nodes,
                                      size=(num_rand_edges, 2))

        new_properties = np.random.randint(self.random_params['num_material_options'],
                                           size=(num_rand_edges))

        return Truss(user_spec_nodes, new_nodes, new_edges, new_properties)

    def initialize_population(self, pop_size=None):
        '''Initializes population with randomly creates Truss objects

        Args:
            pop_size (int): size of the population. If not specified, it
                            defaults to whatever was in the init file

        Returns:
            Updated self.population
        '''
        if pop_size:
            self.ga_params['pop_size'] = pop_size
        else:
            pop_size = self.ga_params['pop_size']

        # Try 1: t= 0.298
        self.population = []
        for i in tqdm(range(pop_size), total=pop_size, leave=False, desc='Initializing Population', position=0):
            self.population.append(self.generate_random())

        # Try 2: t= 0.352
        # pool = Pool()
        # result_list = [pool.map_async(self.generate_random, ()) for i in range(pop_size)]
        #
        # self.population = [res.get() for res in result_list]

        # Try 3: t=0.343
        # pool = Pool()
        # pool.map_async(self.generate_random, range(pop_size),callback=self.population.extend)
        # pool.close()
        # pool.join()

        # Try 4: t=0.232
        # pool = Pool()
        # self.population = list(tqdm(pool.imap(
        #     self.generate_random, range(pop_size), int(np.sqrt(pop_size))), total=pop_size, leave=False, desc='Initializing Population', position=0))
        # pool.close()
        # pool.join()

    def run(self, num_generations=None, progress_display=1, num_threads=None):
        '''Runs the genetic algorithm over all populations and generations

        Args:
            num_generations (int): number of generations to be performed
            progress_display (1,2,or 3): Determines what the progress monitor should display
            num_threads (int): number of threads the multiprocessing should employ

        Returns:
            2-element tuple containing:

            - **self.population[0]** *(Truss)*: The Truss with the best Factor
              of safety.

            - **propgress.pop_progress** (dict): Dictionary containing:

                - ``'Item 1'`` *(blah)*: blah
                - ``'Item 2'`` *(blah)*: blah
        '''
        if num_threads is None:
            if self.ga_params['num_threads'] is None:
                num_threads = 1
            else:
                num_threads = self.ga_params['num_threads']
        if num_generations is None:
            num_generations = self.ga_params['num_generations']
        else:
            self.ga_params['num_generations'] = num_generations

        # ***
        # if progress_display == 2:  # check if figure method of progress monitoring is requested
            # initialize plot:
        #    fig = plt.figure()
        #    ax1 = fig.add_subplot(1, 1, 1)
        #    plt.ylabel('fos')
        #    plt.xlabel('iteration')
        # initialize progress monitor object
        progress = ProgMon(progress_display, num_generations)
        # ***
        if self.ga_params['pop_size'] < 1e4:
            chunksize = int(np.amax((self.ga_params['pop_size']/100, 1)))
        else:
            chunksize = int(np.sqrt(self.ga_params['pop_size']))
        # Loop over all generations:

        for current_gen in tqdm(range(num_generations), desc='Overall', position=0):
            self.ga_params['current_generation'] = current_gen
            # no parallelization
            if num_threads == 1:
                for current_truss in tqdm(self.population, desc='Evaluating', position=1):
                    self.evaluator(current_truss)
                for current_truss in tqdm(self.population, desc='Scoring', position=1):
                    self.fitness_function(current_truss)
            else:
                pool = Pool(num_threads)
                self.population = list(tqdm(pool.imap(
                    self.evaluator, self.population, chunksize),
                    total=self.ga_params['pop_size'], desc='Evaluating', position=1))
                self.population = list(tqdm(pool.imap(
                    self.fitness_function, self.population, chunksize),
                    total=self.ga_params['pop_size'], desc='Scoring', position=1))
                pool.close()
                pool.join()

            self.population.sort(key=lambda x: x.fitness_score)
            progress.progress_monitor(current_gen, self.population)

            self.update_population()  # Determine which members to
            # if progress_display == 2:
            # plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
            if self.ga_params['save_frequency'] != 0 and (current_gen % self.ga_params['save_frequency']) == 0:
                self.save_state(
                    dest_config=self.ga_params['config_save_name'], dest_pop=self.ga_params['pop_save_name'])
        return self.population[0], progress.pop_progress

    # def progress_monitor(self, current_gen, progress_display, ax1):  # Susan
    #     # three options: plot, progress bar ish thing, no output just append
    #     # calc population diversity and plot stuff or show current results
    #     # extract factor of safety from each truss object in population
    #     fitscore = [i.fitness_score for i in self.population]
    #     self.pop_progress.append(self.population)  # append to history
    #     if progress_display == 1:
    #         print(current_gen, np.amin(fitscore))
    #     elif progress_display == 2:
    #         # print(current_gen,min(fitscore))
    #         # plot minimum fitscore for current gen in black
    #         ax1.scatter(current_gen, np.amin(fitscore), c=[0, 0, 0])
    #         # pause for 0.0001s to allow plot to update, can potentially remove this
    #         plt.pause(0.0001)

        # could make population a numpy structured array
        # fitness = population(:).fos
        # plt.plot(it,fitness)
        # plt.ylabel('convergence')
        # plt.xlabel('iteration')
        # plt.show()

        # pass

    def save_state(self, dest_config='config.json',
                   dest_pop='population.json'):  # Cristian
        '''Saves the current population and config settings

        Args:
            dest_config (string): filename to be saved for the config
            dest_pop (string): filename to be saved

        Returns:
            Nothing
        '''
        # Save rng_seed for reloading
        self.config['random_params']['rng_seed'] = np.random.get_state()

        config = self.config
        population = copy.deepcopy(self.population)

        # Save config data
        with open(dest_config, 'w') as f:
            config_dumped = json.dumps(config, cls=encoders.ConfigEncoder)
            json.dump(config_dumped, f)

        # Save population data
        with open(dest_pop, 'w') as f:
            pop_dumped = json.dumps(population, cls=encoders.PopulationEncoder)
            json.dump(pop_dumped, f)

    @staticmethod
    def load_state(dest_config='config.json',
                   dest_pop='population.json'):  # Cristian
        '''Loads the current population and config settings

        Args:
            dest_config (string): filename to be uploaded from for the config
            dest_pop (string): filename to be uploaded from

        Returns:
            GenAlg Object
        '''
        # Load config data
        with open(dest_config, 'r') as f:
            config_loaded = json.load(f)
        config = json.loads(config_loaded, object_hook=encoders.numpy_decoder)

        # Load population data
        with open(dest_pop, 'r') as f:
            pop_loaded = json.load(f)
        population = json.loads(pop_loaded, object_hook=encoders.numpy_decoder)
        population = (Truss(**dct) for dct in population)

        ga = GenAlg(config)
        ga.population = population
        return ga

    def update_population(self):  # Cristian
        ''' Creates new population by performing crossover and mutation, as well
        as taking elites and randomly generating trusses.

        First sorts the population by fitness score, from most fit to least fit.
        Creates selector object from population and method. Calls selector to
        get list of parents for crossover and mutation. Performs crossover and
        mutation.
        '''

        # Store parameters for readability
        population = self.population
        pop_size = self.ga_params['pop_size']
        percent_crossover = self.ga_params['percent_crossover']
        percent_mutation = self.ga_params['percent_mutation']
        num_elite = self.ga_params['num_elite']

        # Sort population by fitness score (lowest score = most fit)
        # population.sort(key=lambda x: x.fitness_score) #remove

        # Calculate parents needed for crossover, ensure even number
        num_crossover = round((pop_size-num_elite)*percent_crossover)
        if (num_crossover % 2) != 0:  # If odd, decrement by 1
            num_crossover -= 1
        # Calculate parents needed for mutation
        num_mutation = round((pop_size-num_elite)*percent_mutation)
        # Calculate remaining number of trusses in next population
        num_random = pop_size - num_elite - num_crossover - num_mutation
        if num_random < 0:  # Raise exception if input params are unreasonable
            raise RuntimeError('percent_crossover + percent_mutation > 1')

        # Instantiate objects
        selector = Selector(self.selector_params)
        crossover = Crossover(self.crossover_params)
        mutator = Mutator(self.mutator_params)

        # Select parents as indices in current population
        crossover_parents = selector(num_crossover, population)
        mutation_parents = selector(num_mutation, population)

        # Save most fit trusses as elites
        pop_elite = population[:num_elite]

        pbar = tqdm(total=(num_crossover+num_mutation+num_random),
                    desc='Updating', position=1)
        # Portion of new population formed by crossover
        pop_crossover = []
        for i in range(0, num_crossover, 2):
            parentindex1 = crossover_parents[i]
            parentindex2 = crossover_parents[i+1]
            parent1 = population[parentindex1]
            parent2 = population[parentindex2]
            child1, child2 = crossover(parent1, parent2)
            pop_crossover.extend((child1, child2))
            pbar.update(2)

        # Portion of new population formed by mutation
        pop_mutation = []
        for i in range(num_mutation):
            parentindex = mutation_parents[i]
            parent = population[parentindex]
            child = mutator(parent)
            pop_mutation.append(child)
            pbar.update()

        # Create new random trusses with remaining spots in generation
        pop_random = []
        for i in range(num_random):
            pop_random.append(self.generate_random())
            pbar.update()

        # Append separate lists to form new generation
        population = pop_elite + pop_crossover + pop_mutation + pop_random
        pbar.close()
        # Update population attribute
        self.population = population
        return
