from town import Town
from functools import reduce
import numpy as np
import random

class AntColonyOptimization():


    def __init__(self, dimension, towns, starting_ant_number, ant_growth, rotations, pheromone_decay, Q, Alpha, Beta):
        self.towns = towns
        self.dimension = dimension
        self.ant_number = starting_ant_number
        self.rotations = rotations
        self.pheromones_matrix = self._create_pheromones_matrix()
        self.ants = []
        self._append_ants(starting_ant_number, 0)
        self.pheromone_decay = pheromone_decay
        self.order = None
        self.Q = Q
        self.Alpha = Alpha
        self.Beta = Beta
        self.ant_growth = ant_growth
        self.best_distance = float('inf')
        self.best_ant_index = None


    def detour(self,):
        pass
    
    def _restet_ants(self, starting_index):
        for ant in self.ants:
            ant.reset(starting_index)

    def calculate(self, starting_index = 0):
        for k in range(self.rotations):

            for _ in range(self.dimension):

                pheromones_matrix_naive = self._create_pheromones_matrix(0)
                last_ant_index = 0
                for i, ant in enumerate(self.ants):

                    if len(ant.towns_processed) == self.dimension-1:
                        
                        new_dist = ant.calculate_full_path()
                        if(self.best_distance > new_dist):
                            self.best_distance = new_dist
                            self.best_ant_index = i
                            self.best_ant = self.ants[i]
                        continue

                    current_town = ant.current_town
                    next_town, distance = ant.calculate_next_town(self.towns, self.pheromones_matrix, self.Alpha, self.Beta)
                    self._update_naive_pheromone(pheromones_matrix_naive, current_town, next_town, distance)

                self._update_pheromones(pheromones_matrix_naive)
            
            if(k < self.rotations-1):
                self._restet_ants(self.towns[starting_index])

            
        

        distance = 0
        for i in range(len(self.best_ant.towns_processed)-1):
            townA =self.best_ant.towns_processed[i]
            townB = self.best_ant.towns_processed[i+1]
            distance += Town.distance(townA, townB )
        last_town = self.best_ant.towns_processed[-1]
        distance += Town.distance(self.towns[starting_index], last_town)
        self.best_ant.towns_processed.append(self.towns[starting_index])
        self.order = self.best_ant.towns_processed
        self.distance = distance

        return distance


    def _update_naive_pheromone(self, pheromones_matrix, current_town, next_town, distance):
        first_index = current_town.index
        second_index = next_town.index

        pheromones_matrix[first_index][second_index] += (self.Q/distance)
        pheromones_matrix[second_index][first_index] += (self.Q/distance)

    def _update_pheromones(self, pheromones_matrix_naive):
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.pheromones_matrix[i][j] = ((1-self.pheromone_decay)*self.pheromones_matrix[i][j]) + pheromones_matrix_naive[i][j]

    def print_pheromones_matrs(self):
        for l in self.pheromones_matrix:
            print(l)

    def _create_pheromones_matrix(self, value=1):
        pheromones = []
        for i in range(self.dimension):
            pheromones.append([])
            for _ in range(self.dimension):
                pheromones[i].append(value)
        return pheromones

    def _append_ants(self, amount, starting_index):
        for _ in range(amount):
            self.ants.append(Ant(self.towns[starting_index]))



class Ant():

    def __init__(self, current_town):
        self.current_town = current_town
        self.towns_processed = []


    def calculate_next_town(self, towns, pheromones_matrix, attactivnes_ratio=1, Alpha=1, Beta=1):
        ratios = []
        allowed_towns = []
        for index, town in enumerate(towns):

            if(town != self.current_town and town not in self.towns_processed):
                distance = Town.distance(town, self.current_town)

                ratio = (pheromones_matrix[self.current_town.index][town.index]**Alpha) * ((attactivnes_ratio/distance)**Beta)
                ratios.append(ratio)
                allowed_towns.append(town)

        denominator = reduce(lambda x,y: x+y, ratios)

        probability_distribution = list(map(lambda x: x/denominator, ratios))

        next_town = np.random.choice(allowed_towns, size=1, p=probability_distribution)[0]
        # next_town = random.choices(allowed_towns, probability_distribution, k=1)[0]
        distance = Town.distance(next_town, self.current_town)
        self.towns_processed.append(self.current_town)
        self.current_town = next_town
        return next_town, distance

    def calculate_full_path(self):
        self.towns_processed.append(self.towns_processed[0])
        distance = 0
        for index in range(len(self.towns_processed)-1):
            distance += Town.distance(self.towns_processed[index], self.towns_processed[index+1])
        return distance

    def reset(self, starting_town):
        self.current_town = starting_town
        self.towns_processed = []
    
