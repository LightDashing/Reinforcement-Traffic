from dataclasses import dataclass


@dataclass
class Road:
    id: str
    intersections: list["Intersection"]
    connected_roads_s: set["Road"]
    connected_roads_l: list["Road"]
    cars: list["Car"]
    length: float
    speed_limit: float

    def __hash__(self):
        return hash(self.id)

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

    c_x: list["Car"]  # amount of cars waiting on x road
    c_y: list["Car"]  # amount of cars waiting on y road

    t_switch: int = 0  # current time, when t_switch == i_x or i_y, active line switches

    curr_active = None  # 0 for road x, 1 for road y
    _curr_active_num: int = None
    t_switch_max: float = None  # current max time, after which update change lanes

    # def __repr__(self):
    #     return f"<Id: {self.id}| Roads: {[road.id for road in self.roads]}>"

    def __repr__(self):
        return f"<Id: {self.id}>"

    def set_current(self, lane: int = 0):
        if lane == 0:
            self.curr_active = self.roads_x
            self.t_switch_max = self.i_x
            self._curr_active_num = 0
        else:
            self.curr_active = self.roads_y
            self.t_switch_max = self.i_y
            self._curr_active_num = 1

    def update(self):
        self.t_switch += 1
        if self.t_switch >= self.t_switch_max:
            if self._curr_active_num == 1:
                self.set_current()
            else:
                self.set_current(0)
            self.t_switch = 0


    def is_allowed_move(self, road):
        if road in self.curr_active:
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
    total_wait_time: float = 0

    def update_position(self):
        if self.curr_intersection:
            if not self.curr_intersection.is_allowed_move(self.curr_road):
                self.total_wait_time += 1
                return
        if self.position + self.speed < self.curr_road.length:
            self.position += self.speed
            if self.speed < self.curr_road.speed_limit:
                self.speed += self.curr_road.speed_limit / self.acc_time
        else:
            pass

