
import matplotlib.pyplot as plt
import random


class Edge:
	def __init__(self, p1=(0,0), p2=(0,0) ):
		self.p1 = p1
		self.p2 = p2
	def equal(self, edge):
		if (self.p1 == edge.p1 or self.p1 == edge.p2 and self.p2 == edge.p2 or self.p2 == edge.p1):
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
			raise("Can not calculate circumcenter for points on the same line")
			
		
		D = 2*( self.p1[0]*(self.p2[1] - self.p3[1])  +  self.p2[0]*(self.p3[1] - self.p1[1])  +  self.p3[0]*(self.p1[1] - self.p2[1]) )
		self.cc[0] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p2[1] - self.p3[1]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p3[1] - self.p1[1]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p1[1] - self.p2[1]) )
		self.cc[1] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p3[0] - self.p2[0]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p1[0] - self.p3[0]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p2[0] - self.p1[0]) )
		
		self.ccr = ( (self.p1[0] - self.cc[0])**2 + (self.p1[1] - self.cc[1])**2 )**0.5

def checkSharedEdge(ed, tris):
	# Count how many times edge appears in triangles
	count = 0
	for tri in tris:
		for e in tri.edges:
			if e.equal(ed):
				count += 1
	return count
		

"""
function BowyerWatson (pointList)
      // pointList is a set of coordinates defining the points to be triangulated
      triangulation := empty triangle mesh data structure
      add super-triangle to triangulation // must be large enough to completely contain all the points in pointList
      for each point in pointList do // add all the points one at a time to the triangulation
         badTriangles := empty set
         for each triangle in triangulation do // first find all the triangles that are no longer valid due to the insertion
            if point is inside circumcircle of triangle
               add triangle to badTriangles
         polygon := empty set
         for each triangle in badTriangles do // find the boundary of the polygonal hole
            for each edge in triangle do
               if edge is not shared by any other triangles in badTriangles
                  add edge to polygon
         for each triangle in badTriangles do // remove them from the data structure
            remove triangle from triangulation
         for each edge in polygon do // re-triangulate the polygonal hole
            newTri := form a triangle from edge to point
            add newTri to triangulation
      for each triangle in triangulation // done inserting points, now clean up
         if triangle contains a vertex from original super-triangle
            remove triangle from triangulation
      return triangulation

"""
def Triangulate(pointList, *args):
	# Args is the top right point and bottom left point, respectively
	# If args[1] is omitted, bottom left is assumed to be 0,0
	
	triangulation = [] # Holds triangles
	bottom = args[1] if args[1] else (0, 0) # Set a point at the relative origin of the grid
	top = (bottom[0], 2*args[0][1]) # Set a point located 2x above the height of the grid
	right = (2*args[0][0], bottom[1]) # Set a point located 2x to the right of the grid
	# This creates our super triangle
	
	superTri = Triangle(bottom, top, right)
	triangulation.append(superTri)
	for point in pointList:
		badTriangles = []
		for triangle in triangulation:
			if (( (point[0] - triangle.cc[0])**2 + (point[1] - triangle.cc[1])**2 )**0.5) < triangle.ccr:
				badTriangles.append(triangle)
		polygon = []
		for triangle in badTriangles:
			for edge in triangle.edges:
				if checkSharedEdge(edge, badTriangles) == 2: # Should be 1, is 2 instead, dont know why, will fix later
					polygon.append(edge)
		for triangle in badTriangles:
			triangulation.remove(triangle)
		for edge in polygon:
			newTri = Triangle((edge.p1[0], edge.p1[1]), (edge.p2[0], edge.p2[1]), (point[0], point[1]))
			triangulation.append(newTri)
	for tri in triangulation:
		if (bottom in tri.points or top in tri.points or right in tri.points):
			triangulation.remove(tri)
	return triangulation
				
	


points = [(random.randrange(100), random.randrange(100)) for x in range(50)]


triangles = Triangulate(points, (100, 100), (0, 0))

for triangle in triangles:
	print(triangle)

plt.gcf().gca().axis("equal")
plt.axis([0, 100, 0, 100])

for t in triangles:
	poly = plt.Polygon( [[t.p1[0], t.p1[1]], [t.p2[0], t.p2[1]], [t.p3[0], t.p3[1]]], closed=True, ec="r")		

	plt.plot(t.p1[0], t.p1[1], "ro") # The three points of the triangle
	plt.plot(t.p2[0], t.p2[1], "ro")
	plt.plot(t.p3[0], t.p3[1], "ro")
	
	plt.gcf().gca().add_artist(poly)
plt.show()
"""
t = Triangle(random.choice(points), random.choice(points), random.choice(points))

circle = plt.Circle( (t.cc[0], t.cc[1]), t.ccr, color='b', fill=False)

plt.plot(t.p1[0], t.p1[1], "ro") # The three points of the triangle
plt.plot(t.p2[0], t.p2[1], "ro")
plt.plot(t.p3[0], t.p3[1], "ro")

for point in points:
	plt.plot(point[0], point[1], "o")


plt.plot(t.cc[0], t.cc[1], "bo") # Plot the circumcenter


plt.gcf().gca().add_artist(circle)
plt.gcf().gca().add_artist(poly)
plt.show()
"""
