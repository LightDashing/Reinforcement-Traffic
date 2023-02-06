from environment import TrafficControlEnv
from collections import deque
import utils
import json
import numpy as np
from pathfinding import greedy, optimize_greedy_path
import uuid


with open("config/default.json", "r") as f:
    CONFIG = json.load(f)
with open("environments/example_1.json", "r") as f:
    ENV_CONF = json.load(f)

if CONFIG["set_seed"]:
    np.random.seed(CONFIG["seed"])


if __name__ == "__main__":
    roads = {}
    intersections = {}
    cars = {}
    cars_iter = 0
    for key, value in ENV_CONF["roads"].items():
        for inter in value["intersections"]:
            if not intersections.get(inter):
                i_x, i_y = np.round(CONFIG['interval_sigma'] * np.random.randn(2) + CONFIG['interval_mu'],3)
                intersections[inter] = utils.Intersection(inter, [], [], [],
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
                                connected_roads_s=set())

    for key, value in ENV_CONF["intersections"].items():
        intersections[key].roads = [roads[road] for road in value["roads"]]
        intersections[key].roads_x = [roads[road] for road in value["roads_x"]]
        intersections[key].roads_y = [roads[road] for road in value["roads_y"]]
        intersections[key].set_current(np.random.choice([0, 1]))

    for key, value in roads.items():
        roads[key].connected_roads_l = [roads[r_id] for r_id in value.connected_roads_l]
        roads[key].connected_roads_s = set(roads[key].connected_roads_l)

    if not CONFIG["fully_connected"]:
        edge_roads = [road for road in roads.values() if len(road.intersections) < 2]

        for road in edge_roads:
            cars_amount = int(np.round(CONFIG['roads_cars_sigma'] * np.random.randn() + CONFIG['roads_cars_mu'], 0))
            for i in range(cars_amount):
                new_car = utils.Car(
                    id=str(uuid.uuid4()),
                    position=0,
                    speed=16.67,
                    curr_road=road,
                    destination=np.random.choice(list(filter(lambda x: x != road, edge_roads))),
                    path=None,
                    curr_intersection=None,
                    acc_time=CONFIG["average_car_acc_time"]
                )
                if cars_iter <= CONFIG["start_cars_max_roads"]:
                    cars_iter += 1
                    cars[new_car.id] = new_car
                    roads[road.id].cars.append(new_car)

    for car_id, car in cars.items():
        path = greedy(car.curr_road, car.destination)
        if not CONFIG["fully_connected"]:
            path = optimize_greedy_path(path)
        path.pop(0)
        cars[car_id].path = path

    env = TrafficControlEnv(list(intersections.values()), list(roads.values()), list(cars.values()))
    for i in range(10_000):
        env.step(None)
        if len(env.cars) == 0:
            print(f"All cars arrived at destination at {i} second!")
            break
    # print(roads["road_1"].cars)
    # result = greedy(roads["road_11"], roads["road_4"])
    # print(result)
    # print(optimize_greedy_path(result))
    # for road in roads.items():
    #     print(road)
    # for inter in intersections.values():
    #     print([road.connected_roads_l for road in inter.roads])
    #print(*[inter.roads for inter in intersections.values()])