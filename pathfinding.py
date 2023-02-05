import utils


def greedy(start_road: utils.Road, end_road: utils.Road) -> list[utils.Road]:
    """
    Simple algorithm to greedily find path from start road to end road
    :param start_road: start point
    :param end_road: end point
    :return: list of roads in sequence to pass
    """
    curr_road = start_road
    path = [start_road]

    if end_road in start_road.connected_roads_s:
        return [start_road, end_road]

    while curr_road != end_road:

        if end_road in curr_road.connected_roads_s:
            path.append(end_road)
            return path

        min_length = max(item.length for item in curr_road.connected_roads_l) + 10
        next_road = None
        failsafe_road = curr_road.connected_roads_l[0]

        for road in curr_road.connected_roads_l:
            if road not in path and len(road.intersections) > 1:
                if road.length < min_length:
                    min_length = road.length
                    next_road = road
                else:
                    failsafe_road = road

        if next_road:
            path.append(next_road)
            curr_road = next_road
        else:
            path.append(failsafe_road)
            curr_road = failsafe_road

    return path


def optimize_greedy_path(greedy_path: list[utils.Road]) -> list[utils.Road]:
    modified_path = []
    redundant_el = None
    if len(greedy_path) > 2:
        try:
            for i in range(len(greedy_path)):
                if greedy_path[i] != redundant_el:
                    modified_path.append(greedy_path[i])
                if greedy_path[i] in greedy_path[i + 2].connected_roads_s:
                    redundant_el = greedy_path[i + 1]
        except IndexError:
            modified_path.append(greedy_path[-1])
            return modified_path
