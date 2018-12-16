from town import Town
from functools import reduce
import numpy as np
import random
import copy


class AntColonyOptimization():


    def __init__(self, dimension, towns, starting_ant_number, rotations, pheromone_decay, Q, Alpha, Beta):
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
        self.best_distance = float('inf')
        self.best_ant_index = None


    def detour(self,):
        pass
    
    def _restet_ants(self, starting_index):
        for ant in self.ants:
            ant.reset(self.towns[starting_index])

    def calculate(self, starting_index = 0):
        
        for _ in range(self.rotations):
            cumulative_pheromones_matrix = self._create_pheromones_matrix(0)
            for ant in self.ants:
                if len(ant.towns_processed) == len(self.towns):
                    distance_traveled = ant.calculate_full_path()
                    if(distance_traveled < self.best_distance):
                        self.best_distance = distance_traveled
                        self.best_ant = copy.deepcopy(ant)
                    ant.reset(self.towns[starting_index])

                previous_town, next_town = ant.go_to_next_town(self.towns, self.pheromones_matrix, attactivnes_ratio=self.Q, Alpha=self.Alpha, Beta=self.Beta)
                self._update_naive_pheromone(cumulative_pheromones_matrix, previous_town, next_town)

            self._update_pheromones(cumulative_pheromones_matrix) #after rotation we update matrix


        self.order = self.best_ant.towns_processed
        return self.best_distance

    def _update_naive_pheromone(self, pheromones_matrix, current_town, next_town):
        first_index = current_town.index
        second_index = next_town.index
        distance = Town.distance(current_town, next_town)
        pheromones_matrix[first_index][second_index] += (self.Q/distance)
        pheromones_matrix[second_index][first_index] += (self.Q/distance)

    def _update_pheromones(self, pheromones_matrix_naive):
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.pheromones_matrix[i][j] = ((1-self.pheromone_decay)*self.pheromones_matrix[i][j]) + pheromones_matrix_naive[i][j]
                


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
        self.towns_processed.append(current_town)


    def calculate_next_town(self, towns, pheromones_matrix, attactivnes_ratio=1, Alpha=1, Beta=1) -> (Town, float):
        ratios = []
        allowed_towns = []

        for index, town in enumerate(towns):

            if(town != self.current_town and town not in self.towns_processed):
                distance = town.distance(self.current_town)

                ratio = (pheromones_matrix[self.current_town.index][town.index]**Alpha) * ((attactivnes_ratio/distance)**Beta)
                ratios.append(ratio)
                allowed_towns.append(town)

        denominator = reduce(lambda x,y: x+y, ratios)

        probability_distribution = list(map(lambda x: x/denominator, ratios))

        next_town = np.random.choice(allowed_towns, size=1, p=probability_distribution)[0]
       
        return next_town, distance


    def calculate_full_path(self):
        self.towns_processed.append(self.towns_processed[0])
        distance = 0
        for index in range(len(self.towns_processed)-1):
            distance += Town.distance(self.towns_processed[index], self.towns_processed[index+1])
        return distance


    def reset(self, starting_town: Town):
        self.current_town = starting_town
        self.towns_processed = []
        self.towns_processed.append(starting_town)
    
    def go_to_next_town(self, towns, pheromones_matrix, attactivnes_ratio=1, Alpha=1, Beta=1) -> (Town, Town):
        next_town, distance =self.calculate_next_town(towns, pheromones_matrix, attactivnes_ratio, Alpha, Beta)
        self.towns_processed.append(self.current_town)

        previous_town = self.current_town
        self.current_town = next_town
        return previous_town, next_town