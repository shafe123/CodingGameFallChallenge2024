import sys
import math


class coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class module:
    def __init__(self, bld_type: int, coordinates: coord, id: int):
        self.type = bld_type
        self.coordinates = coordinates
        self.id = id

    def __str__(self) -> str:
        return f"{self.coordinates}: {self.type}"


class landing_pad(module):
    def __init__(self, id, coord: coord, astronauts: list[int]) -> None:
        super().__init__(0, coord, id)
        self.astronauts = astronauts[:]


class building(module):
    def __init__(self, bld_type: int, coordinates: coord, id: int):
        super().__init__(bld_type, coordinates, id)


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


def calc_distance(coord_1: coord, coord_2: coord) -> float:
    return math.sqrt((coord_1.x - coord_2.x) ** 2 + (coord_1.y - coord_2.y) ** 2)


def point_intersect(point: coord, B: coord, C: coord):
    epsilon = 0.000001
    return (
        -epsilon
        < calc_distance(B, point) + calc_distance(point, C) - calc_distance(B, C)
        < epsilon
    )


def orientation(coord1: coord, coord2: coord, coord3: coord):
    prod = (coord3.y - coord1.y) * (coord2.x - coord1.x) - (coord2.y - coord1.y) * (
        coord3.x - coord1.x
    )
    return math.copysign(1, prod)


def segment_intersect(coord1: coord, coord2: coord, coord3: coord, coord4: coord):
    return (
        orientation(coord1, coord2, coord3) * orientation(coord1, coord2, coord4) < 0
        and orientation(coord3, coord4, coord1) * orientation(coord3, coord4, coord2)
        < 0
    )


def build_tube(source: building, destination: building):
    return f"TUBE {source.id} {destination.id}"


def build_pod(route: list[building], id: int = None):
    global next_route_id
    if not id:
        id = next_route_id
        next_route_id += 1
    return f"POD {id} " + " ".join([str(bldg.id) for bldg in route])


month = 1
all_data = {}
buildings: dict[building] = {}
tubes: list[tube] = []
teleports: list[teleport] = []
pod_routes: dict[pod] = {}
unvisited_modules: set[building] = set()
visited_modules: set[building] = set()
next_route_id = 1

# game loop
while True:
    available_resources = int(input())
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
            buildings[pad_id] = landing_pad(
                pad_id, coord(xCoord, yCoord), building_properties[5:]
            )
            visited_modules.add(buildings[pad_id])
        else:
            bld_type, bld_id, xCoord, yCoord = building_properties
            buildings[bld_id] = building(bld_type, coord(xCoord, yCoord), bld_id)
            unvisited_modules.add(buildings[bld_id])

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    actions = []

    # very simple, greedy approach
    # connect a tube to the closest already-connected building
    for mod in unvisited_modules:
        print(f"mod{mod.id}", file=sys.stderr, flush=True)
        # find nearest visited building
        minimum_distance = math.inf
        nearest_building = None
        for candidate in visited_modules:
            candidate_distance = calc_distance(mod.coordinates, candidate.coordinates)
            if candidate_distance < minimum_distance:
                nearest_building = candidate
                minimum_distance = candidate_distance

        if nearest_building:
            actions.append(build_tube(mod, nearest_building))
            actions.append(build_pod([mod, nearest_building, mod]))
            visited_modules.add(nearest_building)
            if nearest_building in unvisited_modules:
                unvisited_modules.remove(nearest_building)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    if actions:
        final_action = ";".join(actions)
    else:
        final_action = "WAIT"
    print(final_action)
    month += 1
