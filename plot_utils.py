import matplotlib.pyplot as plt
import plotly.graph_objects as go


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

def plot_3d_foam_graph(k_foam):
    fig = go.Figure()

    for vi, ni in k_foam.edges.items():
        x1, y1, z1 = vi
        for vj in ni:
            x2, y2, z2 = vj
            fig.add_trace(go.Scatter3d(
                x=[x1, x2], y=[y1, y2], z=[z1, z2],
                marker=dict(
                    size=6,
                    color='darkblue'
                ),
                line=dict(
                    color='black',
                    width=4
                )
            ))

    fig.update_layout(
        width=800,
        height=700,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0,
                    y=1,
                    z=1,
                )
            ),
            aspectratio=dict(x=1, y=1, z=1),
            aspectmode='manual'
        ),
    )

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
