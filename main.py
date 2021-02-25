# hello 

from hash_code_parser import *
from pprint import pprint


def solve(input_file_name):
    problem = parse_file(input_file_name)
    # pprint(problem)
    output = create_streets(problem["intersections_in"], int(problem["duration"]))
    with open('output_' + input_file_name, 'w') as output_file:
        output_file.write(output)


def create_streets(intersections, time):
    res = str(len(intersections)) + "\n"
    for inter in intersections.items():
        res += inter[0] + "\n"
        if len(inter[1]) == 1:
            res += "1\n" + inter[1][0] + " " + str(time) + "\n"
        else:
            res += (str(len(inter[1])) +
                    "\n" +
                    "\n".join(i + " " + str(1) for i in inter[1]) +
                    "\n")
    return res


def main():
    for l in 'abcdef':
        solve(l + '.txt')


def test_():
    solve('a.txt')


if __name__ == '__main__':
    main()
    # test_()

