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
            string += str(cell['val'])
            i += 1
            if i % 9:
                string += " "
            elif i % 81 and not i % 9:
                string += "\n"
        return string

    def percent_done(self):
        """Return % completion rounded to 2 decimal points."""
        return round((100*len(self)) / 81, 2)

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

    def fill_possibles(self):
        """Fill cells if they have only one possible value."""
        for cell in self:
            r = cell["r"]
            c = cell["c"]
            poss = self.possibles(r, c)
            if len(poss) == 1:
                self[r, c] = poss.pop()

    def fill_possibles_loop(self):
        """fill_possibles() until it doesn't alter the puzzle state further."""
        while True:
            current = len(self)
            self.fill_possibles()
            # If nothing has been added by fill_possibles(), break
            if current == len(self):
                break

    def only_possible(self):
        """Fill cell if it holds the only # possibility in its row/col/sqr."""
        pass
        # TODO finish me

    @classmethod
    def process_str(cls, name):
        """Create a Sudoku from a text file located in ./src/"""
        name = f"./src/{name}.txt"
        with open(name, "r") as f:
            source = f.read().split("\n")
            source = [list(map(int, line.split()))
                      for line in source if len(line) > 0]
        return cls(source)


to_do = Sudoku.process_str("medium")
print(to_do.percent_done())
to_do.fill_possibles_loop()
print(to_do.percent_done())
print(to_do)
