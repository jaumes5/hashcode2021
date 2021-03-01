import copy
import random
import time as time_packet
import bisect

from utils import get_max_cars, sorted_streets, intersection_parser, find_element


def create_streets(
    intersections,
    time,
    streets_dict,
    init_state,
    cars,
    points,
    number_of_generations=3,
    mutate_best=False,
):
    nb_unsuccessful_generations = 0
    best_score = -1
    best_res = ""
    generation_count = 0
    # max_cars = get_max_cars(streets_dict)
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
                if generation_count == 0 or mutate_best is False:
                    streets_time = total_random(streets, time, streets_dict)
                else:
                    streets_time = mutate_prev_generation(
                        streets, time, max_cars, best_res
                    )
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


def mutate_prev_generation(streets, time, max_cars, prev):
    return []


def total_random(streets, time, streets_dict):
    tmp_streets = streets.copy()
    random.shuffle(tmp_streets)
    avail_time = time
    streets_time = []
    for i in tmp_streets:
        if avail_time == 0:
            break
        tmp_time = random.randint(0, min(streets_dict[i]["nb_use"], avail_time))
        avail_time -= tmp_time
        if tmp_time != 0:
            streets_time.append(i + " " + str(tmp_time))
    return streets_time


def end_road_calc(end_road, iterations, i, points):
    score = 0
    for pos in range(len(end_road) - 1, -1, -1):
        if end_road[pos] - 1 <= 0:
            score += iterations - i + points
            end_road.pop(pos)
        else:
            end_road[pos] -= 1
    return score


def calc_score(iterations, initial_state, cars, streets, points, res_file):
    intersection_movements = intersection_parser(res_file)
    actual_street_inter = {i: j[0].copy() for i, j in intersection_movements.items()}
    cars_in_movement = {j: [] for j in initial_state.keys()}
    end_road = []
    score = 0
    loop_time = [0, 0, 0]
    for i in range(iterations):
        start = time_packet.time()
        score += end_road_calc(end_road, iterations, i, points)
        loop_time[0] += time_packet.time() - start
        start = time_packet.time()
        # TODO IMPORTANT optimize this loop
        for street in cars_in_movement.keys():
            for car_mov in range(len(cars_in_movement[street]) - 1, -1, -1):
                if cars_in_movement[street][car_mov][0] - 1 <= 0:
                    tmp_car = cars_in_movement[street].pop(car_mov)
                    initial_state[street].append(tmp_car[1])
                else:
                    cars_in_movement[street][car_mov][0] -= 1
        loop_time[1] += time_packet.time() - start
        start = time_packet.time()
        # TODO optimize this loop
        for inter in actual_street_inter.keys():
            street = actual_street_inter[inter][0]
            if initial_state[street]:
                car = initial_state[street].pop(0)
                if cars[car].index(street) + 2 < len(cars[car]):
                    cars_in_movement[cars[car][cars[car].index(street) + 1]].append(
                        [
                            streets[cars[car][cars[car].index(street) + 1]]["L"],
                            car,
                        ]
                    )
                else:
                    end_road.append(
                        streets[cars[car][cars[car].index(street) + 1]]["L"]
                    )
            if actual_street_inter[inter][1] <= 1:
                tmp = intersection_movements[inter]
                pos = find_element(tmp, street)
                actual_street_inter[inter] = tmp[(pos + 1) % len(tmp)].copy()
            else:
                actual_street_inter[inter][1] -= 1
        loop_time[2] += time_packet.time() - start
    score += end_road_calc(end_road, iterations, iterations, points)
    for i, j in enumerate(loop_time):
        # print("Loop {} took {} minutes and {} seconds".format(i, int(j // 60), j % 60))
        pass
    return score
