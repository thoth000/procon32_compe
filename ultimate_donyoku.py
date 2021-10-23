import numpy as np
import sys

dcol = {'U': 0, 'L': -1, 'D': 0, 'R': 1}
drow = {'U': -1, 'L': 0, 'D': 1, 'R': 0}

class Solver:
    def __init__(self, data):
        self.data = data
        self.width  = data.shape[1]
        self.height = data.shape[0]

        self.now_col, self.now_row = np.unravel_index(np.argmax(data), data.shape)[::-1]
        self.solution = [hex(self.now_col)[2:].upper() + hex(self.now_row)[2:].upper() + '\n']

        self.step = 0
        self.moves = 1

    def out(self, target, proc):
        return
        print(f'Step {self.step}')
        print(f'Now: {self.now_col, self.now_row} {proc} (Target: {target})')
        print(self.data)
        print()

    def get_route(self, dep, dest, obst, route=''):
        depa_col, depa_row = dep
        dest_col, dest_row = dest
        obst_col, obst_row = obst

        if depa_col == obst_col:
            if self.now_col == self.width - 1:
                return self.get_route((depa_col - 1, depa_row), dest, obst, route + 'L')
            else:
                return self.get_route((depa_col + 1, depa_row), dest, obst, route + 'R')

        if dest_row == obst_row:
            if dest_row == self.height - 1:
                return self.get_route(dep, (dest_col, dest_row - 1), obst, route) + 'D'
            else:
                return self.get_route(dep, (dest_col, dest_row + 1), obst, route) + 'U'

        if dest_row < depa_row:
            route += 'U' * (depa_row - dest_row)
        else:
            route += 'D' * (dest_row - depa_row)

        if dest_col < depa_col:
            route += 'L' * (depa_col - dest_col)
        else:
            route += 'R' * (dest_col - depa_col)

        return route

    def venture(self, route, target, out=True):
        for proc in route:
            if out:
                self.out(target, proc)

            new_col = (self.now_col + dcol[proc]) % self.width
            new_row = (self.now_row + drow[proc]) % self.height
            self.data[self.now_row][self.now_col], self.data[new_row][new_col] = self.data[new_row][new_col], self.data[self.now_row][self.now_col]
            self.now_col, self.now_row = new_col, new_row

            self.step += 1

        self.solution.append(route)

    def calc_target_coord(self, target):
        target_col, target_row = np.where(self.data == target)[::-1]
        return target_col[0], target_row[0]

    def setup(self, target):
        target_col, target_row = self.calc_target_coord(target)

        route = self.get_route((self.now_col, self.now_row), (target_col, target_row + 1), (target_col, target_row))
        if target_row == self.height - 1:
            route = self.get_route((self.now_col, self.now_row), (target_col, target_row - 1), (target_col, target_row)) + 'D'
        self.venture(route, target)

    def go_left(self, target, goal_col):
        target_col, _ = self.calc_target_coord(target)
        while target_col != goal_col:
            self.venture('LURDL', target)
            target_col, _ = self.calc_target_coord(target)

    def go_right(self, target, goal_col):
        target_col, _ = self.calc_target_coord(target)
        while target_col != goal_col:
            self.venture('RULDR', target)
            target_col, _ = self.calc_target_coord(target)

    def go_up(self, target, goal_row):
        target_col, target_row = self.calc_target_coord(target)
        while target_row != goal_row:
            route = 'ULDRU'
            if target_col == self.width - 1:
                route = 'URDLU'
            self.venture(route, target)
            target_col, target_row = self.calc_target_coord(target)

    def run(self):
        for row in range(self.height - 2):
            for col in range(self.width - 2):
                target = self.width * row + col
                goal_col = col
                goal_row = row
                target_col, target_row = self.calc_target_coord(target)

                if (target_col, target_row) == (goal_col, goal_row):
                    continue

                self.setup(target)
                if target_row == goal_row:
                    self.venture('ULDDR', target)

                if target_col > goal_col:
                    if target_col - goal_col < self.width - target_col + goal_col:
                        self.go_left(target, goal_col)
                    else:
                        self.go_right(target, goal_col)
                else:
                    if goal_col - target_col < self.width - goal_col + target_col:
                        self.go_right(target, goal_col)
                    else:
                        self.go_left(target, goal_col)

                self.venture('RU', target)
                self.go_up(target, goal_row)

            target = self.width * (row + 1) - 2
            goal_col = self.width - 1
            goal_row = target // self.width
            target_col, target_row = self.calc_target_coord(target)

            self.setup(target)

            if target_col > goal_col:
                if target_col - goal_col < self.width - target_col + goal_col:
                    self.go_left(target, goal_col)
                else:
                    self.go_right(target, goal_col)
            else:
                if goal_col - target_col < self.width - goal_col + target_col:
                    self.go_right(target, goal_col)
                else:
                    self.go_left(target, goal_col)

            self.venture('LU', target)
            self.go_up(target, goal_row)

            target = self.width * (row + 1) - 1
            goal_col = self.width - 1
            goal_row = target // self.width + 1
            target_col, target_row = self.calc_target_coord(target)

            route = 'D'
            if self.data[self.now_row + 1][self.now_col] == target:
                route = 'RDDLURULD'
            self.venture(route, target)
            self.setup(target)

            if target_col > goal_col:
                if target_col - goal_col < self.width - target_col + goal_col:
                    self.go_left(target, goal_col)
                else:
                    self.go_right(target, goal_col)
            else:
                if goal_col - target_col < self.width - goal_col + target_col:
                    self.go_right(target, goal_col)
                else:
                    self.go_left(target, goal_col)

            self.venture('LU', target)
            self.go_up(target, goal_row)

            self.venture('URD', target)

        for col in range(self.width - 2):
            target = (self.height - 1) * self.width + col
            goal_col = col
            goal_row = self.height - 2
            target_col, target_row = self.calc_target_coord(target)

            self.setup(target)

            self.go_left(target, goal_col)

            target = (self.height - 2) * self.width + col
            goal_col = col + 1
            goal_row = self.height - 2
            target_col, target_row = self.calc_target_coord(target)

            route = 'R'
            if self.data[self.now_row][self.now_col + 1] == target:
                route = 'URRDLULDR'
            self.venture(route, target)
            self.setup(target)

            self.go_left(target, goal_col)

            self.venture('LUR', target)

        route = 'RD'
        if self.data[-1][-1] == self.width * self.height - 2:
            route = 'DR'
        self.venture(route, self.width * self.height - 1)

        self.solution.insert(1, str(self.step) + '\n')

        
        route = ''
        target = 0
        if self.data[-1][-2] == self.width * (self.height - 1) - 1:
            route = 'UR'
            self.now_col -= 1
            target = self.width * (self.height - 1) - 1
        elif self.data[-2][-1] == self.width * self.height - 2:
            route = 'LD'
            self.now_row -= 1
            target = self.width * self.height - 2
        elif self.data[-1][-2] == self.width * (self.height - 1) - 2:
            route = 'U'
            self.now_col -= 1
            target = self.width * (self.height - 1) - 2
        elif self.data[-2][-1] == self.width * (self.height - 1) - 2:
            route = 'L'
            self.now_row -= 1
            target = self.width * (self.height - 1) - 2

        if len(route):
            self.moves += 1
            self.solution.append('\n' + hex(self.now_col)[2:].upper() + hex(self.now_row)[2:].upper() + '\n')
            self.solution.append(str(len(route)) + '\n')
            self.solution.append(route)

            self.venture(route, target)

        self.out('', '')

        self.solution.insert(0, str(self.moves) + '\n')
        return self.solution

if __name__ == "__main__":
    solution = []

    with open(sys.argv[2], 'r') as f:
        solution.append(f.read() + '\n')

    solution += Solver(np.loadtxt(sys.argv[1], dtype=int)).run()

    with open('solution.txt', 'w') as f:
        f.writelines(solution)
