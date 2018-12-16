import math
import time
from town import Town
from nearest_neighbour import NearestNeighbourAlgorith
from ant_colony import AntColonyOptimization
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def load_data_trimmed(file_name):
    towns = []
    with open(file_name, 'r') as f:
        dimension = int(f.readline())
        for _ in range(dimension):
            index, x, y = f.readline().split(" ")
            towns.append(Town(int(x), int(y), int(index)-1))
    
    return dimension, towns

def load_data_extended(file_name):
    towns = []
    with open(file_name, 'r') as f:
        for _ in range(3):
            f.readline()
        dimension = int(f.readline().split(" ")[1])
        for _ in range(2):
            f.readline()
        for _ in range(dimension):
            
            index, x, y = f.readline().strip().split(" ")
            towns.append(Town(int(float(x)), int(float(y)), int(float(index))-1))
    
    return dimension, towns


def draw_path(order, title=" "):
    codes = [Path.LINETO] * (len(order)-2)
    codes.insert(0, Path.MOVETO)
    codes.append(Path.CLOSEPOLY)
    verts = []
    max_x = -float('inf')
    min_x = float('inf')

    max_y = -float('inf')
    min_y = float('inf')
    for town in order:
        if(town.x > max_x):
            max_x = town.x
        elif (town.x < min_x):
            min_x = town.x
        if (town.y > max_y):
            max_y = town.y
        if (town.y < min_y):
            min_y = town.y

        verts.append((float(town.x), float(town.y)))

    path = Path(verts, codes)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor='white')
    ax.add_patch(patch)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_title(title)
    plt.show()

if __name__ == "__main__":

    dimension, towns = load_data_extended("berlin52.txt")
    # dist = NearestNeighbourAlgorith(dimension, towns).calculate(0)
    # print(dist)

    # dimension, towns = load_data_trimmed("bayg29.txt")
    # NNA = NearestNeighbourAlgorith(dimension, towns)
    # dist = NNA.calculate(0)
    # print(dist)
    # draw_path(NNA.order, "NNA") 

    ACO = AntColonyOptimization(dimension, towns, starting_ant_number=30,
                                rotations=4*dimension, pheromone_decay=0.4,
                                Q=10, Alpha=1, Beta=3)
    dist = ACO.calculate(0)
    print(dist)
    print(len(ACO.order))
    draw_path(ACO.order, "ACO")



    # print(dist)
    #
    #
    # ACO = AntColonyOptimization(dimension, towns, starting_ant_number=10,
    #                             ant_growth=3, rotations=50, pheromone_decay=0.3,
    #                             Q=10, Alpha=1, Beta=3)
    # dist = ACO.calculate(0)
    # print(dist)

