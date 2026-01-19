# Route Calculation

When navigating New Eden, you need to find the best route from system A to system B. The in-game route planner offers several options to customize your pathfinding:

- **Route preference**: shorter, safer, or less-secure.
- **Security penalty**: how strictly to apply the route preference.

If you want to implement this in your own application, there are two main approaches:

1. **Use ESI** - Simple and straightforward, perfect for occasional route calculations.
2. **Write your own** - More complex but preferred for applications that need to perform many route calculations.

This guide covers both approaches, starting with the simpler ESI option.

## Using ESI

The simplest way to calculate routes is to use [EVE's ESI `/route` route](/api-explorer#/operations/PostRoute). This closely matches the in-game route planner behavior without requiring you to implement pathfinding algorithms.

The route accepts the following parameters (either via query-parameters or via request-body JSON):

- **Origin system ID**: System to start the route from.
- **Destination system ID**: System to end the route at.
- **Route preference**: `Shorter`, `Safer`, or `LessSecure`.
- **Security penalty**: Value controlling how strictly to apply the route preference.

This route returns a list of system IDs representing the calculated route.

### Example Usage

--8<-- "snippets/examples/esi-get-route.md"

## Writing Your Own

When implementing your own route calculation system, you need to understand how pathfinding algorithms work and how to model New Eden's transportation network.

### Pathfinding Algorithms

Pathfinding algorithms treat New Eden as a graph where:

- **Nodes** represent solar systems.
- **Edges** represent connections between systems (stargates, wormholes, etc.).

The most common pathfinding algorithms are:

- **[Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)**: Guarantees finding the shortest path but can be slower for large graphs.
- **[A* Search](https://en.wikipedia.org/wiki/A*_search_algorithm)**: More efficient than Dijkstra when you have a good heuristic.

Most programming languages have libraries that implement these algorithms, or you can implement them yourself if you need more control over the behavior.

!!! note "Important: A* Heuristic Considerations"

    A\* requires a heuristic function (H-value) that estimates the remaining cost to reach the destination. This heuristic must **never overestimate** the actual cost, or A\* won't guarantee finding the optimal route.

    In New Eden, creating an accurate heuristic is challenging because:

    - Systems may appear closer in 3D space but require longer routes due to gate connections.
    - "Pocket space" regions can create misleading distance calculations.

    **Recommendation**: Set the heuristic value to zero for A\* in EVE route calculation. This effectively makes A\* behave like Dijkstra's algorithm, ensuring optimal routes.

### Reading Static Data

To build your route calculation system, you need data about systems, their connections, and their security status.
This information is available in the [Static Data](../services/static-data/index.md) export (SDE).

The systems and their security status are available in the `mapSolarSystems` table.
The static connections are available the `mapStargates` table.

To create a graph for pathfinding:

1. **Load all systems** from `mapSolarSystems` to get the systems and their security status.
2. **Load all stargates** from `mapStargates` to get static connections between the systems.
3. **Create bidirectional edges** between connected systems.
4. **Add connections** for Ansiblex (player-owned jump bridges), Wormholes, or Shipcasters.

This graph can then be used with Dijkstra's algorithm or A* to find optimal routes based on your chosen cost function.

### Cost function

The cost function is the heart of your route calculation system. It determines how "expensive" each system transition is, influencing which route the algorithm will choose.
EVE Online provides three distinct cost function modes, each with different security preferences.

The snippet below serves as example for how cost functions can be used.

--8<-- "snippets/formulae/route-pathfinder.md"

#### Shorter

This mode finds the route with the fewest jumps, regardless of system security status.

--8<-- "snippets/formulae/route-shorter.md"

#### Safer

This mode prioritizes routes through high-security space, making longer routes acceptable if they avoid dangerous systems.
The lower the "security penalty" (0-100, default of 50), the more likely the route will use low-security or null-security space.

--8<-- "snippets/formulae/route-safer.md"

#### Less-Secure

This mode finds routes that prefers low-security space.
The lower the "security penalty" (0-100, default of 50), the more likely the route will use high-security or null-security space.

--8<-- "snippets/formulae/route-less-secure.md"
