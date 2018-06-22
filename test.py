from PIL import Image

# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
img = Image.new( 'RGB', (100,100), "pink") # create a new black image
pixels = img.load()
print(pixels[1,1])
try:
    img2 = Image.open("test2.png")
except IOError:
    img2 = Image.new( 'RGB', (100,100), "black")
