import matplotlib.pyplot as plt
import random

class Edge:
	def __init__(self, p1=(0,0), p2=(0,0) ):
		self.p1 = p1 if (p1 < p2) else p2
		self.p2 = p2 if (p2 >= p1) else p1
	def equal(self, edge):
		if (self.p1 == edge.p1 and self.p2 == edge.p2):
			return True
		return False

class Triangle:
	def __init__(self, p1=(0,0), p2=(0,0), p3=(0,0) ):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.points = [p1, p2, p3]
		self.cc = [0, 0]
		self.ccr = 0
		
		self.edges = [ Edge(p1, p2), Edge(p2, p3), Edge(p3, p1) ]
		
		self.__calculatecc()
	
	def __str__(self):
		return str((self.p1, self.p2, self.p3))
	
	def __calculatecc(self):
		# Sanitize
		if ((self.p1[0] == self.p2[0] == self.p3[0]) or (self.p1[1] == self.p2[1] == self.p3[1])):
			raise Exception("Can not calculate circumcenter for points on the same line")
			
		
		D = 2*( self.p1[0]*(self.p2[1] - self.p3[1])  +  self.p2[0]*(self.p3[1] - self.p1[1])  +  self.p3[0]*(self.p1[1] - self.p2[1]) )
		self.cc[0] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p2[1] - self.p3[1]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p3[1] - self.p1[1]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p1[1] - self.p2[1]) )
		self.cc[1] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p3[0] - self.p2[0]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p1[0] - self.p3[0]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p2[0] - self.p1[0]) )
		
		self.ccr = ( (self.p1[0] - self.cc[0])**2 + (self.p1[1] - self.cc[1])**2 )**0.5

def findNeighbors(tri, tris):
	nbs = []
	#tris.remove(tri)
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
		

def Triangulate(pointList, BL, TR):
	triangulation = [] # Holds triangles
	bottom = (BL[0]-10, BL[1]-10) # Set a point at the relative origin of the grid
	top = (BL[0]-10, 2*TR[1]+10) # Set a point located 2x above the height of the grid
	right = (2*TR[0]+10, BL[1]-10) # Set a point located 2x to the right of the grid
	# This creates our super triangle
	
	superTri = Triangle(bottom, top, right)
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
		if not (bottom in tri.points or top in tri.points or right in tri.points):
			cleanup.append(tri)
	return cleanup
				


points = [(random.randrange(0,100, 10), random.randrange(0, 100, 10)) for x in range(50)]
points.append((50,50))
points.append((0,0))
points.append((0,99))
points.append((99,0))
points.append((99,99))

triangles = Triangulate(points, (0,0), (100,100))

plt.gcf().gca().axis("equal")
plt.axis([0, 100, 0, 100])


for t in triangles:
			
	plt.plot(t.p1[0], t.p1[1], "ro") # The three points of the triangle
	plt.plot(t.p2[0], t.p2[1], "ro")
	plt.plot(t.p3[0], t.p3[1], "ro")
	plt.plot(t.cc[0], t.cc[1], "bo")
	
	circle = plt.Circle( (t.cc[0], t.cc[1]), t.ccr, color='b', fill=False)
	poly = plt.Polygon( [[t.p1[0], t.p1[1]], [t.p2[0], t.p2[1]], [t.p3[0], t.p3[1]]], closed=True, ec="r")
	
	#plt.gcf().gca().add_artist(circle)
	plt.gcf().gca().add_artist(poly)


# Voronoi
for t in triangles:
	nbs = findNeighbors(t, triangles)
	for nb in nbs:
		plt.plot([t.cc[0], nb.cc[0]], [t.cc[1], nb.cc[1]], "k-")
plt.show()
