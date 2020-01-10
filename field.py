import itertools
import numpy as np


class OrthotropicField(object):
	"""
	Implementation of a data structure that represents the local orthotropic behavior of a material.

	The OrthotropicField structure rely on an the assumptions described in [1], where a material posses an orthotropic
	elasticity characteristics, that can be depicted in each location by a few parameters:
		* The point density Voronoi Foam representing the material [Martínez et al. 2016]
		* The n-dimensional angle of the local rotation matrix
		* The n-dimensional stretch ratios of the local stretch matrix.

	To represent the local behavior in a discrete manner, we represent it over a grid, divided into local tiles.
	Each tile is uniform in its elasticity characteristics, while those can vary between tiles.

	[1] Orthotropic k-nearest foams for additive manufacturing, Martinez et al. 2017.

	Parameters
	----------
		grid : np.array,
			an array of dimensions d x m, where d is the number of dimensions (2 or 3)
			and m is the number of tiles along each dimension.
			The grid represents an arrangement of m ^ d tiles, each represented by an in
			(Example - np.array([[0, 1], [0, 1]])
		density : np.array,
			an array of dimensions m x m ... x m (determined by d), describing the uniform density for each tile.
			The density of each tile will be translated to the number of foam vertices created in that tile.
			(Example - np.array([[5, 10,], [5, 5]]))
		angle:  np.array,
			an array of dimensions m x m ... x m (determined by d), describing the uniform rotation angle for each tile.
			(Example (2D) - np.array([[0.78, 0.78], [0.1, 0.78]]))
		stretch:  np.array,
			an array of dimensions m x m ... x m (determined by d), describing the uniform stretch ratios for each tile.
			(Example (2D) - np.array([[(10.0, 20.0), (20.0, 40.0)], [(20.0, 40.0), (10.0, 10.0)]])

	Examples
	--------
	field = OrthotropicField(grid, density, angle, stretch)
	field.cell_sizes
	"""
	def __init__(self, grid, density, angle, stretch):
		self._grid = grid
		self._dim = len(grid)
		self._cell_sizes = [np.diff(grid[di])[0] for di in range(self._dim)]

		self._density = density
		self._angle = angle
		self._stretch = stretch

	def tile_density(self, *tile_indices):
		return self._density[tile_indices]

	def tile_orthotropic(self, *tile_indices):
		return self._angle[tile_indices], self._stretch[tile_indices]

	def point_orthotropic(self, *point_indices):
		tile_indices = self._find_matching_tile(point_indices)
		return self.tile_orthotropic(*tile_indices)

	@property
	def grid(self):
		return self._grid

	@property
	def cell_sizes(self):
		return self._cell_sizes

	@property
	def dim(self):
		return self._dim

	def _find_matching_tile(self, *point_indices):
		tile_indices = []
		for di, pi in zip(self._grid, *point_indices):
			tile_indices.append(di[di <= pi].max())
		return tuple(tile_indices)

	def __iter__(self):
		self.__iter_tiles = itertools.product(*[range(len(di)) for di in self._grid])
		return self

	def __next__(self):
		return next(self.__iter_tiles)
