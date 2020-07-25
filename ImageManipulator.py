import EdgeDetector as ed
import DV
from PIL import Image, ImageDraw
import random
import time
import os

if __name__ == "__main__":
    t = time.time()

    iname = os.path.join(os.path.dirname(__file__), "Images/FakeFace2.jpg")

    a = ed.canny(iname, low=2, high=5, sigma=5, kernel_size=15)
    print("Fin canny", time.time() - t)

    white = []
    for ir, row in enumerate(a):
        for ic, col in enumerate(row):
            if col > 200:
                white.append((ic, ir))

    print("Points assigned", time.time() - t)

    print(len(white))
    white = random.choices(white, k=int(len(white) / 10))
    print(len(white))
    print("Points removed", time.time() - t)
    v = DV.Voronoi(white)
    print ("Voronoi", time.time() - t)



    with Image.open(iname) as refImg:
        # See if the white points are working correctly
        with Image.new("RGB", refImg.size, (20, 20, 20)) as test:
            d = ImageDraw.Draw(test)
            for point in white:
                d.point(point, fill=(255, 255, 255))
            test.save("Points.png", "PNG")

        with Image.new("RGB", refImg.size, (0, 0, 0)) as newImg:

            draw = ImageDraw.Draw(newImg)
            for triangle in v.triangles:
                try:
                    center = (
                        (triangle.points[0][0] + triangle.points[1][0] + triangle.points[2][0]) / 3,
                        (triangle.points[0][1] + triangle.points[1][1] + triangle.points[2][1]) / 3
                    )
                    color = refImg.getpixel(center)
                except IndexError:
                    color = (0, 0, 0)

                draw.polygon(triangle.points, fill=color, outline=color)

            newImg.save("Output.bmp", "BMP")