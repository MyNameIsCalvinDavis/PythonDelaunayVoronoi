import random, PIL, PIL.Image as Image, time, PIL.ImageDraw as ImageDraw, graphics as g, numpy as np
from scipy.spatial import Delaunay
while True:
    win = g.GraphWin("Delaunay Triangulation", 1300,1000)
    choices = [("I-" + str(x) + ".png") for x in range(0, 37)]
    img = random.choice(choices)
    img = "I-9.gif"
    pixelsg = g.Image(g.Point(0,0), img);copy = pixelsg;width, height = copy.getWidth(), copy.getHeight();pixelsg = g.Image(g.Point(width/2, height/2), img);saveimg = Image.new("RGB", (1000,1000), "white");draw = ImageDraw.Draw(saveimg);p, blacklist = np.array([[0, 0], [0, height], [width, 0], [width, height]]), []
    for i in range(600):
        x, y = random.choice(range(0, width, 30)), random.choice(range(0, height, 30))
        if [x, y] not in blacklist:p = np.vstack([p, [x, y]]);blacklist.append([x, y])
    simplexVs, tri = [], Delaunay(p)
    for vertexTriplet in tri.vertices:
        templist = [tri.points[vertex] for vertex in vertexTriplet]
        simplexVs.append(templist)
    for simplex in simplexVs:
        poly = [[vertex[0], vertex[1]] for vertex in simplex]
        polycopy = poly[::]
        ax, ay = (poly[0][0] + poly[1][0] + poly[2][0]) * (1.0/3), (poly[0][1] + poly[1][1] + poly[2][1]) * (1.0/3)
        for item in range(len(poly)):poly[item] = g.Point(poly[item][0], poly[item][1])
        triangle = g.Polygon(poly);triangle.setFill(g.color_rgb(pixelsg.getPixel(int(ax), int(ay))[0], pixelsg.getPixel(int(ax), int(ay))[1], pixelsg.getPixel(int(ax), int(ay))[2]));triangle.setOutline(g.color_rgb(pixelsg.getPixel(int(ax), int(ay))[0], pixelsg.getPixel(int(ax), int(ay))[1], pixelsg.getPixel(int(ax), int(ay))[2]))
        draw.polygon([tuple(x) for x in polycopy], fill=g.color_rgb(pixelsg.getPixel(int(ax), int(ay))[0], pixelsg.getPixel(int(ax), int(ay))[1], pixelsg.getPixel(int(ax), int(ay))[2]))
        triangle.draw(win)
    saveimg.save("Output.bmp")
    print "Done!"
    time.sleep(3)
    win.close()
    
