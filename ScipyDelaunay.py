from scipy.spatial import Delaunay, Voronoi
import numpy as np
import random
from PIL import Image, ImageDraw
import os
import EdgeDetector as ed

def calculateCenter(simplex):
    x = []
    y = []
    for point in simplex:
        x.append(point[0])
        y.append(point[1])

    x = sum(x) / len(x)
    y = sum(y) / len(y)

    return ((x, y))

def getSimplexPoints(ob):
    try:
        var = ob.regions # Voronoi
        pts = ob.vertices
    except:
        var = ob.simplices # Delaunay
        pts = ob.points

    sp = []
    for simplex in var:
        switch = 0
        p = []
        try:
            for point in simplex:
                if point != -1:
                    p.append(tuple(pts[point]))
                else:
                    switch = 1
                    break
            if switch == 0:
                sp.append(p)
        except:
            pass
            # Weird index error caused by extra regions? Lets just ignore it
    return sp

class DelaunayTriangulation:
    """
    Wrapper class for scipy.spatial to edit images
    """
    def __init__(self, refImg, numPoints, edgeDetection=False, pointsList = None):
        self.refImg = Image.open(os.path.join(os.path.dirname(__file__), "Images/" + refImg))
        self.refImgStr = refImg
        self.w, self.h = self.refImg.size
        self.edgeDetect = edgeDetection
        self.numPoints = numPoints

        if pointsList is None:
            self.p = self._initPoints(numPoints)
        else:
            self.p = pointsList

        self.tri = Delaunay(self.p)
        self.simplexPoints = getSimplexPoints(self.tri)

    def __exit__(self, exc_type, exc_val, exc_tb): # How do python destructors work again?
        self.refImg.close()

    def _edgeDetect(self):
        """
        Implements the canny edge detector, used to sample points
        """
        iname = os.path.join(os.path.dirname(__file__), "Images/" + self.refImgStr)

        canny = ed.canny(iname, low=2, high=5, sigma=5, kernel_size=15)

        p = []
        for ir, row in enumerate(canny):
            for ic, col in enumerate(row):
                if col > 200:
                    p.append((ic, ir))

        return random.choices(p, k=self.numPoints)

    def calculateImage(self):
        with Image.new("RGB", self.refImg.size, (30,0,0)) as newImg:
            draw = ImageDraw.Draw(newImg)
            self._drawPolygons(self.simplexPoints, draw)
            newImg.save("Output.bmp", "BMP")

    def setImage(self, img):
        self.refImg.close()
        self.refImg = None # Just in case
        try:
            self.refImgStr = img
            self.refImg = Image.open(img)
            self.p = self._initPoints(self.numPoints)
            self.tri = Delaunay(self.p)
            self.simplexPoints = getSimplexPoints(self.tri)
        except Exception as e:
            print(e)

    def _drawPolygons(self, points, draw): #
        for simplex in points:
            centerPixel = calculateCenter(simplex)
            try:
                color = self.refImg.getpixel(centerPixel)
            except IndexError:
                color = (255,255,255)

            # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            try:
                draw.polygon(simplex, fill=color, outline=color)
            except TypeError:
                draw.polygon(simplex, fill=color[0], outline=color)

    def _initPoints(self, num):

        if self.edgeDetect:
            return self._edgeDetect()
        else:
            p = np.array([[0, 0], [0, self.h], [self.w, 0], [self.w, self.h]])  # Includes 4 corners
            for i in range(num):  # Randomize the points on a plane
                x = random.choice(range(0, self.w, 5))
                y = random.choice(range(0, self.h, 5))
                p = np.vstack([p, [x, y]])
            return p

class VoronoiDiagram:
    def __init__(self, refImg, numPoints, edgeDetection=False, pointsList=None):
        self.refImg = Image.open(os.path.join(os.path.dirname(__file__), "Images/" + refImg))
        self.refImgStr = refImg
        self.w, self.h = self.refImg.size
        self.edgeDetect = edgeDetection
        self.numPoints = numPoints

        if pointsList is None:
            self.p = self._initPoints(numPoints)
        else:
            self.p = pointsList

        self.vor = Voronoi(self.p, qhull_options="Qbb Qc Qx")
        self.simplexPoints = getSimplexPoints(self.vor)



    def __exit__(self, exc_type, exc_val, exc_tb): # How do python destructors work again?
        self.refImg.close()

    def _edgeDetect(self):
        iname = os.path.join(os.path.dirname(__file__), "Images/" + self.refImgStr)

        canny = ed.canny(iname, low=2, high=5, sigma=5, kernel_size=15)

        p = []
        for ir, row in enumerate(canny):
            for ic, col in enumerate(row):
                if col > 200:
                    p.append((ic, ir))

        return random.choices(p, k=self.numPoints)

    def calculateImage(self):
        with Image.new("RGB", self.refImg.size, (30,0,0)) as newImg:
            draw = ImageDraw.Draw(newImg)
            self._drawPolygons(self.simplexPoints, draw)
            newImg.save("Output.bmp", "BMP")

    def setImage(self, img):
        self.refImg.close()
        self.refImg = None # Just in case
        try:
            self.refImgStr = img
            self.refImg = Image.open(img)
            self.p = self._initPoints(self.numPoints)
            self.vor = Voronoi(self.p)
            self.simplexPoints = getSimplexPoints(self.vor)
        except Exception as e:
            print(e)

    def _drawPolygons(self, points, draw):
        for simplex in points:

            centerPixel = calculateCenter(simplex)
            try:
                color = self.refImg.getpixel(centerPixel)
            except IndexError:
                color = (255,255,255)

            #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            try:
                draw.polygon(simplex, fill=color, outline=color)
            except TypeError:
                draw.polygon(simplex, fill=color[0], outline=color)

    def _initPoints(self, num):

        if self.edgeDetect:
            return self._edgeDetect()
        else:
            p = np.array([[0, 0], [0, self.h], [self.w, 0], [self.w, self.h]])  # Includes 4 corners
            for i in range(num):  # Randomize the points on a plane
                x = random.choice(range(0, self.w, 5))
                y = random.choice(range(0, self.h, 5))
                p = np.vstack([p, [x, y]])
            return p


a = DelaunayTriangulation("FakeFace2.jpg", 8000, True)
a.calculateImage()

# Create a voronoi diagram out of input points, producing a new set of points
# b = VoronoiDiagram("FakeFace2.jpg", 4000, True)
# b.calculateImage()

#Create a voronoi diagram out of the vertices of the last diagram, producing original(ish) points
# c = VoronoiDiagram("FakeFace2.jpg", 4000, pointsList=b.vor.vertices)
# c.calculateImage()






