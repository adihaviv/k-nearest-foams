import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


def plot_2d_foam_graph(k_foam):
    fig = plt.figure()

    x, y = k_foam.grid
    for xi, yi in zip(x, y):
        plt.axvline(x=xi, linestyle='--')
        plt.axhline(y=yi, linestyle='--')

    for vi, ni in k_foam.edges.items():
        for vj in ni:
            plt.plot(*zip(vi, vj), 'ko-')

    fig.show()


def plot_3d_mesh(x, y, z):
    #  Download data set from plotly repo
    # pts = np.loadtxt(np.DataSource().open('https://raw.githubusercontent.com/plotly/datasets/master/mesh_dataset.txt'))
    # x, y, z = pts.T

    fig = go.Figure(data=[go.Mesh3d(x=x,
                                    y=y,
                                    z=z,
                                    color='lightpink',
                                    opacity=0.50)])
    fig.show()
