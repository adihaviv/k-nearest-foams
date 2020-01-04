import plotly.graph_objects as go
import numpy as np

#Download data set from plotly repo
pts = np.loadtxt(np.DataSource().open('https://raw.githubusercontent.com/plotly/datasets/master/mesh_dataset.txt'))
x, y, z = pts.T

fig = go.Figure(data=[go.Mesh3d(x=x,
                                y=y,
                                z=z,
                                color='lightpink',
                                opacity=0.50)])
fig.show()
