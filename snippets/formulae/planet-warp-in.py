import math
import random


def warpin(id, x, y, z, r):
    j = (random.Random(id).random() - 1.0) / 3.0
    t = math.asin(x / abs(x) * (z / math.sqrt(x**2 + z**2))) + j
    s = 20.0 * (1.0 / 40.0 * (10 * math.log10(r / 10**6) - 39)) ** 20.0 + 1.0 / 2.0
    s = max(0.5, min(s, 10.5))
    d = r * (s + 1) + 1000000

    return (x + d * math.sin(t), y + 1.0 / 2.0 * r * math.sin(j), z - d * math.cos(t))
