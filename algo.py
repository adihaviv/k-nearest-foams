import plotly.graph_objects as go
import numpy as np
import random


# Point distribution -
# Our structures rely on an isotropic point distribution similarly to procedural Voronoi foams [Martínez et al. 2016].
# We generate one random point in each cell of a virtual grid covering
# the space, which provides a crude but effcient approximation of a
# Poisson disc distribution [Worley 1996]. The subdivision scheme
# of Martínez et al. [2016] is used to locally increase or decrease the
# point density
def build_graph(point_density=10, grid=([0, 1], [0, 1])):
    V = []
    grid_x, grid_y = grid
    cell_size_x = (grid_x[1] - grid_x[0]) / point_density
    cell_size_y = (grid_y[1] - grid_y[0]) / point_density
    for point in range(point_density):
        x = random.uniform(grid_x + point * cell_size_x, grid_x + (point + 1) * cell_size_x)
        y = random.uniform(grid_y + point * cell_size_y, grid_x + (point + 1) * cell_size_y)
        V.append((x, y))
    return V


# We produce the angular edge length bias by stretching the distance computation when selecting the k-nearest neighbors
def stretch_graph(V,angle):
    return V

def build_edges_k_nearest_neighbors(V,k=6):
    E = {}
    return (V,E)
