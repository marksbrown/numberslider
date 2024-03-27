"""
Grid Game

1. Create a grid of 3 by 3 squares
Holding values 1 to 9. Put them in order!

For computer science project :
https://jweilhammer.github.io/sliding-puzzle-solver/
Nice clean idea
"""

import pyxel
from random import shuffle

TESTING = False

BLOCK_SIZE = 50
N = 3
GAP = 0.1 * BLOCK_SIZE

SCREEN_WIDTH = int(GAP + (BLOCK_SIZE + GAP) * N)
SCREEN_HEIGHT = int(GAP + (BLOCK_SIZE + GAP) * N)


class Loc:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __repr__(self):
        return f"({self.i},{self.j})"

    def valid_loc(self):
        return 0 <= self.i < N and 0 <= self.j < N

    @property
    def x(self):
        return GAP + self.i * (BLOCK_SIZE + GAP)

    @property
    def y(self):
        return GAP + self.j * (BLOCK_SIZE + GAP)

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
    def __init__(self, i, j, value, col):
        super().__init__(i, j)
        self.value = value
        self.col = col

    def draw(self):
        pyxel.rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE, self.col)
        pyxel.text(
            self.x + BLOCK_SIZE // 2, self.y + BLOCK_SIZE // 2, str(self.value), col=0
        )

    def contains(self, x, y):
        x1 = self.x
        x2 = x1 + BLOCK_SIZE
        y1 = self.y
        y2 = y1 + BLOCK_SIZE
        return x1 < x < x2 and y1 < y < y2


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setup()
        pyxel.run(self.draw, self.update)

    def setup(self):
        self.x = 0
        coordinates = (divmod(i, N) for i in range(N * N))

        values = [str(v) for v in range(1, N * N)] + [""]

        if not TESTING:
            shuffle(values)

        # index is position!
        self.cells = [
            Cell(j, i, v, col=5 if v else 0)
            for j, (v, (i, j)) in enumerate(zip(values, coordinates), 1)
        ]

        pyxel.mouse(True)

    def update(self):
        if self.check_if_won():
            self.x = (self.x + 2) % (SCREEN_WIDTH * 1.1)
            return
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x
            y = pyxel.mouse_y
            first = 0
            while first < len(self.cells):
                if self.cells[first].contains(x, y):
                    for second in self.cells[first].adjacent():
                        if not self.cells[second].value:
                            self.cells[first].value, self.cells[second].value = (
                                self.cells[second].value,
                                self.cells[first].value,
                            )
                            self.cells[first].col, self.cells[second].col = (
                                self.cells[second].col,
                                self.cells[first].col,
                            )
                            return

                first += 1

    def check_if_won(self):
        for j, cell in enumerate(self.cells[:-1], 1):
            if cell.value != str(j):
                return False
        return True

    def draw(self):
        if self.check_if_won():
            pyxel.cls(5)
            pyxel.text(
                self.x,
                SCREEN_HEIGHT // 2,
                "Congratulations! You win!",
                col=10,
            )
        else:
            pyxel.cls(0)
            for cell in self.cells:
                cell.draw()


if __name__ == "__main__":
    App()
