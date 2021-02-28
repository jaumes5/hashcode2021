def get_max_cars(streets_dict):
    best = 0
    for val in streets_dict.values():
        if val["nb_use"] > best:
            best = val["nb_use"]
    return best


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
