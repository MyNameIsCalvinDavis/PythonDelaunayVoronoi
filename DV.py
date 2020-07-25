import matplotlib.pyplot as plt
import random
import math

def distance(p1, p2):
	return ( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )**0.5

def checkSharedEdge(ed, tris):
	# Count how many times edge appears in tris
	count = 0
	for tri in tris:
		for edge in tri.edges:
			if edge.equal(ed):
				count += 1
	return count

def orientation(p1, p2, p3):
	v = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
	if v == 0: return 0
	if v > 0:
		return 1
	else:
		return 2

def polarAngle(A, B):  # param: (x, y)
	B = (B[0] - A[0], B[1] - A[1])
	return math.degrees(math.atan((B[1] / (B[0] + 0.001))))

def findNeighbors(tri, tris):
	"""
	Return a list of neighbors in a Delaunay Triangulation
	for a tri given the list of tris it occupies
	"""
	nbs = []
	for t in tris:
		tmp = 0
		for edge in t.edges:
			for ed in tri.edges:
				if ed.equal(edge):
					nbs.append(t)
					tmp = 1
					break
			if tmp == 1:
				break

	return nbs

class Triangle:
	def __init__(self, p1, p2, p3):
		self.p1 = tuple(p1)
		self.p2 = tuple(p2)
		self.p3 = tuple(p3)
		self.points = [p1, p2, p3]
		self.cc = [0, 0]
		self.ccr = 0
		self.edges = [Edge(p1, p2), Edge(p2, p3), Edge(p3, p1)]

		self._calculatecc()

	def __str__(self):
		return str((self.p1, self.p2, self.p3))

	def _calculatecc(self):  # Calculate circumcenter
		if (self.p1[0] == self.p2[0] == self.p3[0]) or (self.p1[1] == self.p2[1] == self.p3[1]):
			raise Exception("Can not calculate circumcenter for points on the same line")

		# Stolen directly from wikipedia
		D = 2 * (self.p1[0] * (self.p2[1] - self.p3[1]) + self.p2[0] * (self.p3[1] - self.p1[1]) + self.p3[0] * (
					self.p1[1] - self.p2[1]))
		self.cc[0] = (1 / D) * ((self.p1[0] ** 2 + self.p1[1] ** 2) * (self.p2[1] - self.p3[1]) + (
					self.p2[0] ** 2 + self.p2[1] ** 2) * (self.p3[1] - self.p1[1]) + (
											self.p3[0] ** 2 + self.p3[1] ** 2) * (self.p1[1] - self.p2[1]))
		self.cc[1] = (1 / D) * ((self.p1[0] ** 2 + self.p1[1] ** 2) * (self.p3[0] - self.p2[0]) + (
					self.p2[0] ** 2 + self.p2[1] ** 2) * (self.p1[0] - self.p3[0]) + (
											self.p3[0] ** 2 + self.p3[1] ** 2) * (self.p2[0] - self.p1[0]))
		self.ccr = ((self.p1[0] - self.cc[0]) ** 2 + (self.p1[1] - self.cc[1]) ** 2) ** 0.5

class Edge:
	def __init__(self, p1=(0,0), p2=(0,0) ):
		self.p1 = p1 if (p1 < p2) else p2
		self.p2 = p2 if (p2 >= p1) else p1
	def equal(self, edge):
		if self.p1 == edge.p1 and self.p2 == edge.p2:
			return True
		return False

class Delaunay:
	"""
	Given a pointList [(x, y), (x, y), ...]
	Generate a Delaunay data structure with the Bowyer-Watson Algorithm
	"""
	def __init__(self, pointList):
		self.pointList = pointList
		self.triangles = self._Triangulate()

	def _Triangulate(self):
		"""
		:return: A list of Triangle objects

		Implementation of the Bowyer-Watson triangulation for x, y > 0
		"""
		TR = (  # Find the top right most point
			max(self.pointList, key=lambda x: x[0])[0] + 1,
			max(self.pointList, key=lambda x: x[1])[1] + 1
		)

		# These points are added to simulate infinity for the voronoi dual graph
		ins = 7  # infinity scale factor
		self.pointList.append((TR[0] * ins, TR[1] * ins))  # TR
		self.pointList.append((TR[0] * ins, TR[1] * (-ins)))  # BR
		self.pointList.append((TR[0] * (-ins), TR[1] * (-ins)))  # BL
		self.pointList.append((TR[0] * (-ins), TR[1] * ins))  # TL

		triangulation = []  # Holds triangles
		s = 50  # super triangle scale factor
		# If this scale factor is not properly larger than the infinity scale factor,
		# the super triangle will not encapsulate the infinity points correctly and the circumcenter
		# for the infinity points will bug out

		# Create the 3 points for our super triangle, must also encapsulate infinity points
		st_bl = (TR[0] * (-s), TR[1] * (-s))
		st_tl = (TR[0] * (-s), TR[1] * s)
		st_r = (TR[0] * s, TR[1] / 2)

		superTri = Triangle(st_bl, st_tl, st_r)
		triangulation.append(superTri)
		for point in self.pointList:
			badTriangles = []
			for triangle in triangulation:
				if distance(point, triangle.cc) < triangle.ccr:
					badTriangles.append(triangle)
			polygon = []
			for triangle in badTriangles:
				for edge in triangle.edges:
					if checkSharedEdge(edge, badTriangles) == 1:
						polygon.append(edge)
			for triangle in badTriangles:
				triangulation.remove(triangle)
			for edge in polygon:
				try:
					newTri = Triangle((edge.p1[0], edge.p1[1]), (edge.p2[0], edge.p2[1]), (point[0], point[1]))
					triangulation.append(newTri)
				except:
					continue
		cleanup = []
		for tri in triangulation:
			if not (st_bl in tri.points or st_tl in tri.points or st_r in tri.points):
				cleanup.append(tri)
		return cleanup

class Voronoi:
	"""
	Given a pointList [(x,y), (x,y), ...]
	Generate a Voronoi data structure by first calculating the Delaunay Triangulation
	and using that to find the dual, the Voronoi Diagram.
	"""
	def __init__(self, pointList, triangulation = None):
		self.pointList = pointList
		self.Delaunay = triangulation
		if triangulation is None:
			self.Delaunay = Delaunay(pointList)

		self.triangles = self.Delaunay.triangles
		self.simplices = self._makeVoronoiCells()

	def _makeVoronoiCells(self):
		"""
		Return a list containing VoronoiCell objects
		"""
		regions = self._identifyVoronoiRegions()
		cells = []

		for region in regions:
			node = region.pop()
			VoronoiPointList = 0
			for tri in region:
				# Get the center of the cell and the vertices of it
				VoronoiPointList = [t.cc for t in region]
			cells.append(VoronoiCell(VoronoiPointList, node))
		return cells

	def _identifyVoronoiRegions(self):
		"""
		Return a 2D list containing the triangles that make each voronoi region (unordered).
		The last part of each list is the shared point for all of the triangles
		that make up that region
		"""
		vcells = []

		for point in self.pointList:
			l = []
			for tri in self.triangles:
				if point in tri.points:
					l.append(tri)
			l.append(point)  # to determine what the shared point is
			vcells.append(l)

		return vcells

class VoronoiCell:
	def __init__(self, pointList, node):
		self.pointList = pointList
		self.edges = self._calculateEdges()
		self.node = node

	def _calculateEdges(self):
		"""
		The cell has vertices associated with it, but not edges, and the vertices aren't
		sorted so it's not as easy as just connecting them. To make the cell walls, we'll
		be using the Graham Scan algorithm which procudes a convex hull given a set of points.
		"""

		f = self._grahamScan()
		self.pointList = f
		edges = []
		for i in range(len(f) - 1):
			edges.append(Edge(f[i], f[i+1]))
		edges.append((f[-1], f[0]))

		return edges

	def _grahamScan(self):
		stack = []

		P0 = min(self.pointList, key=lambda x: x[1])
		c = [x for x in self.pointList if x[1] == P0[1]]
		P0 = min(c)

		# Sorts by polar angle primarily, then distance secondarily
		p = sorted( self.pointList, key = lambda x: (polarAngle(P0, x), distance(P0, x)) )

		for point in p:
			while len(stack) > 1 and orientation(stack[-2], stack[-1], point) < 0:
				stack.pop()
			stack.append(point)
		return stack


def plotVoronoiRegions(ob):
	for simplex in ob.simplices:

		x = [i[0] for i in simplex.pointList]
		y = [i[1] for i in simplex.pointList]

		poly = plt.Polygon( simplex.pointList, closed=True, ec="r", fill=False)
		#plt.gcf().gca().add_artist(poly)
		plt.plot(x, y)

	plt.show()
		#break

def plotTriangles(ob):
	for t in ob.triangles:
		plt.plot(t.p1[0], t.p1[1], "ro") # The three points of the triangle
		plt.plot(t.p2[0], t.p2[1], "ro")
		plt.plot(t.p3[0], t.p3[1], "ro")
		plt.plot(t.cc[0], t.cc[1], "bo")

		poly = plt.Polygon( [[t.p1[0], t.p1[1]], [t.p2[0], t.p2[1]], [t.p3[0], t.p3[1]]], closed=True, ec="r", fill=False)
		plt.gcf().gca().add_artist(poly)

	plt.show()


if __name__ == "__main__":
	points = [(random.randrange(0, 2000, 3), random.randrange(0, 2000, 3)) for x in range(1000)]
	plt.autoscale(enable=True)
	v = Voronoi(points)
	#plotTriangles()
	plotVoronoiRegions(v)

