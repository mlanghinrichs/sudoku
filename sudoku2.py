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
        return len(self) == 81

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
        for r in range(9):
            for c in range(9):
                if r//3 == row_//3 and c//3 == col_//3:
                    yield self[r, c]

    def others_in_square(self, row_, col_):
        for r in range(9):
            for c in range(9):
                # if it's in the same square but not the same cell...
                if (r//3 == row_//3 and c//3 == col_//3
                    and not (r == row_ and c == col_)):
                    yield self[r, c]

    def possibles(self, row_, col_):
        """Return set of the possible values for self[row_, col_]."""
        if self[row_, col_]:
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
        orp = set()
        for c in range(9):
            if c != col_:
                orp = orp | self.possibles(row_, c)
        return orp
        
    def other_column_possibles(self, row_, col_):
        ocp = set()
        for r in range(9):
            if r != row_:
                ocp = ocp | self.possibles(r, col_)
        return ocp
    
    def other_square_possibles(self, row_, col_):
        osp = set()
        for r in range(9):
            for c in range(9):
                if row_//3 == r//3 and col_//3 == c//3 and (r, c) != (row_, col_):
                    osp = osp | self.possibles(r, c)
        return osp

    def fill_possibles(self):
        """Fill cells if they have only one possible value."""
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
    
    def fill_possibles_loop(self):
        return self.loop_function(self.fill_possibles)

    def loop_function(self, func):
        while True:
            current = len(self)
            func()
            if current == len(self):
                return self.full()

    def only_possibles(self):
        """Fill cell if it holds the only # possibility in its row/col/sqr."""
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
     
    def only_possibles_loop(self):
        return self.loop_function(self.only_possibles)
    
    def solve_funcs(self, *args):
        current = len(self)
        while not args[0]():
            if current == len(self) and len(args) > 1:
                self.solve_funcs(*args[1:])
            if current == len(self):
                return self.full()
            current = len(self)
        return self.full()
    
    def solve(self):
        if self.solve_funcs(self.fill_possibles_loop, self.only_possibles_loop):
            print("Puzzle complete!")
        else:
            print("Incomplete.")
        print(self)

    @classmethod
    def process_str(cls, name):
        """Create a Sudoku from a text file located in ./src/"""
        name = f"./src/{name}.txt"
        with open(name, "r") as f:
            source = f.read().split("\n")
            source = [list(map(int, line.split()))
                      for line in source if len(line) > 0]
        return cls(source)


to_do = Sudoku.process_str("extreme1")
print(to_do)
to_do.solve()
