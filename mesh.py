import numpy as np
from pymesh.wires import WireNetwork, Inflator


def foam_graph_to_mesh(k_foam, thickness):
	V, E = k_foam.vertices, k_foam.edges

	V_ = []
	E_ = []
	dups = []
	for v in V:
		V_.append(10 * np.array(v))
		nv = E[v]
		for ni in nv:
			if (ni, v) in dups:
				continue
			E_.append(np.array([V.index(v), V.index(ni)]))
			dups.append((ni, v))
			dups.append((v, ni))

	V_, E_ = np.array(V_), np.array(E_)

	wire_network = WireNetwork().create_from_data(V_, E_)
	wire_network.center_at_origin()
	wire_network.compute_symmetry_orbits()

	inflator = Inflator(wire_network)
	inflator.inflate(thickness)

	return inflator.mesh