"""
An ASCII version of the game devoid of interface concerns

This version is more useful for playing the game algorithmically
"""

from random import shuffle

TESTING = False

N = 3


def ask_for_int(prompt, low, high):
    while True:
        try:
            mv = int(input(">>"))
        except ValueError:
            print("not an option!")
            continue
        if low <= mv < high:
            break
        else:
            print("Invalid move!")
    return mv


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

    def draw(self):
        print(f"{self.value:>3} ", end="")


class App:
    def __init__(self):
        run_game = True
        while run_game:
            self.setup()

            while True:
                self.draw()
                if not self.check_if_won():
                    self.update(str(ask_for_int(">>", 1, N * N)))
                else:
                    r = input("play again (y)?").lower()
                    if r[0] != "y":
                        run_game = False
                    break

    def setup(self):
        coordinates = (divmod(i, N) for i in range(N * N))
        values = [str(v) for v in range(1, N * N)] + ["_"]

        if not TESTING:
            shuffle(values)

        # index is position!
        self.cells = [
            Cell(j, i, v if v else 0)
            for j, (v, (i, j)) in enumerate(zip(values, coordinates), 1)
        ]

    def update(self, value):
        if self.check_if_won():
            print("YAY!")
            return

        for first, cell in enumerate(self.cells):
            if cell.value == value:
                break
        for second in self.cells[first].adjacent():
            if self.cells[second].value == "_":
                self.cells[first].value, self.cells[second].value = (
                    self.cells[second].value,
                    self.cells[first].value,
                )
                return

    def check_if_won(self):
        for j, cell in enumerate(self.cells[:-1], 1):
            if cell.value != str(j):
                return False
        return True

    def draw(self):
        if self.check_if_won():
            print("Congratulations! You win!")

        for j, cell in enumerate(self.cells):
            cell.draw()
            if not (j + 1) % N:
                print("")
        print("")


if __name__ == "__main__":
    App()
