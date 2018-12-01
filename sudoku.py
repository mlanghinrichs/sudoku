"""Interpret and solve a sudoku number puzzle."""
import random

class Sudoku():
    """A sudoku puzzle object."""

    def __init__(self, puzzle):
        self.raw = puzzle
        self.possibles = [[], [], [], [], [], [], [], [], []]
        self.update()

    def update(self):
        """Update rows, cols, and squares vars."""
        for i in range(9):
            self.__dict__["row" + str(i)] = self.raw[i]
            self.__dict__["col" + str(i)] = [row[i] for row in self.raw]
        for a in range(3):
            for b in range(3):
                self.__dict__[f"sqr{a}{b}"] = []
        for i in range(9):
            for j in range(9):
                rbox, cbox = str(i//3), str(j//3)
                self.__dict__[f"sqr{rbox}{cbox}"].append(self.raw[i][j])
        self.possibles = [[], [], [], [], [], [], [], [], []]
        for r in range(9):
            for c in range(9):
                if self.raw[r][c] != 0:
                    self.possibles[r].append([])
                    continue
                this_box = []
                for num in range(9):
                    if not (num+1 in self.__dict__["row" + str(r)]
                            or num+1 in self.__dict__["col" + str(c)]
                            or num+1 in self.__dict__[f"sqr{r//3}{c//3}"]):
                        this_box.append(num+1)
                self.possibles[r].append(this_box)

    def first_pass(self):
        initial = str(self.raw)
        for r in range(9):
            for c in range(9):
                if len(self.possibles[r][c]) == 1:
                    print(self.possibles[r][c])
                    self.raw[r][c] = self.possibles[r][c][0]
                    print(self.raw[r][c])
        self.update()
        return initial == str(self.raw)

    def row(self, *args):
        return self.__dict__["row" + str(args[0])]

    def col(self, *args):
        return self.__dict__["col" + str(args[0])]

    def square(self, *args):
        return (args[0]//3, args[1]//3)

    def __getitem__(self, key):
        # 0-indexed in both instances, as god intended
        if isinstance(key, int):
            # e.g. Sudoku[15] should get 1, 7
            row = key // 9
            col = key % 9
            return self.raw[row][col]
        elif isinstance(key, tuple):
            a, b = key
            return self.raw[a][b]

    def __str__(self):
        out = ""
        for row in self.raw:
            for num in row:
                out += str(num) + " "
            out = out[:-1] + "\n"
        out = out[:-1]
        return out

    @classmethod
    def random(cls):
        """Generate a random (potentially invalid) test sudoku."""
        nums = [i+1 for i in range(9)]
        puzz = []
        for i in range(9):
            random.shuffle(nums)
            puzz.append(list(nums))
        return cls(puzz)


test = Sudoku.random()
new = Sudoku([[0, 0, 4, 5, 0, 2, 0, 9, 0],
              [0, 1, 5, 0, 6, 0, 2, 0, 0],
              [0, 8, 2, 0, 1, 0, 0, 0, 0],
              [5, 2, 8, 1, 0, 0, 0, 0, 0],
              [7, 0, 0, 6, 0, 8, 0, 0, 1],
              [0, 0, 0, 0, 0, 3, 7, 8, 5],
              [0, 0, 0, 0, 4, 0, 6, 3, 0],
              [0, 0, 9, 0, 2, 0, 8, 1, 0],
              [0, 3, 0, 7, 0, 6, 5, 0, 0]])

extreme = Sudoku([[0, 0, 0, 0, 0, 1, 0, 0, 5],
                  [2, 1, 3, 0, 0, 0, 0, 7, 0],
                  [0, 0, 5, 0, 7, 0, 4, 2, 0],
                  [0, 0, 8, 5, 0, 4, 0, 0, 0],
                  [6, 0, 0, 0, 0, 0, 0, 0, 4],
                  [0, 0, 0, 7, 0, 9, 6, 0, 0],
                  [0, 4, 6, 0, 8, 0, 9, 0, 0],
                  [0, 9, 0, 0, 0, 0, 1, 4, 8],
                  [3, 0, 0, 4, 0, 0, 0, 0, 0]])

while not (extreme.first_pass()):
    print(extreme, "\n")

