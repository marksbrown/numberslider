"""
This is the third implementation
"""


from random import shuffle, choice
from time import sleep

TESTING = False

N = 3


class Loc:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __repr__(self):
        return f"({self.i},{self.j})"

    def valid_loc(self):
        return 0 <= self.i < N and 0 <= self.j < N

    def adjacent(self):
        i = self.i
        j = self.j
        if i > 0:
            yield i - 1 + N * j  # left
        if i < N - 1:
            yield i + 1 + N * j  # right
        if j > 0:
            yield i + N * (j - 1)  # top
        if j < N - 1:
            yield i + N * (j + 1)  # bottom

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return self.i + N * self.j


class Cell(Loc):
    def __init__(self, i, j, value):
        super().__init__(i, j)
        self.value = value


class Slider:

    @property
    def state(self):
        return [cell.value for cell in self.cells]

    def __init__(self):
        coordinates = (divmod(i, N) for i in range(N * N))
        values = [str(v) for v in range(1, N * N)] + ["_"]

        if not TESTING:
            shuffle(values)

        self.slider = values.index("_")
        # index is position!
        self.cells = [
            Cell(j, i, v if v else 0)
            for j, (v, (i, j)) in enumerate(zip(values, coordinates), 1)
        ]

    def valid_moves(self):
        for cell in self.cells[self.slider].adjacent():
            yield self.cells[cell].value

    def update(self, value):
        for first, cell in enumerate(self.cells):
            if cell.value == value:
                break
        for second in self.cells[first].adjacent():
            if self.cells[second].value == "_":
                self.cells[first].value, self.cells[second].value = (
                    self.cells[second].value,
                    self.cells[first].value,
                )
                self.slider = first
                return
        raise IndexError(f"No move was performed with index {first}")

    def in_order(self) -> bool:
        for j, cell in enumerate(self.cells[:-1], 1):
            if cell.value != str(j):
                return False
        return True

    def pretty(self):
        for j, v in enumerate(self.state):
            print(v, end=" ")
            if not (j + 1) % N:
                print("")


def random_walk(verbose=False):
    sl = Slider()
    moves = 0
    while not sl.in_order():
        if verbose:
            sl.pretty()
        moves += 1
        mv = choice(tuple(sl.valid_moves()))
        sl.update(mv)

    print(f"Game completed in {moves} moves")


if __name__ == "__main__":
    random_walk()
