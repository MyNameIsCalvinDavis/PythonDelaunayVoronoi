import matplotlib.pyplot as plt
import random
import math

class Edge:
	def __init__(self, p1=(0,0), p2=(0,0) ):
		self.p1 = p1 if (p1 < p2) else p2
		self.p2 = p2 if (p2 >= p1) else p1
	def equal(self, edge):
		if (self.p1 == edge.p1 and self.p2 == edge.p2):
			return True
		return False

class VoronoiCell:
	def __init__(self, triangles):

		self.triangles = triangles
		self.node = self.triangles.pop()
		self.DelauynayPointList = self._calculatePointsFromTriangles(triangles)
		self.VoronoiPointList = [t.cc for t in triangles]
		print("OGPL", self.VoronoiPointList)

		self.edges = self._calculateEdges()
		self.P0 = 0

	def _calculatePointsFromTriangles(self, triangles):
		l = []
		for t in triangles:
			for point in t.points:
				if not point in l:
					l.append(point)
		if self.node in l:
			l.remove(self.node)

		return l

	def _calculateEdges(self):
		"""
		The cell has vertices associated with it, but not edges, and the vertices aren't
		sorted so it's not as easy as just connecting them. To make the cell walls, we'll
		be using the Graham Scan algorithm which procudes a convex hull given a set of points.
		"""

		f = self._grahamScan()
		for i in range(len(f) - 1):
			self.edges.append(Edge(f[i], f[i+1]))
		self.edges.append(f[-1], f[0])

	def _grahamScan(self):
		# Lowest y coordinate and leftmost point, in that priority order
		stack = []
		P0 = min(self.VoronoiPointList, key=lambda x: x[1])
		p = sorted( self.VoronoiPointList, key = lambda x: self._polarAngle(P0, x) )

		# TODO: Check if points have the same polar angle
		# Kinda hoping this problem just disappears but i know it wont

		for point in p:
			while len(stack) > 1 and self._orientation(stack[-2], stack[-1], point) < 0:
				stack.pop()
			stack.append(point)
		return stack


	def _orientation(self, p1, p2, p3):
		v = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
		if v == 0: return 0
		if v > 0: return 1
		else: return 2

	def _polarAngle(self, A, B): # param: (x, y)
		B = (B[0] - A[0], B[1] - A[1])
		return math.degrees(math.atan((B[1] / (B[0] + 0.001))))


class Triangle:
	def __init__(self, p1, p2, p3 ):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.points = [p1, p2, p3]
		self.cc = [0, 0]
		self.ccr = 0
		self.edges = [ Edge(p1, p2), Edge(p2, p3), Edge(p3, p1) ]
		
		self._calculatecc()
	
	def __str__(self):
		return str((self.p1, self.p2, self.p3))
	
	def _calculatecc(self): # Calculate circumcenter
		if ((self.p1[0] == self.p2[0] == self.p3[0]) or (self.p1[1] == self.p2[1] == self.p3[1])):
			raise Exception("Can not calculate circumcenter for points on the same line")
			
		# Stolen directly from wikipedia
		D = 2*( self.p1[0]*(self.p2[1] - self.p3[1])  +  self.p2[0]*(self.p3[1] - self.p1[1])  +  self.p3[0]*(self.p1[1] - self.p2[1]) )
		self.cc[0] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p2[1] - self.p3[1]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p3[1] - self.p1[1]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p1[1] - self.p2[1]) )
		self.cc[1] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p3[0] - self.p2[0]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p1[0] - self.p3[0]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p2[0] - self.p1[0]) )
		self.ccr = ( (self.p1[0] - self.cc[0])**2 + (self.p1[1] - self.cc[1])**2 )**0.5

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

def checkSharedEdge(ed, tris):
	# Count how many times edge appears in tris
	count = 0
	for tri in tris:
		for edge in tri.edges:
			if edge.equal(ed):
				count += 1
	return count

def distance(p1, p2):
	return ( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )**0.5
		

def Triangulate(pointList):
	"""
	:param pointList: [(x,y), (x,y), ...] where points > 0
	:return: A list of Triangle objects

	Implementation of the Bowyer-Watson triangulation
	"""

	# BL = ( # Find the bottom left most point
	# 	min(pointList, key = lambda x: x[0])[0] + 1,
	# 	min(pointList, key = lambda x: x[1])[1] + 1
	# )
	TR = ( # Find the top right most point
		max(pointList, key=lambda x: x[0])[0] + 1,
		max(pointList, key=lambda x: x[1])[1] + 1
	)

	# These points are added to simulate infinity for the voronoi dual graph
	ins = 7 # infinity scale factor
	pointList.append((  TR[0]*ins, TR[1]*ins  )) 	# TR
	pointList.append((  TR[0]*ins, TR[1]*(-ins) )) 	# BR
	pointList.append((  TR[0]*(-ins), TR[1]*(-ins) ))# BL
	pointList.append((  TR[0]*(-ins), TR[1]*ins ))	# TL



	triangulation = [] # Holds triangles
	s = 50 # super triangle scale factor
	# If this scale factor is not properly larger than the infinity scale factor,
	# the super triangle will not encapsulate the infinity points correctly and the circumcenter
	# for the infinity points will bug out

	# Create the 3 points for our super triangle, must also encapsulate infinity points
	st_bl = (  TR[0]*(-s), TR[1]*(-s)  )
	st_tl = (  TR[0]*(-s), TR[1]*s)
	st_r = (  TR[0]*s, TR[1] / 2)
	
	superTri = Triangle(st_bl, st_tl, st_r)
	triangulation.append(superTri)
	for point in pointList:
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
				


points = [(random.randrange(0,200, 3), random.randrange(0, 200, 3)) for x in range(50)]

points = [
	(1, 1),
	(3, 1),
	(4, 2),
	(3, 5),
	(2, 4),
	(1, 3)
]

triangles = Triangulate(points)


def Voronoiify(pointList):
	tris = Triangulate(pointList)
	voronois = []

	for point in pointList:
		l = []
		for tri in tris:
			if point in tri.points:
				l.append(tri)
		l.append(point) # to determine what the shared point is
		return l
		break


v = VoronoiCell(Voronoiify(points))

plt.gcf().gca().axis("equal")
plt.axis([0, 100, 0, 100])

def plotA():
	for t in triangles:

		plt.plot(t.p1[0], t.p1[1], "ro") # The three points of the triangle
		plt.plot(t.p2[0], t.p2[1], "ro")
		plt.plot(t.p3[0], t.p3[1], "ro")
		plt.plot(t.cc[0], t.cc[1], "bo")

		circle = plt.Circle( (t.cc[0], t.cc[1]), t.ccr, color='b', fill=False)
		poly = plt.Polygon( [[t.p1[0], t.p1[1]], [t.p2[0], t.p2[1]], [t.p3[0], t.p3[1]]], closed=True, ec="r", fill=False)

		#plt.gcf().gca().add_artist(circle)
		#plt.gcf().gca().add_artist(poly)


	# Voronoi
	for t in triangles:
		nbs = findNeighbors(t, triangles)
		for nb in nbs:
			plt.plot([t.cc[0], nb.cc[0]], [t.cc[1], nb.cc[1]], "k-")
	plt.show()

plotA()

