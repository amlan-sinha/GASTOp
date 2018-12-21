import numpy as np
import Truss

class Crossover():

# Crossover() object takes in two parents and returns two children

    def __init__(self,crossover_params):
        self.params = crossover_params

    def uniform_crossover(self, truss_1, truss_2 ,uniform_crossover_params=None): #Paul
        '''
        For each array, generate another array of 0s and 1s. If its a 0, take
        data from one parent and if its a 1, take data from the other parent.
        Let's say parent one corresponds to 0 and parent two to 1:
        To make normal child, multiply array of 0s and 1s with parent two array
        and the complement of that 0s and 1s array with parent one array and
        add the two resulting arrays together.
        To make the evil kid, do the opposite.
        Output 2 children
        '''
        # find the shape of the parents
        nn = np.shape(truss_1)

        # making an array of ones and zeros
        unos_and_zeros = np.random.randint(2, size=nn)

        # creating an array of all ones to later create the complementary array
        unos = np.ones(nn, dtype=int)

        # creating the complementary array
        unos_and_zeros_c = unos - unos_and_zeros

        # making kids ;)
        child1 = (unos_and_zeros * truss_2) + (unos_and_zeros_c * truss_2)
        child2 = (unos_and_zeros_c * truss_2) + (unos_and_zeros * truss_2)

        # checks for flag that specifies whether output should be an integer and rounds the \
        # output arrays
        if uniform_crossover_params:
            if (uniform_crossover_params['int_flag']==True):
                child1 = (np.rint(child1)).astype(int)
                child2 = (np.rint(child2)).astype(int)

        return child1, child2

    def single_point_split(self, array_1, array_2, single_point_split_params=None): #Amlan

        (array_row,array_col) = array_1.shape
        point = np.random.randint(0, array_row)

        child_1 = np.concatenate((array_1[:point],array_2[point:]),axis=0)
        child_2 = np.concatenate((array_2[:point],array_1[point:]),axis=0)

        if single_point_split_params:
            if (single_point_split_params['int_flag']==True):
                child_1 = (np.rint(child_1)).astype(int)
                child_2 = (np.rint(child_2)).astype(int)

        return child_1, child_2

    def __call__(self,truss_1,truss_2):

        node_method = getattr(self,self.params['node_crossover_method'])
        edge_method = getattr(self,self.params['edge_crossover_method'])
        property_method = getattr(self,self.params['property_crossover_method'])

        child_1 = Truss.Truss(0,0,0)
        child_2 = Truss.Truss(0,0,0)
        child_1.nodes, child_2.nodes = node_method(truss_1.nodes,truss_2.nodes,self.params['node_crossover_params'])
        child_1.edges, child_2.edges = edge_method(truss_1.edges,truss_2.edges,self.params['edge_crossover_params'])
        child_1.properties, child_2.properties = property_method(truss_1.properties,truss_2.properties,self.params['property_crossover_params'])

        return child_1, child_2
