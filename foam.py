import numpy as np
from math import cos, sin
import random


class KNearestFoam(object):
	"""
	Implementation of K-Nearest Foam [1]
	The foam is locally orthotropic and its characteristics are controlled by an Orthotropic Field
	give to it as input.
	For further details on the Orthotropic Field refer to the OrthotropicField class.

	The foam structure rely on an isotropic point distribution similarly to procedural
	Voronoi foams [Martínez et al. 2016].
	We generate one random point in each cell of a virtual grid covering the space, which provides a crude but
	efficient approximation of a Poisson disc distribution [Worley 1996].
	The subdivision scheme of Martínez et al. [2016] is used to locally increase or decrease the density.

	[1] Orthotropic k-nearest foams for additive manufacturing, Martinez et al. 2017.

	Parameters
	----------
		orthotropic_field : OrthotropicField instance,
			field over a n-dimentional grid, controlling to local characteristics of the foam.
		k : int,
			the degree of the foam. k defines the number of edges connecting each vertex in the foam.

	Examples
	--------
	k_foam = KNearestFoam(field, k=3)
	k_foam.vertices, k_foam.edges
	"""
	def __init__(self, orthotropic_field, k):
		self._field = orthotropic_field
		self._k = k
		self._populate_vertices()
		self._populate_edges(self._k)

	@property
	def vertices(self):
		return self._V

	@property
	def edges(self):
		return self._E

	@property
	def grid(self):
		return self._field.grid

	def _populate_vertices(self):
		cell_sizes = self._field.cell_sizes

		self._V = []
		for tile_indices in self._field:
			local_density = self._field.tile_density(*tile_indices)
			for _ in range(local_density):
				point = [random.uniform(ti, ti + ci) for ti, ci in zip(tile_indices, cell_sizes)]
				self._V.append(tuple(point))

	def _populate_edges(self, k):
		self._E = {}

		for p_i in self.vertices:
			angle_i, stretch_i = self._field.point_orthotropic(*p_i)
			M_i = KNearestFoam._get_distance_matrix(angle_i, stretch_i)

			p_i_neighbors = []
			for p_j in self.vertices:

				if p_i == p_j:
					continue

				angle_j, stretch_j = self._field.point_orthotropic(*p_j)
				M_j = KNearestFoam._get_distance_matrix(angle_j, stretch_j)

				d_ij = KNearestFoam._distance(M_i, M_j, p_i, p_j)
				p_i_neighbors.append((d_ij, p_j))

			p_i_neighbors = sorted(p_i_neighbors, key=lambda x: x[0])  # sort by distance
			p_i_knn = [p_j for d_ij, p_j in p_i_neighbors[:k]]
			self._E[p_i] = p_i_knn

	@staticmethod
	def _create_rotation_matrix(angle):
		if not isinstance(angle, np.ndarray):
			theta = angle
			R = np.array([
				[cos(theta), -sin(theta)],
				[sin(theta), cos(theta)]
			])
		elif len(angle) == 3:
			psi = angle[0]
			phi = angle[1]
			theta = angle[2]

			R = np.array([
				[cos(psi) * cos(theta) * cos(phi) - sin(psi) * sin(phi),
				 -cos(psi) * cos(theta) * sin(phi) - sin(psi) * cos(phi),
				 cos(psi) * sin(theta)],

				[sin(psi) * cos(theta) * cos(phi) + cos(psi) * cos(phi),
				 -sin(psi) * cos(theta) * sin(phi) + cos(psi) * cos(phi),
				 sin(psi) * sin(theta)],

				[-sin(theta) * cos(phi),
				 sin(theta) * sin(phi),
				 cos(theta)]])
		else:
			raise ValueError('only support 3D and 2D cases')
		return R

	@staticmethod
	def _create_stretch_matrix(stretch):
		U = np.diag(np.power(stretch, -2))
		return U

	@staticmethod
	def _get_distance_matrix(angle, stretch):
		E = KNearestFoam._create_rotation_matrix(angle)
		U = KNearestFoam._create_stretch_matrix(stretch)
		EtU = np.matmul(np.transpose(E), U)
		M = np.matmul(EtU, E)
		return M

	@staticmethod
	def _distance(M_i, M_j, p_i, p_j):
		p_i, p_j = np.array(p_i), np.array(p_j)
		d_pi_pj = np.sqrt(np.matmul(np.matmul(np.transpose((p_i - p_j)), M_i), (p_i - p_j)))
		d_pj_pi = np.sqrt(np.matmul(np.matmul(np.transpose((p_j - p_i)), M_j), (p_j - p_i)))
		return (d_pi_pj + d_pj_pi) / 2
