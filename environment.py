import gym
import utils
import numpy as np
from main import generate_cars


class TrafficControlEnv(gym.Env):

    def __init__(self, intersections: dict[str, utils.Intersection],
                 roads: dict[str, utils.Road], cars: list[utils.Car],
                 config: dict):

        self.intersections = list(intersections.values())
        self.roads = list(roads.values())
        self.cars = cars
        self.all_cars = len(self.cars)

        self.orig_inter = intersections
        self.orig_roads = roads

        self.config = config

        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(intersections) * 3 + 1, ), dtype=np.int32)
        self.action_space = gym.spaces.Box(low=10, high=180, shape=(len(intersections) * 2,), dtype=np.int32)

        self.wait_arr = []

    def step(self, action: np.ndarray):

        average_wait_time = np.median([[inter.i_y, inter.i_x] for inter in self.intersections])

        action_intersections = np.split(action, len(action) / 2)
        for intersection, actions in zip(self.intersections, action_intersections):
            intersection.move_cars()
            intersection.update(actions)

        updated_cars = []
        for car in self.cars:
            car.update()
            if car.at_destination:
                # print(car.destination.cars)
                # print(f"{car.id} is arrived at {car.destination}! Car wait time: {car.total_wait_time}, "
                #       f"total traveled distance: {car.total_traveled_distance}, total travel time: {car.total_travel_time}")
                self.wait_arr.append(car.total_wait_time)
                del car
                continue
            updated_cars.append(car)
        self.cars = updated_cars

        observations = []
        for intersection in self.intersections:
            observations.extend([intersection.t_switch,
                                 intersection.i_x,
                                 intersection.i_y
                                 ])
        median_wait_time = np.median(self.wait_arr) if self.wait_arr else 0
        observations.append(median_wait_time if self.wait_arr else average_wait_time)
        is_done = True if not self.cars else False
        reward = self.all_cars / median_wait_time if median_wait_time != 0 else average_wait_time
        return observations, reward, is_done, False, {}

    def reset(self):
        for inter in self.intersections:
            inter.i_x, inter.i_y = np.round(
                self.config['interval_sigma'] * np.random.randn(2) + self.config['interval_mu'], 0)
        self.cars = list(generate_cars(self.orig_roads, self.orig_inter).values())
        self.all_cars = len(self.cars)
        self.wait_arr = []

        observations = []
        for intersection in self.intersections:
            observations.extend([intersection.t_switch,
                                 intersection.i_x,
                                 intersection.i_y
                                 ])
        observations.append(0)
        return observations, 0, False, False, {}


    def render(self, mode="human"):
        pass
