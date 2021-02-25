
from collections import defaultdict


def parse_file(file_name):
    with open(file_name, 'r') as my_file:
        lines = my_file.read().splitlines()
        first_line = lines[0].split(' ')
        duration = first_line[0]
        nb_intersections = int(first_line[1])
        nb_streets = int(first_line[2])
        nb_car = int(first_line[3])
        intersections = defaultdict(list)
        streets = {}
        cars = {}
        for line in lines[1:nb_streets+1]:
            words = line.split(' ')
            streets[words[2]] = {
                'L': words[3],
                'start': words[0],
                'end': words[1],
                'name': words[2]
            }
            intersections[words[0]].append(words[2])
            intersections[words[1]].append(words[2])
        for i, line in enumerate(lines[nb_streets+1:]):
            words = line.split(' ')
            cars[i] = words[1:]
        return {
            'duration': duration,
            'nb_intersections': nb_intersections,
            'nb_streets': nb_streets,
            'nb_car': nb_car,
            'intersections': intersections,
            'streets': streets,
            'cars': cars,
        }