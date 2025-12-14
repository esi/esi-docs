import json
from PIL import Image, ImageDraw # Using 'Pillow' for image drawing.

# Load data from SDE; `system_coordinates` as a list of `(x, y, z)` tuples
system_coordinates = []
with open("./mapSolarSystems.jsonl", encoding="utf8") as f:
    for line in f:
        system = json.loads(line)
        if int(system["_key"]) <= 30_999_999:    # "_key" is the solarSystemID; Load only the systems in the New Eden cluster
            system_coordinates.append((system["position"]["x"], system["position"]["y"], system["position"]["z"]))


# Image config
IMG_SIZE = 1024
STAR_RADIUS = 1

# Determine bounding-box
xMin, xMax, zMin, zMax = 0,0,0,0
for (x, y, z) in system_coordinates:
    xMin = min(xMin, x)
    xMax = max(xMax, x)
    zMin = min(zMin, z)
    zMax = max(zMax, z)

MAP_SIZE = max((xMax - xMin), (zMax - zMin))
ASPECT_RATIO = (xMax - xMin) / (zMax - zMin) # The cluster is not perfectly square, adjust image width to match aspect ratio to avoid the map becoming 'stretched' into a square

img = Image.new("RGBA", (int(IMG_SIZE * ASPECT_RATIO), IMG_SIZE), (0, 0, 0, 255))
draw = ImageDraw.Draw(img)

for (x, y, z) in system_coordinates:
    draw.circle(
        (
            # To convert the coordinates from 3D to pixel positions:
            # 1) Subtract the minimum value to set the lowest value to 0.0
            # 2) Divide by MAP_SIZE (the difference between max and minimum value) to set the highest value to 1.0
            #    This places all X coordinates in the range 0.0 - 1.0
            # 3) Multiply by IMAGE_SIZE, placing all X coordinates in the range 0.0 to IMG_SIZE, in pixels
            (x-xMin)/MAP_SIZE * IMG_SIZE,
            # Repeated for the Z coordinate, which is inverted as the map coordinate axis points in the opposite direction as the pixel coordinates.
            # Accordingly, the maximum ("least negative") value is subtracted instead
            (-(z-zMax))/MAP_SIZE * IMG_SIZE
        ),
        STAR_RADIUS,
        fill=(255, 255, 255, 255)
    )

img.show()