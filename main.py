# hello

from hash_code_parser import *
from pprint import pprint


def solve(input_file_name):
    problem = parse_file(input_file_name)
    # pprint(problem)
    output = create_streets(
        problem["intersections_in"], int(problem["duration"]), problem["streets"]
    )
    with open("output_" + input_file_name, "w") as output_file:
        output_file.write(output)


def create_streets(intersections, time, streets_dict):
    res = str(len(intersections)) + "\n"
    for inter in intersections.items():
        res += inter[0] + "\n"
        if len(inter[1]) == 1:
            res += "1\n" + inter[1][0] + " " + str(time) + "\n"
        else:
            streets = sorted_streets(inter[1], streets_dict)
            num_streets = len(inter[1])
            res += (
                str(num_streets)
                + "\n"
                + "\n".join(
                    i + " " + str(num_streets - acc) for acc, i in enumerate(streets)
                )
                + "\n"
            )
    return res


def sorted_streets(streets, streets_dict):
    return sorted(streets, key=lambda s: streets_dict[s]["nb_use"] / streets_dict[s]["L"], reverse=True)


def main():
    for l in "abcdef":
        solve(l + ".txt")


def test_():
    solve("a.txt")


if __name__ == "__main__":
    main()
    # test_()
