# hello 

from hash_code_parser import *

def main():
    intersections = {0: [], 1: []}
    cars = {1: [], 2: []}
    streets = {"rue_lo": (0,1)}
    problem = parse_file('a.txt')
    print(problem)

if __name__ == '__main__':
    main()

