from scipy.spatial import Delaunay
import numpy as np
import random
import PIL
import PIL.Image as Image
from PIL import ImageTk
import graphics as g
import time
import PIL.ImageDraw as ImageDraw

lastimg = [5, "P-2.png"] # Used so the same image isnt used twice. 5 is a placeholder.

while True:# The main loop, this will run forever until stopped manually.
    win = g.GraphWin("Delaunay Triangulation", 1200,1000) # The grid
    #choices = ["I-" + str(x) + ".png" for x in range(0, 20)] # The pictures
    
    """
    Python 2.7's tkinter doesn't like dealing with png files
    so instead of downloading a bunch of single frame gif files
    i've decided instead to do nothing
    """
    
    #img = random.choice(choices)
    img = "I-9.gif"
    
    """
    if img in lastimg:
        continue
    lastimg[0] = img
    """
    
    saveimg = Image.new("RGB", (1000,1000), "white")
    draw = ImageDraw.Draw(saveimg)
    
    pixelsg = g.Image(g.Point(0,0), img)
    copy = pixelsg
    width, height = copy.getWidth(), copy.getHeight() # Gets the width and height of the image
    pixelsg = g.Image(g.Point(width/2, height/2), img)
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
        polycopy = poly[::]
        # Now we have the polygon
        ax = (poly[0][0] + poly[1][0] + poly[2][0]) * (1.0/3)
        ay = (poly[0][1] + poly[1][1] + poly[2][1]) * (1.0/3) # The center of the triangle
        rgb = pixelsg.getPixel(int(ax), int(ay)) # The color at the center of the triangle
        for item in range(len(poly)):# Turning the vertices into points that the graph can understand
            poly[item] = g.Point(poly[item][0], poly[item][1])
        triangle = g.Polygon(poly) # Plotting the triangle
        triangle.setFill(g.color_rgb(rgb[0], rgb[1], rgb[2]))
        triangle.setOutline(g.color_rgb(rgb[0], rgb[1], rgb[2]))
        
        # I actually stole this line from another version of this code that is much more condensed
        # Because i used to like to try to fit code into as few lines as possible
        # As a result I have no idea what it actually does, I just know it saves the image
        draw.polygon([tuple(x) for x in polycopy], fill=g.color_rgb(pixelsg.getPixel(int(ax), int(ay))[0], pixelsg.getPixel(int(ax), int(ay))[1], pixelsg.getPixel(int(ax), int(ay))[2]))
        triangle.draw(win)
    saveimg.save("Output.bmp")
    time.sleep(3)
    win.close()
    
    break
