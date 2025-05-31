# Using 'Pillow' for image drawing.


from PIL import Image, ImageDraw

# Image config
IMG_SIZE = 1024
STAR_RADIUS = 1

system_coordinates = [
    # Let `system_coordinates` be a list of `(x, y, z)` tuples, loaded from either the SDE or ESI
]

# Determine bounding-box
xMin, xMax, zMin, zMax = 0,0,0,0
for (x, y, z) in system_coordinates:
    xMin = min(xMin, x)
    xMax = max(xMax, x)
    zMin = min(zMin, z)
    zMax = max(zMax, z)

MAP_SIZE = max((xMax - xMin), (zMax - zMin))

img = Image.new("RGBA", (IMG_SIZE, IMG_SIZE), (0, 0, 0, 255))
draw = ImageDraw.Draw(img)

for (x, y, z) in system_coordinates:
    draw.circle(
        (
            (x-xMin)/MAP_SIZE * IMG_SIZE,   # X
            (-(z-zMax))/MAP_SIZE * IMG_SIZE # Y
        ),
        STAR_RADIUS,
        fill=(255, 255, 255, 255)
    )

img.show()