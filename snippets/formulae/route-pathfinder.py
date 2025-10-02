import heapq

# This is a simplified implementation of a pathfinder algorithm, and only serves as example.
def find_path(origin_system, destination_system):
    open_list = []
    closed_list = {}
    heapq.heappush(open_list, (0, None, origin_system))

    while len(open_list) > 0:
        current_cost, current_parent, current_system = heapq.heappop(open_list)
        if current_system in closed_list:
            # This system was already seen with a lower cost.
            continue
        closed_list[current_system] = current_parent

        if current_system == destination_system:
            return build_path(closed_list, current_system)

        for neighbour in get_neighbours(current_system):
            if neighbour in closed_list:
                continue

            # define cost_fn() to calculate the cost. There are examples below.
            cost = current_cost + cost_fn(current_system, neighbour)
            heapq.heappush(open_list, (cost, current_system, neighbour))

# Reverse-walk the closed list to find the shortest path.
def build_path(closed_list, current_system):
    path = []
    while current_system is not None:
        path.append(current_system)
        current_system = closed_list[current_system]
    return path[::-1]

# Implement this yourself.
def get_neighbours(system):
    raise NotImplementedError("get_neighbours is not implemented")
