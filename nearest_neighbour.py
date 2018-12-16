from town import Town
import time
def count_time(method):
    def timed(self, starting_index):
        timeA = time.time()
        result =  method(self, starting_index)
        timeB = time.time()
        print(f'czas wykonania algorytmu: {timeB- timeA}')
        return result
    return timed

class NearestNeighbourAlgorith:

    def __init__(self, dimension, towns):
        self.dimension = dimension
        self.towns = towns
        self.distance = None
        self.order = None

   

    def closest_neighbour(self, townA, processed):
        minimum = float('inf')
        next_town = None

        for town in self.towns:
            if townA != town and town not in processed:
                cur_dist = townA.distance(town)
                if(cur_dist < minimum):
                    minimum = cur_dist
                    next_town = town

        return next_town, minimum

    @count_time
    def calculate(self, starting_index = 0):
        
        cur_distance = 0
        processed = []
        current_town = self.towns[starting_index]
        for _ in range(self.dimension):
            current_town, add_distance = self.closest_neighbour(current_town, processed)
            processed.append(current_town)
            cur_distance += add_distance

        cur_distance += current_town.distance(self.towns[starting_index])
        self.distance = cur_distance
        processed.append(self.towns[starting_index])
        self.order = processed
        return cur_distance