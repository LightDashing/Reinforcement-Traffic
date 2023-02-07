import gym
import utils
import numpy as np


class TrafficControlEnv(gym.Env):

    def __init__(self, intersections: list[utils.Intersection], roads: list[utils.Road], cars: list[utils.Car]):
        self.intersections = intersections
        self.roads = roads
        self.cars = cars

        # self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(intersections) * 2 + 1, ), dtype=np.int32)
        # self.action_space = gym.spaces.Box(low=0, high=)

    def step(self, action):

        for intersection in self.intersections:
            intersection.move_cars()
            intersection.update()

        for car in self.cars:
            car.update()
            if car.at_destination:
                self.cars.remove(car)
                print(f"{car.id} is arrived at {car.destination}! Car wait time: {car.total_wait_time}, "
                      f"total traveled distance: {car.total_traveled_distance}, total travel time: {car.total_travel_time}")
                del car

    def reset(self):
        pass

    def render(self, mode="human"):
        pass
