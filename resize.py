import Image


imageFile = "J-1.png"
im1 = Image.open(imageFile)
width, height = im1.size

while True:
    if width > 1200 or height > 1200:
        width, height = int(width*(0.95)), int(height*(0.95))
    elif width < 800 or height < 800:
        width, height = int(width*(1.05)), int(height*(1.05))
    else:
        break

im5 = im1.resize((width, height), Image.ANTIALIAS) # best down-sizing filter
im5.save(imageFile)
print ("Done")

