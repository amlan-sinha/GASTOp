"""GASTOp.py
This file runs the gastop program
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the GenAlg class.

"""
from gastop import GenAlg, utilities
import imageio

# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init_sfr.txt'
config = utilities.init_file_parser(init_file_path)

pop_size = config['ga_params']['pop_size']
num_gens = config['ga_params']['num_generations']

progress_fitness = False
progress_truss = True
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
          deflection=True, load_scale=.001, def_scale=100)

if progress_truss and not progress_fitness:
    images = []
    for i in range(num_gens):
        images.append(imageio.imread(
            'animation/truss_evo_iter' + str(i) + '.png'))
    imageio.mimsave('animation/truss_evo_gif.gif', images, duration=0.5)
