import sys
import math


class coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class building:
    def __init__(self, bld_type: int, coordinates: coord):
        self.type = bld_type
        self.coordinates = coordinates

    def __str__(self) -> str:
        return f"{self.coordinates}: {self.type}"


class tube:
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

    def __str__(self) -> str:
        return f"{building_1} <-> {building_2}: {capacity}"


class teleport:
    @classmethod
    def build_cost(cls) -> float:
        return -5000

    def __init__(self, source: building, destination: building):
        self.begin = source
        self.end = destination

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination}: ∞"


class pod:
    @classmethod
    def build_cost(cls):
        return -1000

    def __init__(self, pod_id: int, path: list[int]):
        self.id = pod_id
        self.path = path[:]

    def destroy(self):
        return 750


class landing_pad:
    def __init__(self, id, coord: coord, astronauts: list[int]) -> None:
        self.id = id
        self.coordinates = coord
        self.astronauts = astronauts[:]


def calc_distance(coord_1: coord, coord_2: coord) -> float:
    return math.sqrt((coord_1.x - coord_2.x) ** 2 + (coord_1.y - coord_2.y) ** 2)


month = 1
all_data = {}
landing_pads = {}
buildings = {}
tubes = []
teleports = []
pod_routes = {}

# game loop
while True:
    num_routes = int(input())
    # process transport lines
    for i in range(num_routes):
        building_1, building_2, capacity = [int(j) for j in input().split()]
        if capacity == 0:
            teleports.append(teleport(buildings[building_1], buildings[building_2]))
        else:
            tubes.append(tube(buildings[building_1], buildings[building_2], capacity))

    num_pods = int(input())
    # process transport pods
    for i in range(num_pods):
        pod_properties = input()
        pod_id = pod_properties[0]
        pod_routes[pod_id] = pod(pod_id, pod_properties[2:])

    new_buildings = int(input())

    # process **new** buildings
    for i in range(new_buildings):
        building_properties = [int(x) for x in input().split()]

        if building_properties[0] == 0:
            pad_id, xCoord, yCoord, astro_count = building_properties[1:5]
            landing_pads[pad_id] = landing_pad(
                pad_id, (xCoord, yCoord), building_properties[5:]
            )
        else:
            bld_type, bld_id, xCoord, yCoord = building_properties
            buildings[bld_id] = building(bld_type, (xCoord, yCoord))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0 1 0 2")
