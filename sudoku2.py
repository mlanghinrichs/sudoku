class Sudoku():

    def __init__(self, puzzle):
        self.raw = puzzle

    def __getitem__(self, key):
        try:
            a, b = key
            return self.raw[a][b]
        except IndexError:
            raise IndexError(f"Nothing exists at {a}, {b}")
        except TypeError:
            raise TypeError("Sudoku indexing requires int, int coordinates")

    def __setitem__(self, key, value):
        try:
            a, b = key
            self.raw[a][b] = value
        except IndexError:
            raise IndexError(f"{a}, {b} is out of Sudoku bounds")
        except TypeError:
            raise TypeError("Sudoku indexing requires int, int coordinates")

    def __iter__(self):
        for r in range(9):
            for c in range(9):
                yield {"val": self.raw[r][c], "r": r, "c": c}

    def __len__(self):
        length = 0
        for cell in self:
            if cell["val"] > 0:
                length += 1
        return length

    def __str__(self):
        string = ""
        i = 0
        for cell in self:
            if cell["val"] != 0:
                string += str(cell['val'])
            else:
                string += "-"
            i += 1
            if i%9 == 3 or i%9 == 6:
                string += "|"
            elif i % 9:
                string += " "
            elif i % 81 and not i % 9:
                string += "\n"
            if i == 27 or i == 54:
                string += "-----------------\n"
        return string

    def percent_done(self):
        """Return % completion rounded to 2 decimal points."""
        return round((100*len(self)) / 81, 2)
        
    def full(self):
        """Return True if all cells are full, False if not."""
        return len(self) == 81

    def validate(self):
        """Returen whether the sudoku values appear to be valid."""
        valid = True
        for i in range(9):
            col_ = [val for val in self.column(i) if val != 0]
            row_ = [val for val in self.row(i) if val != 0]
            if len(col_) != len(set(col_)) or len(row_) != len(set(row_)):
                valid = False
        for sqx in (0, 3, 6):
            for sqy in (0, 3, 6):
                sqr_ = [val for val in self.square(sqx, sqy) if val != 0]
            if len(sqr_) != len(set(sqr_)):
                valid = False
        return valid

    def column(self, col_):
        """Iterate over col_'s contents."""
        for row in self.raw:
            yield row[col_]

    def others_in_column(self, row_, col_):
        """Iterate over col_'s contents except for row_."""
        for r in range(9):
            if r != row_:
                yield self[r, col_]

    def row(self, row_):
        """Iterate over row_'s contents."""
        for cell_val in self.raw[row_]:
            yield cell_val

    def others_in_row(self, row_, col_):
        """Iterate over row_'s contents except for col_."""
        for c in range(9):
            if c != col_:
                yield self[row_, c]

    def square(self, row_, col_):
        """Iterate over the square containing row_, col_."""
        for r in range(9):
            for c in range(9):
                if r//3 == row_//3 and c//3 == col_//3:
                    yield self[r, c]

    def others_in_square(self, row_, col_):
        """Iterate over the square containing row_, col_ except for that cell."""
        for r in range(9):
            for c in range(9):
                # if it's in the same square but not the same cell...
                if (r//3 == row_//3 and c//3 == col_//3
                    and not (r == row_ and c == col_)):
                    yield self[r, c]

    def possibles(self, row_, col_, none_if_full=True):
        """Return set of the possible values for self[row_, col_]."""
        if self[row_, col_] and none_if_full:
            return set()
        else:
            poss = set([i+1 for i in range(9)])
            for val in self.others_in_column(row_, col_):
                poss.discard(val)
            for val in self.others_in_row(row_, col_):
                poss.discard(val)
            for val in self.others_in_square(row_, col_):
                poss.discard(val)
            return poss

    def other_row_possibles(self, row_, col_):
        """Return set of possible values for other cells in row."""
        orp = set()
        for c in range(9):
            if c != col_:
                orp = orp | self.possibles(row_, c)
        return orp

    def other_column_possibles(self, row_, col_):
        """Return set of possible values for other cells in column."""
        ocp = set()
        for r in range(9):
            if r != row_:
                ocp = ocp | self.possibles(r, col_)
        return ocp
    
    def other_square_possibles(self, row_, col_):
        """Return set of possible values for other cells in square."""
        osp = set()
        for r in range(9):
            for c in range(9):
                if row_//3 == r//3 and col_//3 == c//3 and (r, c) != (row_, col_):
                    osp = osp | self.possibles(r, c)
        return osp

    def fill_possibles(self):
        """Fill cells if they have only one possible value and return full()."""
        print("db - running fill_possibles()")
        for cell in self:
            r = cell["r"]
            c = cell["c"]
            poss = self.possibles(r, c)
            if len(poss) == 1:
                val = poss.pop()
                self[r, c] = val
                print(f"({r}, {c}) -> {val}")
        return self.full()

    def only_possibles(self):
        """Fill cell if it has a unique possibility, return full()."""
        print("db - running only_possibles()")
        for cell in self:
            r, c = cell["r"], cell["c"]
            check = self.possibles(r, c)
            if not check:
                continue
            for val in range(1, 10):
                if (val in check and
                    (not val in self.other_row_possibles(r, c)
                    or not val in self.other_column_possibles(r, c)
                    or not val in self.other_square_possibles(r, c))):
                    print(f"({r}, {c}) -> {val}")
                    self[r, c] = val
        return self.full()

    def guess_dicts(self):
        out = []
        for cell in self:
            r, c = cell["r"], cell["c"]
            if cell["val"] == 0:
                out.append({"val": cell["val"],
                            "r": r,
                            "c": c,
                            "poss": self.possibles(r, c)
                            })
        for dict_ in out:
            print(dict_)
        return out

    def guess(self, *dicts):
        # given {val, r, c, poss} and a self.validate() function
        if not dicts:
            return True
        for cell in dicts:
            r, c = cell["r"], cell["c"]
            for p in cell["poss"]:
                self[r, c] = p
                print(f"Guessing ({r}, {c}) -> {p}")
                if self.validate() and self.guess(*dicts[1:]):
                    return True
                elif not self.validate():
                    print(f"{p} was wrong")
                    continue
                else:
                    print("Something went wrong?")
            return False
     
    def solve_funcs(self, *args):
        """Recur args until none of them change self.raw, return full()."""
        current = len(self)
        while not args[0]():
            if current == len(self) and len(args) > 1:
                self.solve_funcs(*args[1:])
            if current == len(self):
                return self.full()
            current = len(self)
        return self.full()

    def solve(self):
        """Call solve_funcs() with current solve algorithms."""
        if self.solve_funcs(self.fill_possibles, self.only_possibles):
            print("Puzzle complete!")
        else:
            print("Incomplete. Trying to guess:")
            print(self.guess(*self.guess_dicts()))
        print(self)

    @classmethod
    def process_str(cls, name):
        """Create a Sudoku from a text file located in ./src/."""
        name = f"./src/{name}.txt"
        with open(name, "r") as f:
            source = f.read().split("\n")
            source = [list(map(int, line.split()))
                      for line in source if len(line) > 0]
        return cls(source)


to_do = Sudoku.process_str("extreme1")
print(to_do)
to_do.solve()

