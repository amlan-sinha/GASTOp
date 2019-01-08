"""GASTOp.py
This file runs the gastop program
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the GenAlg class.

"""
from gastop import GenAlg, utilities
import imageio

animation_path = '/Users/Dan/Documents/Academic/Current Classes/MAE 524 (Comp. Mtds.)/Final Project/APC524_FinalProject/animation' #needs to be full path
# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init2.txt'
#init_file_path = 'gastop-config/struct_making_test_init_sfr_cantilevered.txt'
init_file_path = 'gastop-config/struct_making_test_init2.txt'

config = utilities.init_file_parser(init_file_path)

pop_size = config['ga_params']['pop_size']
num_gens = config['ga_params']['num_generations']
progress_fitness = config['monitor_params']['progress_fitness']
progress_truss = config['monitor_params']['progress_truss']

# Create the Genetic Algorithm Object
ga = GenAlg(config)
ga.initialize_population(pop_size)
best, progress_history = ga.run(
    num_generations=num_gens, progress_fitness=progress_fitness,
    progress_truss=progress_truss, num_threads=4)


print(best)

best.plot(domain=config['random_params']['domain'],
          loads=config['evaluator_params']['boundary_conditions']['loads'],
          fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
<<<<<<< HEAD
          deflection=True, load_scale=.0002, def_scale=10)
=======
          deflection=True, load_scale=.001, def_scale=100)

>>>>>>> b40dbd717efcb9ecb4ece2ee532d3bb854e14819
progress_fitness = True
progress_truss = True
utilities.save_gif(progress_history, progress_fitness, progress_truss, animation_path, num_gens,config)
