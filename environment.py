import gym
import utils
import numpy as np
#from main import CONFIG


class TrafficControlEnv(gym.Env):

    def __int__(self, intersections: list[utils.Intersection], roads: list[utils.Road], cars: list[utils.Car]):
        self.intersections = intersections
        self.roads = roads
        self.cars = cars

    def step(self, action):

        for car in self.cars:
            if car.position + car.speed < car.curr_road.length:
                car.position += car.speed
                if car.speed < CONFIG["speed_limit_meters"]:
                    car.speed += CONFIG["speed_limit_meters"] / ["average_car_acc_time"]
            else:
                if len(car.curr_road.intersections) < 2:
                    car.curr_intersection = car.curr_road.intersections[0]
                else:
                    car.path

    def reset(self):
        pass

    def render(self, mode="human"):
        pass
