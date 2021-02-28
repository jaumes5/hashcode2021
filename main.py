# hello

from hash_code_parser import *
from pprint import pprint
from genetic import create_streets


def solve(input_file_name, dry_run=False):
    problem = parse_file(input_file_name)
    # pprint(problem)
    init_state = initial_state(problem["intersections_in"], problem["cars"])
    # pprint(init_state)

    output = create_streets(
        problem["intersections_in"],
        int(problem["duration"]),
        problem["streets"],
        problem["black_list"],
        init_state,
        problem["cars"],
        problem["points"],
    )
    if not dry_run:
        with open("output_" + input_file_name, "w") as output_file:
            output_file.write(output)
    else:
        print(output)


def initial_state(intersections_in, cars):
    res = {street: [] for _, streets in intersections_in.items() for street in streets}
    for car, street in cars.items():
        res[street[0]].append(car)
    return res


def main():
    for l in "abcdef":
        print(l)
        solve(l + ".txt")


def test_():
    solve("a.txt")
    # pprint(parse_file("a.txt"))
    # solve('a.txt', dry_run=True)


if __name__ == "__main__":
    main()
    # test_()
