from scipy.spatial import Delaunay
import numpy as np
import random
from PIL import Image
from PIL import ImageDraw

class Triangles:
    def __init__(self, refImg, numPoints):
        self.refImg = refImg
        self.refImg = Image.open(refImg)
        self.w, self.h = self.refImg.size

        # Create some points randomly
        self.p = self._initPoints(numPoints)

        # Triangluate them
        self.tri = Delaunay(self.p)

        # print("Points: ", self.p)                  # Generated points w/ numpy
        # print("DPoints: ", self.tri.points)        # Scipy.Delaunay's points, identical to above
        # print("Simplices: ", self.tri.simplices)   # Object's indexed indices from tri.points

        self.simplexPoints = self._getSimplexPoints(self.tri)

        # print(l)          # List of simplices
        # print(l[0])       # A simplex
        # print(l[0][0])    # A point

    def __exit__(self, exc_type, exc_val, exc_tb): # How do python destructors work again?
        self.refImg.close()

    def triangulateImage(self):
        with Image.new("RGB", self.refImg.size, (0,0,0)) as newImg:
            draw = ImageDraw.Draw(newImg)
            self._drawPolygons(self.simplexPoints, draw)
            newImg.save("Output.png", "BMP")

    def _getSimplexPoints(self, triangle):  # Because the triangle object only stores indices for some reason
        return [(
            tuple(triangle.points[simplex[0]]),
            tuple(triangle.points[simplex[1]]),
            tuple(triangle.points[simplex[2]])
        ) for simplex in triangle.simplices]

    def _calculateTriangleCenter(self, simplex):
        return (
            (simplex[0][0] + simplex[1][0] + simplex[2][0]) / 3,
            (simplex[0][1] + simplex[1][1] + simplex[2][1]) / 3
        )

    def _drawPolygons(self, points, draw): #
        for simplex in points:
            centerPixel = self._calculateTriangleCenter(simplex)
            color = self.refImg.getpixel(centerPixel)
            draw.polygon(simplex, fill=color, outline=color)

    def _initPoints(self, num):
        p = np.array([[0, 0], [0, self.h], [self.w, 0], [self.w, self.h]])  # Includes 4 corners
        for i in range(num):  # Randomize the points on a plane
            x = random.choice(range(0, self.w, 5))
            y = random.choice(range(0, self.h, 5))
            p = np.vstack([p, [x, y]])
        return p

a = Triangles("Example.png", 200)
a.triangulateImage()






