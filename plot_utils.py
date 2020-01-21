import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_2d_foam_graph(k_foam):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x, y = k_foam.grid
    for xi in x:
        ax.axvline(x=xi, linestyle='--')
    for yi in y:
        ax.axhline(y=yi, linestyle='--')

    for vi, ni in k_foam.edges.items():
        for vj in ni:
            ax.plot(*zip(vi, vj), 'ko-')

    ax.set_aspect('equal')
    fig.set_size_inches((10, 10))
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
            aspectratio=dict(x=len(k_foam.grid[0]), y=len(k_foam.grid[1]), z=len(k_foam.grid[2])),
            aspectmode='manual'
        ),
    )

    fig.show()


def plot_3d_mesh(mesh):
    x = mesh.vertices[:, 0]
    y = mesh.vertices[:, 1]
    z = mesh.vertices[:, 2]

    i = mesh.faces[:, 0]
    j = mesh.faces[:, 1]
    k = mesh.faces[:, 2]

    fig = go.Figure(data=[
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            colorbar_title='z',
            colorscale=[[0, 'gold'],
                        [0.5, 'mediumturquoise'],
                        [1, 'magenta']],
            intensity=[0, 0.33, 0.66, 1],
            i=i,
            j=j,
            k=k,
            name='y',
            showscale=True
        )
    ])

    fig.show()

