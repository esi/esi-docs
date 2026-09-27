# Map Data

## General Information

Map data is available in the [SDE](../../services/static-data/index.md) or through [ESI](../../services/esi/overview.md).
Objects like regions, constellations, solarsystems, planets, moons, and other celestial bodies have a position.

There are two kinds of position, each using their own coordinate system:

* Relative to the center of the New Eden cluster. (Used by regions, constellations, solarsystems)<br>
  The center of the cluster lies near Zarzakh, labelled "Point of No Return" on the in-game map. (See the red dot on the cluster map below)<br>
  For systems in the New Eden Cluster both a 'geographic' position and a 'schematic' position ("position2D") is provided. The former is the actual position of the solarsystem, used for jump range calculations and the in-game 3D map. The latter is used for the in-game 2D map.

* Relative to the center of a solarsystem. (used by planets, moons, stars, as well as other positions within a solarsystem such as killmails)<br>
  The center of a solarsystem is it's star. The star objects themselves do not have an explicit position in the SDE or ESI, as their position is always `[0.0, 0.0, 0.0]`<br>
  Not every solarsystem has a star object; for abyssal deadspace systems with neither star nor planet, the origin is an arbitrary point.

These coordinate systems have the same scale (1.0 = 1 meter), but different directions.

## Universe

All regions, constellations, and solarsystems share a single coordinate system.

The SDE contains map data in the `map`-prefixed files, such as `mapRegions`, `mapConstellations`, and `mapSolarSystems`.
ESI provides this data through endpoints under the `/universe/` such as [`/universe/regions/`](/api-explorer#/operations/GetUniverseRegions).

For both SDE and ESI, data is provided for all kinds ('known space', 'wormhole space', 'abyssal space') of space. Different kinds of space can be identified by the [ID ranges](../../guides/id-ranges.md) for the regionID, constellationID or solarSystemID.
Only the 'New Eden' solarsystems (`SolarSystemID` in the range `30,000,000 to 30,999,999`) are included on the in-game map.

### Map

When displayed by the in-game map & most community maps, the mapping convention is to look "top down" oriented with the region of 'Venal' at the top as a "Space&nbsp;North". In this orientation, the coordinates have the following directions:

* `+X` is East/Right, `-X` is West/Left.
* `+Y` is Up, `-Y` is Down.
* `+Z` is North/Forward, `-Z` is South/Backward

!!! note

    This forms a **Left**-Handed coordinate system. If you are using a 3D graphics or geometry library, it may expect either Left- or Right-Handed coordinates. Using incorrect handedness results in a 'mirrored' image which rotations alone cannot correct. You can convert handedness by negating a single axis. (e.g. `[X, Y, -Z]`)

![New Eden map](./cluster_map.png)

### 2D 'schematic' Map

The 2D 'schematic' positions follow the same conventions, with the position2D `X` coordinate pointing in the same direction as the 3D position `X` coordinate, and position2D `Y` coordinate pointing in the same direction as the 3D position `Z` coordinate.

![New Eden '2D' diagram map](./cluster_map_2d.png)

### Route calculation

See [Route Calculation](../route-calculation.md) for details how to calculate a route in New Eden.

### Jump drives

Unlike stargate connections, jump drives can reach any valid system within range in a single jump. Jump drives allow jumping *to* any low- and nullsec system, with the exclusion of Pochven and the Jove regions. Ships can also jump *from* high-sec space into low- or nullsec.
Jump drive range is determined by the ship the player is piloting and their 'Jump Drive Calibration' skill.

A graph can be built by linking each solarsystem to every other solar system that may be jumped to.
For a given system<sub>1</sub> and system<sub>2</sub> and their positions (x, y, z), the systems are in jump range if:

$\sqrt{\left(x_1-x_2\right)^2+\left(y_1-y_2\right)^2+\left(z_1-z_2\right)^2}\le\ (Jump\ range\ in\ LY\ \ast\ {9\,460\,000\,000\,000\,000.0})$

!!! warning "Caution"

    For the purposes of jump drive range calculation, a single lightyear is exactly `9,460,000,000,000,000.0` (9.46 × 10^15) meters, slightly less than the real world scientific definition of a lightyear.
    Using the incorrect value may cause routes to include impossible jumps.


## Solarsystem

Each individual solar system in the game has its own isolated coordinate system, with planets & other celestial objects having their positions given relative to the star.

When matching the 'Space North' orientation as used by the in-game map (see above), the coordinate system is as follows:

In this orientation, the coordinates have the following directions:

* `+X` is West/Left, `-X` is East/Right.
* `+Y` is Up, `-Y` is Down.
* `+Z` is North/Forward, `-Z` is South/Backward.

!!! note

    This is different to the Universe's coordinate system, and is **Right**-Handed.

![Jita System map](./system_map.png)

### Combining the coordinate systems

Both coordinate systems have the same scale but different axes. To get the position of a planet within the larger 'universe' coordinate system, it's position can be added to that of the parent star with the x coordinate negated:
x = x<sub>system</sub> - x<sub>planet</sub>
y = y<sub>system</sub> + y<sub>planet</sub>
z = z<sub>system</sub> + z<sub>planet</sub>

!!! note "Note: Floating point precision"

    32-bit floating point numbers do not have enough precision to handle both the 'large' scale of the interstellar distances and the 'small' scale of interplanetary distances when combining the position of stars and the celestial bodies orbiting them as described above.

    This problem can be mitigated by using 64-bit "double precision" floating point numbers.

    In 3D rendering or other situations where 64-bit numbers are unavailable, "Floating Origin" techniques can also mitigate this problem.

### Orbit paths

The in-game map shows planet's and moon's orbits. These orbit paths are not directly provided by the SDE or ESI, but can be calculated from either.

!!! abstract "Abstract: Orbits in EVE Online"

    Planet and Moon orbits in EVE Online are all perfectly circular with no eccentricity. (See Celestial Statistics note below)  
    Moon orbits use the same logic as planet orbits, but with the parent planet taking the role of the sun.
    
    When rendering orbit paths on a map, the orbit path is a circle in 3D space. Centered on the star, with a radius of the planet's distance to the sun, and a specific rotation `q` to intersect the planet.

    The orbit rotation is defined by the following steps:

    1. The orbit path circle is placed horizontally in the solarsystem's X-Z plane.
    2. The rotation is that which moves the point `(-radius, 0.0, 0.0)` onto the planet's position by rotating around the sun's position with the shortest arc.
    
    After applying this rotation to the circle, it now intersects the planet's position and has the same orbital inclination as on the in-game map.

!!! warning "Note: Celestial Statistics"

    Planet and moon orbits in EVE Online do not use the `statistics` field and `eccentricity` or `orbitRadius` values found in the SDE.

    The `orbitRadius` value is correct for only some *but not all* planets and moons, and must instead be calculated from the planet/moon position to obstain the correct value.

#### Formula

To calculate the rotation, the following formula is used:

1. Calculate orbit radius $r$, vector $\vec{V_0}$ pointing at $(-r, 0, 0)$, and vector $\vec{V_1}$ pointing at $Position_{planet}$. Both vectors 'normalized' to length 1
    $r=\|Position_{planet}-Position_{sun}\| = \sqrt{(x_{planet}-x_{sun})^2+(y_{planet}-y_{sun})^2+(z_{planet}-z_{sun})^2}$  
    $\vec{v_0}=\left[-1,0,0\right]$  
    $\vec{v_1}=\frac{Position_{planet}-Position_{sun}}{r}$
2. Calculate cross product $c$ and dot product $d$ of vectors $\vec{v_0}$ and $\vec{v_1}$  
    $\vec{c}=\vec{v_0} \times \vec{v_1}$  
    $d=\vec{v_0} \cdot \vec{v_1}$
3. Depending on desired representation:
    1. [Axis-Angle rotation]  
        Rotate around vector $\vec{c}$ by $\theta$ radians  
        $\theta=\arccos(d)$
    2. [Quaternion]  
        Calculate angle value $s$, then construct quaternion $q$ from components.  
        $s=\sqrt{2 \times (d+1)}$  
        $q = [q_x, q_y, q_z, q_w] = [c_x/s, c_y/s, c_z/s, s/2]$  

        !!! warning ""
            Quaternions may be stored in memory scalar-first `wxyz` or scalar-last `xyzw`, check the argument order for the library you're using.

    3. [Other]  
        Convert from axis-angle or quaternion.

For moons, substitute the parent planet for the sun and the moon for the planet in the above formulae.  
If only calculating orbits for planets rather than a general implementation, subtracting the sun's position may be omitted as that position is always (0, 0, 0)

#### Visualisation

<video controls>
  <source src="./Orbit-Visualization.mp4" type="video/mp4">
</video>

#### Example code implementation

--8<-- "snippets/examples/map-orbitpath.md"

## Example: 3D map rendered as an image

To draw a map of the universe, the 3D coordinates need to be transformed into 2D positions on an image. The transformation required varies depending on the coordinate system used by the image.

This example uses the common "top-left origin" coordinate system widely used in images & 2D graphics. Here the `(0,0)` origin lies in the top-left corner of the image, the X axis points **right** and the Y axis points **down**.

![](./image-coordinate-system.svg)

These image axes map onto the axes of the universe data as follows:

* X<sub>img</sub> = X<sub>eve</sub>
* Y<sub>img</sub> = -Z<sub>eve</sub>
* The Y<sub>eve</sub> coordinate is discarded to flatten the map vertically.

After this, the coordinates must be moved and resized to fit within the image canvas. This can be done by calculating a bounding box, subtracting the position of the top-left corner of the bounding box from each coordinate, then dividing by width or height of the bounding box. This yields a position in the range 0 to 1, which can then be multiplied by the image width or height to get a final pixel position.

--8<-- "snippets/examples/map-cluster.md"

The 2D "schematic" positions can be used similarly, with the 3D `Z` coordinate replaced by the 2D `Y` coordinate:

* X<sub>img</sub> = X<sub>eve</sub>
* Y<sub>img</sub> = -Y<sub>eve</sub>

A solarsystem map uses different axes; The X-axis points in the opposite direction for celestial body coordinates, both the X<sub>eve</sub> and Z<sub>eve</sub> are negated:

* X<sub>img</sub> = -X<sub>eve</sub>
* Y<sub>img</sub> = -Z<sub>eve</sub>

!!! tip

    Use logarithmic scaling for maps of solarsystems, as the distances between objects span several orders of magnitude.
