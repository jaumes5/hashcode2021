import copy
import bisect
import random


def create_streets(
    intersections,
    time,
    streets_dict,
    blacklist,
    init_state,
    cars,
    points,
    number_of_generations=3,
):
    max_time = min(10, time)
    nb_unsuccessful_generations = 0
    best_score = 0
    best_res = ""
    generation_count = 0
    while nb_unsuccessful_generations < number_of_generations:
        res = ""
        inter_count = 0
        for inter in intersections.items():
            if len(inter[1]) == 1:
                res += inter[0] + "\n"
                res += "1\n" + inter[1][0] + " " + str(time) + "\n"
                inter_count += 1
            else:
                streets = sorted_streets(inter[1], streets_dict)
                num_streets = len(inter[1])
                avail_time = time
                streets_time = []
                for i in streets:
                    if avail_time == 0:
                        break
                    tmp_time = random.randint(0, avail_time)
                    avail_time -= tmp_time
                    if tmp_time != 0:
                        streets_time.append(i + " " + str(tmp_time))
                if len(streets_time) > 0:
                    res += inter[0] + "\n"
                    res += (
                        str(len(streets_time)) + "\n" + "\n".join(streets_time) + "\n"
                    )
                    inter_count += 1
        res = str(inter_count) + "\n" + res
        tmp_score = calc_score(
            time, copy.deepcopy(init_state), cars, streets_dict, points, res
        )
        if tmp_score > best_score:
            print("NEW RECORD!")
            best_score = tmp_score
            best_res = res
            nb_unsuccessful_generations = 0
        else:
            nb_unsuccessful_generations += 1
        if generation_count % (max(1, number_of_generations // 10)) == 0:
            print(
                "Generation {}, best score {} points".format(
                    generation_count, best_score
                )
            )
        generation_count += 1
    print("BEST SCORE: " + str(best_score))
    return best_res


def sorted_streets(streets, streets_dict):
    return sorted(
        streets,
        key=lambda s: streets_dict[s]["nb_use"] / streets_dict[s]["L"],
        reverse=True,
    )


def intersection_parser(res_file):
    file_split = res_file.split("\n")
    inter_dict = {}
    line_pos = 1
    for iter_count in range(int(file_split[0])):
        inter = int(file_split[line_pos])
        inter_dict[inter] = []
        line_pos += 1
        for street in range(int(file_split[line_pos])):
            line_pos += 1
            tmp = file_split[line_pos].split(" ")
            inter_dict[inter].append([tmp[0], int(tmp[1])])
        line_pos += 1
    return inter_dict


def find_element(two_d_list: list, element, pos=0):
    for pos_element, i in enumerate(two_d_list):
        if i[pos] == element:
            return pos_element
    return -1


def calc_score(iterations, initial_state, cars, streets, points, res_file):
    intersection_movements = intersection_parser(res_file)
    actual_street_inter = {i: j[0] for i, j in intersection_movements.items()}
    cars_in_movement = {j: [] for j in initial_state.keys()}
    end_road = []
    score = 0
    for i in range(iterations):
        for pos in range(len(end_road) - 1, -1, -1):
            if end_road[pos] - 1 <= 0:
                score += iterations - i + points
                end_road.pop(pos)
            else:
                end_road[pos] -= 1
        for street in cars_in_movement.keys():
            for car_mov in range(len(cars_in_movement[street]) - 1, -1, -1):
                if cars_in_movement[street][car_mov][0] - 1 <= 0:
                    tmp_car = cars_in_movement[street].pop(car_mov)
                    initial_state[street].append(tmp_car[1])
                else:
                    cars_in_movement[street][car_mov][0] -= 1
        for inter in actual_street_inter.keys():
            street = actual_street_inter[inter][0]
            if initial_state[street]:
                car = initial_state[street].pop(0)
                if cars[car].index(street) + 2 < len(cars[car]):
                    bisect.insort(
                        cars_in_movement[cars[car][cars[car].index(street) + 1]],
                        [
                            streets[cars[car][cars[car].index(street) + 1]]["L"],
                            car,
                        ],
                    )
                else:
                    end_road.append(
                        streets[cars[car][cars[car].index(street) + 1]]["L"]
                    )
            if actual_street_inter[inter][1] <= 1:
                tmp = intersection_movements[inter]
                pos = find_element(tmp, street)
                actual_street_inter[inter] = tmp[(pos + 1) % len(tmp)]
            else:
                actual_street_inter[inter][1] -= 1
    return score
