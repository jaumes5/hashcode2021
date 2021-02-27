from collections import defaultdict


def parse_file(file_name):
    with open(file_name, "r") as my_file:
        lines = my_file.read().splitlines()
        first_line = lines[0].split(" ")
        duration = first_line[0]
        nb_intersections = int(first_line[1])
        nb_streets = int(first_line[2])
        nb_car = int(first_line[3])
        points = int(first_line[4])
        intersections = defaultdict(list)
        intersections_in = defaultdict(list)
        intersections_out = defaultdict(list)
        streets = {}
        cars = {}
        for line in lines[1 : nb_streets + 1]:
            words = line.split(" ")
            street_name = words[2]
            streets[street_name] = {
                "L": int(words[3]),
                "start": int(words[0]),
                "end": int(words[1]),
                "name": street_name,
                "nb_use": 0,
            }
            intersections[words[0]].append(street_name)
            intersections[words[1]].append(street_name)
            intersections_in[words[1]].append(street_name)
            intersections_out[words[0]].append(street_name)
        for i, line in enumerate(lines[nb_streets + 1 :]):
            words_bis = line.split(" ")
            cars[i] = words_bis[1:]
            for street_name in words_bis[1:]:
                streets[street_name]["nb_use"] += 1
        black_list = {
            street["name"] for _, street in streets.items() if street["nb_use"] == 0
        }
        for inter in intersections_in.keys():
            intersections_in[inter] = [
                i for i in intersections_in[inter] if i not in black_list
            ]
        return {
            "duration": duration,
            "nb_intersections": nb_intersections,
            "nb_streets": nb_streets,
            "nb_car": nb_car,
            "intersections": intersections,
            "streets": streets,
            "cars": cars,
            "intersections_in": intersections_in,
            "intersections_out": intersections_out,
            "black_list": black_list,
            "points": points,
            # 'weights': weights(intersections_in, streets)
        }
