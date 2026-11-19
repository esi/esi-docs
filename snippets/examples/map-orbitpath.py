import math
import numpy as np

def orbitpath_rotation(planet_position: tuple[float, float, float], sun_position: tuple[float, float, float]) -> tuple[float, float, float, float]:
    v0 = np.array([-1.0, 0.0, 0.0])
    v1 = np.array([planet_position[0] - sun_position[0], planet_position[1] - sun_position[1], planet_position[2] - sun_position[2]])
    v1 /= np.linalg.norm(v1)

    c = v0.cross(v1)
    d = v0.dot(v1)
    s = math.sqrt(2 * (1 + d))

    return c[0] / s, c[1] / s, c[2] / s, s / 2