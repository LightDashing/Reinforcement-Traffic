from dataclasses import dataclass
from collections import deque


@dataclass
class Road:
    id: str
    intersections: list["Intersection"]
    connected_roads_s: set["Road"]
    connected_roads_l: list["Road"]
    cars: list["Car"]
    length: float
    speed_limit: float
    lanes: int  # right now there is no support for uneven lanes, so there is always lanes*2 total amount of road lanes
    spawn_random: bool  # if true, then spawns random amount of cars
    ignore_spawn_limit: bool # if true, then global car limit is ignored
    spawn_cars_amount: int  # if spawn_random true, uses this variable to spawn cars
    can_be_destination: bool  # right now doesn't work TODO: change how destinations_list is created
    dest_priority: int  # priority in destination generation queue
    dest_percent: int  # amount of cars from all pool to generate


    def __hash__(self):
        return hash(self.id + str(type(self)))

    def __eq__(self, other):
        return other and self.id == other.id

    # def __repr__(self):
    #     return f"<Id: {self.id}| Intersections: {[inter.id for inter in self.intersections]}| " \
    #            f"Connected: {[road.id for road in self.connected_roads_l]}>"

    def __repr__(self):
        return f"<Id: {self.id}>"


@dataclass
class Intersection:
    id: str

    roads: list[Road]
    roads_x: set[Road]
    roads_y: set[Road]

    i_x: float  # green-light interval for road x
    i_y: float  # green-light interval for road_y

    t_x: float  # average wait time for cars on x road
    t_y: float  # average wait time for cars on y road

    c_x: deque["Car"]  # amount of cars waiting on x road
    c_y: deque["Car"]  # amount of cars waiting on y road

    t_switch: int = 0  # current time, when t_switch == i_x or i_y, active line switches

    curr_active = None  # array, roads_x or roads_y
    curr_active_queue = None
    _curr_active_num: int = None  # 0 for road x, 1 for road y
    t_switch_max: float = None  # current max time, after which update change lanes
    car_flow: int = 3

    # def __repr__(self):
    #     return f"<Id: {self.id}| Roads: {[road.id for road in self.roads]}>"

    def __repr__(self):
        return f"<Id: {self.id}>"

    def __hash__(self):
        return hash(self.id + str(type(self)))

    def set_current(self, lane: int = 0):
        if lane == 0:
            self.curr_active = self.roads_x
            self.curr_active_queue = self.c_x
            self.t_switch_max = self.i_x
            self._curr_active_num = 0
        else:
            self.curr_active = self.roads_y
            self.curr_active_queue = self.c_y
            self.t_switch_max = self.i_y
            self._curr_active_num = 1

    def update(self):
        self.t_switch += 1
        if self.t_switch >= self.t_switch_max:
            if self._curr_active_num == 1:
                self.set_current()
            else:
                self.set_current(1)
            self.t_switch = 0

    def move_cars(self):
        if not self.curr_active_queue:
            return
        for road in self.curr_active:  # we move cars at each side of intersection
            for i in range(road.lanes):  # if road has more than one lane for each direction
                if self.t_switch % self.car_flow == 0:
                    if not self.curr_active_queue:
                        return
                    car = self.curr_active_queue.popleft()
                    car.pass_intersection()

    def add_car(self, car_road: Road, car: "Car"):
        if car_road in self.roads_x:
            self.c_x.append(car)
        else:
            self.c_y.append(car)

    def remove_car(self, car_road: Road):
        if car_road in self.roads_x:
            self.c_x.popleft()
        else:
            self.c_y.popleft()

    def is_allowed_move(self, road: Road, car: "Car") -> bool:
        if road in self.curr_active and self.curr_active_queue.index(car) == 0:
            return True
        else:
            return False


@dataclass
class Car:
    id: str
    position: float  # position on current road
    speed: float  # current speed
    curr_road: Road | None  # current road id
    destination: Road  # destination road id
    path: list[Road] | None  # path to destination road
    curr_intersection: Intersection | None  # current intersection id
    acc_time: float  # 0-60 km/h time

    # Different car statistics
    total_wait_time: float = 0
    total_traveled_distance: float = 0
    total_travel_time: float = 0

    at_destination = False

    def __hash__(self):
        return hash(self.id + str(type(self)))

    def get_current_intersection(self) -> Intersection:

        if self.curr_road.intersections == self.path[0].intersections:
            return self.curr_road.intersections[0]

        if len(self.curr_road.intersections) >= len(self.path[0].intersections):
            difference = list(set(self.curr_road.intersections) - set(self.path[0].intersections))[0]
            return list(filter(lambda x: x != difference, self.curr_road.intersections))[0]

        if len(self.curr_road.intersections) < len(self.path[0].intersections):
            difference = list(set(self.path[0].intersections) - set(self.curr_road.intersections))[0]
            return list(filter(lambda x: x != difference, self.path[0].intersections))[0]

    def pass_intersection(self):
        self.curr_intersection = None
        self.curr_road = self.path.pop(0)

        self.speed += self.curr_road.speed_limit / self.acc_time
        self.position = 0
        return

    def update(self):
        self.total_travel_time += 1
        if self.curr_intersection:
            self.speed = 0
            self.total_wait_time += 1
            return

        if self.position + self.speed < self.curr_road.length:
            self.position += self.speed
            self.total_traveled_distance += self.speed
            if self.speed < self.curr_road.speed_limit:
                self.speed += self.curr_road.speed_limit / self.acc_time
            return

        if self.curr_road == self.destination:
            self.at_destination = True
            return

        self.curr_intersection = self.get_current_intersection()
        self.curr_intersection.add_car(self.curr_road, self)
