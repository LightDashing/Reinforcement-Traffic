import collections

import environment
from collections import deque
import utils
import json
import numpy as np
from pathfinding import greedy, optimize_greedy_path
import uuid
import gc


with open("config/default.json", "r") as f:
    CONFIG = json.load(f)
with open("environments/example_1.json", "r") as f:
    ENV_CONF = json.load(f)

if CONFIG["set_seed"]:
    np.random.seed(CONFIG["seed"])


def generate_cars(roads: dict[str, utils.Road], intersections: dict[str, utils.Intersection]) -> dict[str, utils.Car]:
    cars = {}
    cars_iter = 0
    if not CONFIG["fully_connected"]:
        edge_roads = [road for road in roads.values() if len(road.intersections) < 2]
        destination_roads = edge_roads.copy()
        destination_roads.sort(key=lambda x: x.dest_priority)
        destination_roads = deque(destination_roads)

        max_cars = sum([road.spawn_cars_amount for road in roads.values() if road.ignore_spawn_limit]) + CONFIG["start_cars_max_roads"]

        dest_road = destination_roads.popleft()
        dest_cars = 0
        max_dest_cars = max_cars * (dest_road.dest_percent / 100) \
            if dest_road.dest_percent != 0 else len(edge_roads) * 100 / max_cars
        for road in edge_roads:
            if road.spawn_random:
                cars_amount = int(np.round(CONFIG['roads_cars_sigma'] * np.random.randn() + CONFIG['roads_cars_mu'], 0))
            else:
                cars_amount = road.spawn_cars_amount

            for i in range(cars_amount):
                new_car = utils.Car(
                    id=str(uuid.uuid4()),
                    position=0,
                    speed=16.67,
                    curr_road=road,
                    destination=dest_road,
                    #destination=np.random.choice(list(filter(lambda x: x != road, edge_roads))),
                    path=None,
                    curr_intersection=None,
                    acc_time=CONFIG["average_car_acc_time"]
                )
                if cars_iter > max_cars:
                    break
                cars_iter += 1
                dest_cars += 1
                cars[new_car.id] = new_car
                roads[road.id].cars.append(new_car)

                if dest_cars >= max_dest_cars:
                    if destination_roads:
                        dest_road = destination_roads.popleft()
                        dest_cars = 0
                        max_dest_cars = max_cars * (dest_road.dest_percent / 100) \
                            if dest_road.dest_percent != 0 else len(edge_roads) * 100 / max_cars

    # Statistics
    dests = collections.defaultdict(int)
    spawns = collections.defaultdict(int)

    for car_id, car in cars.items():
        path = greedy(car.curr_road, car.destination)
        dests[car.destination.id] += 1
        spawns[car.curr_road.id] += 1
        if not CONFIG["fully_connected"]:
            path = optimize_greedy_path(path)
        path.pop(0)
        cars[car_id].path = path

    print("Destinations distribution:", dests)
    print("Spawn distribution:", spawns, max_cars)

    return cars




if __name__ == "__main__":
    roads = {}
    intersections = {}
    cars = {}
    cars_iter = 0
    for key, value in ENV_CONF["roads"].items():
        for inter in value["intersections"]:
            if not intersections.get(inter):
                i_x, i_y = np.round(CONFIG['interval_sigma'] * np.random.randn(2) + CONFIG['interval_mu'], 0)
                intersections[inter] = utils.Intersection(inter, [], set([]), set([]),
                                                          i_x=i_x,
                                                          i_y=i_y,
                                                          t_x=0,
                                                          t_y=0,
                                                          c_x=deque(),
                                                          c_y=deque(),
                                                          car_flow=CONFIG["seconds_to_pass_intersection"])

        roads[key] = utils.Road(id=key,
                                intersections=[intersections[inter] for inter in value["intersections"]],
                                length=np.round(CONFIG['road_length_sigma']
                                                * np.random.randn() + CONFIG['road_length_mu'], 3),
                                speed_limit=CONFIG['speed_limit_meters'],
                                cars=[],
                                connected_roads_l=value["connected_roads"],
                                connected_roads_s=set(),
                                lanes=value["lanes_amount"],
                                spawn_random=value["spawn_random"],
                                ignore_spawn_limit=value["ignore_spawn_limit"],
                                spawn_cars_amount=value["spawn_cars_amount"],
                                can_be_destination=value["can_be_destination"],
                                dest_priority=value["dest_priority"],
                                dest_percent=value["dest_percent"])

    for key, value in ENV_CONF["intersections"].items():
        intersections[key].roads = [roads[road] for road in value["roads"]]
        intersections[key].roads_x = [roads[road] for road in value["roads_x"]]
        intersections[key].roads_y = [roads[road] for road in value["roads_y"]]
        intersections[key].set_current(np.random.choice([0, 1]))

    for key, value in roads.items():
        roads[key].connected_roads_l = [roads[r_id] for r_id in value.connected_roads_l]
        roads[key].connected_roads_s = set(roads[key].connected_roads_l)

    cars = generate_cars(roads, intersections)

    env = environment.TrafficControlEnv(intersections, roads, list(cars.values()), CONFIG)
    total_reward = 0
    for i in range(2):
        for j in range(10_000):
            _, reward, _, _, _ = env.step(np.round(CONFIG['interval_sigma'] * np.random.randn(len(intersections) * 2) + CONFIG['interval_mu'], 0))
            total_reward += reward
            if len(env.cars) == 0:
                print(f"All cars arrived at destination at {j} second!")
                break
        print(total_reward)
        total_reward = 0
        env.reset()
    print([len(road.cars) for road in env.roads])
    gc.collect()