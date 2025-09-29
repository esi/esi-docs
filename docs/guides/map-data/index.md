# Map Data

## General Information

Map data is available in the [SDE](../../services/static-data/index.md) or through [ESI](../../services/esi/overview.md).
Objects like regions, constellations, solarsystems, planets, moons, and other celestial bodies have a position.

There are two kinds of position, each using their own coordinate system:

* Relative to the center of the New Eden cluster. (Used by regions, constellations, solarsystems)
  The center of the cluster lies near Zarzakh, labelled "Point of No Return" on the in-game map. (See the red dot on the cluster map below)

* Relative to the center of a solarsystem. (used by planets, moons, stars, as well as other positions within a solarsystem such as killmails)
  The center of a solarsystem is it's star. The star objects themselves do not have an explicit position in the SDE or ESI, as their position is always `[0.0, 0.0, 0.0]`  
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

### Route calculation

ESI provides two routes for in-game navigation. The [`/route/`](/api-explorer#/operations/GetRouteOriginDestination) endpoint generates routes closely matching the ingame route planner.
And the [`/ui/autopilot/waypoint/`](/api-explorer#/operations/PostUiAutopilotWaypoint) endpoint enables setting the in-game autopilot destination without needing to calculate a route.

When not using ESI or more fine-grained control is desired, routes can be calculated manually from map data.

#### Stargate to stargate

Information about how systems are connected by stargates is available through both the SDE and ESI.  
In the SDE this data can be found in `mapStargates`.  
In ESI each solarsystem has a list of stargates (if present), whose destination may be retrieved from the [`/universe/stargates/` endpoint](/api-explorer#/operations/GetUniverseStargatesStargateId).

A graph can be constructed by taking each solarsystem as a node, and each stargate link as an edge. Each stargate of a pair linking two systems has a data entry in the SDE/ESI. These can be modelled as either a pair of edges in a directed graph, or merged into a single edge in an undirected graph.

With a graph, pathfinding algorithms like Dijkstra's Algorithm can be used. For A\*, the distance between solarsystems can be used as a heuristic, but this may yield different or suboptimal results.

Wormhole connections or player-constructed 'Ansiblex' jump gates can be added to this graph the same as stargates. Information about both of these connections is not available through the API.

!!! note

    Route calculation may yield several alternative routes of the same (shortest) length. Some algorithms may inconsistently select between these and give different results for the same start and destination. The in-game route planner has no specific behaviour defined for this case.  
    Routes may be also differ depending on avoidance lists, security preference, and the use of wormhole connections or player-constructed 'Ansiblex'.

#### Jump drives

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

!!! note

    32-bit floating point numbers do not have enough precision to handle both the 'large' scale of the interstellar distances and the 'small' scale of interplanetary distances. This results in a loss of precision and graphical glitches on objects distant from the origin.  

    This problem can be mitigated by using 64-bit floating point numbers in rendering or using "Floating Origin" techniques if your graphics API only supports 32-bit rendering.


## Example: 2D map

To draw a 2D map of the universe, the 3D coordinates need to be transformed into 2D positions on an image. The transformation required varies depending on the coordinate system used by the image.

This example uses the common "top-left origin" coordinate system widely used in images & 2D graphics. Here the `(0,0)` origin lies in the top-left corner of the image, the X axis points **right** and the Y axis points **down**.

![](./image-coordinate-system.svg)

These image axes map onto the axes of the universe data as follows:

* X<sub>img</sub> = X<sub>eve</sub>
* Y<sub>img</sub> = -Z<sub>eve</sub>
* The Y<sub>eve</sub> coordinate is discarded to flatten the map vertically.

After this, the coordinates must be moved and resized to fit within the image canvas. This can be done by calculating a bounding box, subtracting the position of the top-left corner of the bounding box from each coordinate, then dividing by width or height of the bounding box. This yields a position in the range 0 to 1, which can then be multiplied by the image width or height to get a final pixel position.

--8<-- "snippets/examples/map-2d-cluster.md"

A 2D solarsystem map can be drawn through the same approach, but as the X-axis points in the opposite direction for celestial body coordinates, both the X<sub>eve</sub> and Z<sub>eve</sub> are negated:

* X<sub>img</sub> = -X<sub>eve</sub>
* Y<sub>img</sub> = -Z<sub>eve</sub>

!!! tip

    Use logarithmic scaling for maps of solarsystems, as the distances between objects span several orders of magnitude.
