"""Interpret and solve a sudoku number puzzle."""
import random

class Sudoku():
    """A sudoku puzzle object."""

    def __init__(self, puzzle):
        self.raw = puzzle
        self.possibles = [[], [], [], [], [], [], [], [], []]
        self.update()

    def update_dict(self, raw_or_poss="raw"):
        if raw_or_poss == "raw":
            pre = ""
            pull_from = self.raw
        elif raw_or_poss == "poss":
            pre = "poss"
            pull_from = self.possibles

        for i in range(9):
            self.__dict__[pre + "row" + str(i)] = pull_from[i]
            self.__dict__[pre + "col" + str(i)] = [row[i] for row in pull_from]
        for a in range(3):
            for b in range(3):
                self.__dict__[pre + f"sqr{a}{b}"] = []
        for i in range(9):
            for j in range(9):
                rbox, cbox = str(i//3), str(j//3)
                self.__dict__[pre + f"sqr{rbox}{cbox}"].append(pull_from[i][j])

    def build_possibles(self):
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

    def print_possibles(self):
        print("\n")
        for line in self.possibles:
            out = ""
            for item in line:
                out += str(item).ljust(16, " ")
            print(out)

    def update(self):
        self.update_dict("raw")
        self.build_possibles()
        self.update_dict("poss")

    def first_pass(self):
        print("Starting first pass")
        initial = str(self.raw)
        for r in range(9):
            for c in range(9):
                if len(self.possibles[r][c]) == 1:
                    print((r+1, c+1), " -> ", self.possibles[r][c][0])
                    self.raw[r][c] = self.possibles[r][c][0]
        self.update()
        print("Ending first pass")
        return initial == str(self.raw)

    def second_pass(self):
        print("Starting second pass")
        initial = str(self.raw)
        for r in range(9):
            for c in range(9):
                if self.raw[r][c] != 0:
                    continue
                self.update()
                rowmates = self.__dict__["possrow" + str(r)][:c] + self.__dict__["possrow" + str(r)][c+1:] 
                checkrow = []
                for fellow in rowmates:
                    checkrow.extend(fellow)
                checkrow = set(checkrow)

                colmates = self.__dict__["posscol" + str(c)][:c] + self.__dict__["posscol" + str(c)][c+1:] 
                checkcol = []
                for fellow in colmates:
                    checkcol.extend(fellow)
                checkcol = set(checkcol)

                pos = (3*(r%3) + (c%3))
                sqrmates = self.__dict__[f"posssqr{r//3}{c//3}"][:pos] + self.__dict__[f"posssqr{r//3}{c//3}"][pos+1:]
                checksqr = []
                for fellow in sqrmates:
                    checksqr.extend(fellow)
                checksqr = set(checksqr)

                poss = self.possibles[r][c]
                for num in range(1, 10):
                    # Consider only numbers in poss
                    if not num in poss:
                        continue
                    if (not num in checkrow
                        or not num in checkcol
                        or not num in checksqr):
                        self.print_possibles()
                        print(checkrow,
                              checkcol,
                              checksqr)
                        print("row = " + str(r))
                        print("col = " + str(c))
                        print("Pos = " + str(pos))
                        self.raw[r][c] = num
                        print((r+1, c+1), " -> ", num)
                        break
        self.update()
        print("Ending second pass")
        return initial == str(self.raw)

    def solve(self):
        while True:
            initial = str(self.raw)
            while not self.first_pass():
                pass
            self.second_pass()
            if initial == str(self.raw):
                for line in self.possibles:
                    print(line)
                print(self)
                return

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

    @classmethod
    def process_txt(cls, name):
        name = "./src/" + name + ".txt"
        out = []
        with open(name, "r") as f:
            temp = f.read().split("\n")
            for line in temp:
                line = line.split()
                line = list(map(int, line))
                if len(line) != 0:
                    out.append(line)
        print(out)
        return cls(out)


to_do = Sudoku.process_txt("new_extreme")
to_do.update()
to_do.solve()
# while not (to_do.first_pass()):
#     print(to_do, "\n")

