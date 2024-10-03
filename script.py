import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class building():
    def __init__(self, bld_type, x_coord, y_coord):
        self.type = bld_type
        self.coord = coord(x_coord, y_coord)

class coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class tube():
    @classmethod
    def build_cost(cls, building_1: building, building_2: building) -> float:
        distance = calc_distance(building_1.coord, building_2.coord)
        cost = 0.1 * int(distance * 10) / 10
        return -cost

    def __init__(self, source: building, destination: building, capacity: int):
        self.endpoints = [source, destination]
        self.capacity = capacity

    def upgrade_cost(self) -> float:
        return tube.build_cost(self.endpoints[0], self.endpoints[1]) * (capacity + 1)

class teleport():
    @classmethod
    def build_cost(cls) -> float:
        return -5000

    def __init__(self, source: building, destination: building):
        self.begin = source
        self.end = destination

class pod():
    @classmethod
    def build_cost(cls):
        return -1000

    def __init__(self, pod_id: int, path: list[int]):
        self.id = pod_id
        self.path = path[:]

    def destroy(self):
        return 750


def calc_distance(coord_1: coord, coord_2: coord) -> float:
    return math.sqrt((coord_1.x - coord_2.x) ** 2  + (coord_1.y - coord_2.y) ** 2)


month = 1
all_data = {}
landing_pads = {}
buildings = {}
new_astronauts = []
# game loop
while True:
    month_data = {}

    month_data['available_resources'] = int(input())
    month_data['num_travel_routes'] = int(input())
    month_data['pod_routes'] = []
    month_data['transport_routes'] = []
    # process transport lines
    for i in range(month_data['num_travel_routes']):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        if capacity == 0:
            month_data['transport_routes'].append((building_id_1, building_id_2))
        else:
            month_data['pod_routes'].append((building_id_1, building_id_2, capacity))
    
    month_data['num_pods'] = int(input())
    month_data['pod_itineraries'] = {}
    # process transport pods
    for i in range(month_data['pods']):
        pod_properties = input()
        pod_id = pod_properties[0]
        itinerary_length = pod_properties[1]
        month_data['pod_itineraries'][pod_id] = pod_properties[2:]

    month_data['new_buildings'] = int(input())
    
    # process buildings
    for i in range(month_data['new_buildings']):
        building_properties = [int(x) for x in input().split()]

        if building_properties[0] == 0:
            pad_id, xCoord, yCoord, astro_count = building_properties[1:5]
            new_astronauts.extend(building_properties[5:])
        else:
            bld_type, bld_id, xCoord, yCoord = building_properties
            buildings[bld_id] = bld_type, xCoord, yCoord
            

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0 1 0 2")
