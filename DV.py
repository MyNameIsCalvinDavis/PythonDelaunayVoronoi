
import matplotlib.pyplot as plt
import random


class Edge:
	def __init__(self, p1=(0,0), p2=(0,0) ):
		self.p1 = p1
		self.p2 = p2

class Triangle:
	def __init__(self, p1=(0,0), p2=(0,0), p3=(0,0) ):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.points = [p1, p2, p3]
		self.cc = [0, 0]
		self.ccr = 0
		
		self.edges = [ Edge(p1, p2), Edge(p2, p3), Edge(p3, p1) ]
		
		self.calculatecc()
	
	def calculatecc(self):
		# Sanitize
		if ((self.p1[0] == self.p2[0] == self.p3[0]) or (self.p1[1] == self.p2[1] == self.self.p3[1])):
			raise("Can not calculate circumcenter for points on the same line")
			
		
		D = 2*( self.p1[0]*(self.p2[1] - self.p3[1])  +  self.p2[0]*(self.p3[1] - self.p1[1])  +  self.p3[0]*(self.p1[1] - self.p2[1]) )
		self.cc[0] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p2[1] - self.p3[1]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p3[1] - self.p1[1]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p1[1] - self.p2[1]) )
		self.cc[1] = (1 / D) * ( (self.p1[0]**2 + self.p1[1]**2)*(self.p3[0] - self.p2[0]) + (self.p2[0]**2 + self.p2[1]**2)*(self.p1[0] - self.p3[0]) + (self.p3[0]**2 + self.p3[1]**2)*(self.p2[0] - self.p1[0]) )
		
		self.ccr = ( (self.p1[0] - self.cc[0])**2 + (self.p1[1] - self.cc[1])**2 )**0.5


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
	bottom = args[1] if args[1] else [0, 0]
	superTri = Triangle(, 
	


points = [(random.randrange(100), random.randrange(100)) for x in range(50)]
points.append((0,0))
points.append((0, 99))
points.append((99, 0))
points.append((99,99))

triangles = Triangulate(points, (100, 100))



		
"""


t = Triangle(random.choice(points), random.choice(points), random.choice(points))

plt.gcf().gca().axis("equal")
plt.axis([0, 100, 0, 100])
circle = plt.Circle( (t.cc[0], t.cc[1]), t.ccr, color='b', fill=False)
poly = plt.Polygon( [[t.x[0], t.y[0]], [t.x[1], t.y[1]], [t.x[2], t.y[2]]], closed=True, ec="r")

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
