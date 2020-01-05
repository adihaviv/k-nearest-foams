import plotly.graph_objects as go
import numpy as np
import random
from math import cos, sin


# Point distribution -
# Our structures rely on an isotropic point distribution similarly to procedural Voronoi foams [Martínez et al. 2016].
# We generate one random point in each cell of a virtual grid covering
# the space, which provides a crude but effcient approximation of a
# Poisson disc distribution [Worley 1996]. The subdivision scheme
# of Martínez et al. [2016] is used to locally increase or decrease the
# point density
def build_graph(point_density=10, grid=([0, 1], [0, 1])):
    V = np.array()
    grid_x, grid_y = grid
    cell_size_x = (grid_x[1] - grid_x[0]) / point_density
    cell_size_y = (grid_y[1] - grid_y[0]) / point_density
    for point in range(point_density):
        x = random.uniform(grid_x + point * cell_size_x, grid_x + (point + 1) * cell_size_x)
        y = random.uniform(grid_y + point * cell_size_y, grid_x + (point + 1) * cell_size_y)
        np.append(V.append((x, y)))
    return V


# for 2D - theta is [0-pi]
# for 3D - theta is [[0-pi],[0-pi],[0-pi]] --> https://www.continuummechanics.org/rotationmatrix.html
def create_rotation_matrix(angle):
    if len(angle) == 1:
        theta = angle
        R = np.array([cos(theta), -sin(theta)],
             [sin(theta), cos(theta)])
    elif len(angle) == 3:
        psi = angle[0]
        phi = angle[1]
        theta = angle[2]

        R = np.array(
            [cos(psi)*cos(theta)*cos(phi) - sin(psi)*sin(phi),
             -cos(psi)*cos(theta)*sin(phi) - sin(psi)*cos(phi),
             cos(psi)*sin(theta)],

             [sin(psi)*cos(theta)*cos(phi) + cos(psi)*cos(phi),
              -sin(psi)*cos(theta)*sin(phi) + cos(psi)*cos(phi),
              sin(psi)*sin(theta)],

             [-sin(theta)*cos(phi),
              sin(theta)*sin(phi),
              cos(theta)])
    else:
        raise ValueError('only support 3D and 2D cases')
    return R


# Edge connections -
# follow the notation in the paper https://hal.archives-ouvertes.fr/hal-01577859/file/MSDL17.pdf
# section 4. page 5

# V - the vertices of the graph
# angle - [0,pi]^a where a in {1,3} for 2D and 3D respectively
def rotate_graph(V, angle):
    E = np.array() #points after rotation
    R = create_rotation_matrix(angle)
    for p in V:
        Rp = np.matmul(R,p)
        np.append(E,Rp)
    return E

# V - the vertices of the graph
# H -  stretch vector R^d where d in {2,3} for 2D and 3D respectively
def stretch_graph(V, H):
     U = np.diag(np.exp(V*H,-2))
     return U


# V - the vertices of the graph
# H -  stretch vector R^d where d in {2,3} for 2D and 3D respectively
# angle - [0,pi]^a where a in {1,3} for 2D and 3D respectively
def stretch_and_rotate_graph(V, H, angle):
    E = rotate_graph(V,angle)
    U = stretch_graph(V,H)
    EtU = np.matmul(np.transpose(E),U)
    M = np.matmul(EtU,E)
    return M

def build_edges_k_nearest_neighbors(V,k=6):
    E = {}
    return (V,E)
