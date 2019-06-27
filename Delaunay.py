from scipy.spatial import Delaunay
import numpy as np
import random
import PIL
import PIL.Image as Image
from PIL import ImageTk
from graphics import *
import time

"""

How does it work?

- First, the program plots 1000 points randomly on a grid.

- Second, using the Delaunay Triangulation, the program triangulates every point.
    - It creates an object (named tri) that acts as a grid
    - In this, you can iterate through all of the triangles (simplices)
      and get the color of the image at the center of that triangle.
        - To break it down:
        > Iterate through every triangle in the grid
        > Get the center of that triangle
        > Find the color of the pixel on the image at the center of the triangle
        
- Lastly, it iterates through every triangle and graphs the vertices of 
  that triangle to the grid, with the color at the circumcenter.
"""

lastimg = [5, "P-2.png"] # Used so the same image isnt used twice. 5 is a placeholder.

while True:# The main loop, this will run forever until stopped manually.
    win = GraphWin("Delaunay Triangulation - Calvin Davis", 1200,1000) # The grid
    choices = ["I-" + str(x) + ".png" for x in range(0, 20)] # The pictures
    img = random.choice(choices)
    img = "I-9.gif"
    
    if img in lastimg:
        continue
    lastimg[0] = img
    
    pixelsg = Image(Point(0,0), img)
    copy = pixelsg
    width, height = copy.getWidth(), copy.getHeight() # Gets the width and height of the image
    pixelsg = Image(Point(width/2, height/2), img)
    #pixelsg.draw(win)
    time.sleep(1)
    

    p = np.array([[0, 0], [0, height], [width, 0], [width, height]])# The list in which the points go
    blacklist = []
    for i in range(500): # Randomize the points on a plane
        x = random.choice(range(0, width, 5))
        y = random.choice(range(0, height, 5))
        if [x, y] not in blacklist: # Dont repeat any points
            p = np.vstack([p, [x, y]])
            blacklist.append([x, y])
    tri = Delaunay(p)

    simplexVIs = [] # "Simplex Vertex indices"
    for simplex in tri.vertices:
        simplexVIs.append(simplex) # Not important

    simplexVs = [] # "Simplex Vertices"
    for vertexTriplet in simplexVIs: # Grab the vertices of every simplex and add to a list
        templist = []
        for vertex in vertexTriplet:
            templist.append(tri.points[vertex])
        simplexVs.append(templist) # Get the 3 vertices that make the triangle
        

    for simplex in simplexVs:# iterate through every triangle
        poly = []
        for vertex in simplex: # Keep in mind vertex is an X, Y pair
            poly.append([vertex[0], vertex[1]])
        # Now we have the polygon
        ax = (poly[0][0] + poly[1][0] + poly[2][0]) * (1.0/3)
        ay = (poly[0][1] + poly[1][1] + poly[2][1]) * (1.0/3) # The center of the triangle
        rgb = pixelsg.getPixel(int(ax), int(ay)) # The color at the center of the triangle
        for item in range(len(poly)):# Turning the vertices into points that the graph can understand
            poly[item] = Point(poly[item][0], poly[item][1])
        triangle = Polygon(poly) # Plotting the triangle
        triangle.setFill(color_rgb(rgb[0], rgb[1], rgb[2]))
        triangle.setOutline(color_rgb(rgb[0], rgb[1], rgb[2]))
        triangle.draw(win)

    """
    plt.triplot(p[:,0], p[:,1], tri.vertices)
    plt.plot(p[:,0], p[:,1], "o")
    plt.show()
    """
    print "Done!"
    time.sleep(2)
    win.close()
    break
