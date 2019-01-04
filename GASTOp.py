"""GASTOp.py
This file runs the gastop program
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the GenAlg class.

"""
import matplotlib.pyplot as plt
from gastop import GenAlg, utilities

# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init_sfr.txt'
config = utilities.init_file_parser(init_file_path)

pop_size = config['ga_params']['pop_size']
num_gens = config['ga_params']['num_generations']


# Create the Genetic Algorithm Object
ga = GenAlg(config)
ga.initialize_population(pop_size)
best, progress_history = ga.run(
    num_generations=num_gens,progress_fitness=True,
    progress_truss=False, num_threads=4)


# print(best.rand_nodes)
# print(best.edges)
# print(best.properties)
# print(best.fos)
# print(best.deflection[:, :, 0])

print(best)

best.plot(domain=config['random_params']['domain'].T,
          loads=config['evaluator_params']['boundary_conditions']['loads'],
          fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
          deflection=True, load_scale=.001, def_scale=100)  # must be followed by plt.show()
#plt.show()
