from collections import defaultdict


def sum_nb_use(streets):
    pass


def weights(intersections_in, streets):
    _weights = {}
    for i, intersection in intersections_in.items():
        total_use = max(sum(
            street['nb_use'] for street in streets.values() if street['name'] in intersection
        ), 1)

        min_nb_use = min(
            street['nb_use'] for street in streets.values() if street['name'] in intersection)

        min_percentage = min_nb_use / total_use

        my_factor = (1 / min_percentage) if min_percentage > 0 else 0

        def percentage_of(street_name):
            return streets[street_name]['nb_use'] / total_use

        _weights[int(i)] = {
            name: percentage_of(name) * my_factor
            for name in intersection
        }

    return _weights


def parse_file(file_name):
    with open(file_name, 'r') as my_file:
        lines = my_file.read().splitlines()
        first_line = lines[0].split(' ')
        duration = first_line[0]
        nb_intersections = int(first_line[1])
        nb_streets = int(first_line[2])
        nb_car = int(first_line[3])
        intersections = defaultdict(list)
        intersections_in = defaultdict(list)
        intersections_out = defaultdict(list)
        streets = {}
        cars = {}
        for line in lines[1:nb_streets + 1]:
            words = line.split(' ')
            street_name = words[2]
            streets[street_name] = {
                'L': int(words[3]),
                'start': int(words[0]),
                'end': int(words[1]),
                'name': street_name,
                'nb_use': 0
            }
            intersections[words[0]].append(street_name)
            intersections[words[1]].append(street_name)
            intersections_in[words[1]].append(street_name)
            intersections_out[words[0]].append(street_name)
        for i, line in enumerate(lines[nb_streets + 1:]):
            words = line.split(' ')
            cars[i] = words[1:]
            for street_name in words[1:]:
                streets[street_name]['nb_use'] += 1
        black_list = {street['name'] for _, street in streets.items() if street['nb_use'] == 0}
        return {
            'duration': duration,
            'nb_intersections': nb_intersections,
            'nb_streets': nb_streets,
            'nb_car': nb_car,
            'intersections': intersections,
            'streets': streets,
            'cars': cars,
            'intersections_in': intersections_in,
            'intersections_out': intersections_out,
            'black_list': black_list,
            'weights': weights(intersections_in, streets)
        }
