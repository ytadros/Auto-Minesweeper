import random
from neighborhood import Block


class Minefield(dict):
    """
    A dictionary to hold the Cell objects indexed by x, y coordinates.

    Attributes:

        total_mines (`int`): Total number of mines to be placed in Minefield.

        is_new (`bool`): If True, there are still no mines in the Minefield.
                         Once the first Cell is uncovered, mines are placed
                         and `is_new` is set to False.

    Methods:

        place_mines(first_step): Place mines randomly in Minefield, avoiding
                                 the Cell at `first_step` and its neighbors.

        uncover(loc): Uncover Cell with x, y coordinates `loc`.

        is_all_clear(): Return True if player wins.

        is_triggered(): Return True if player steps on mine.

        detonate(): Call each Cell object's show_mistakes() method.
    """

    def __init__(self, total_mines):
        super().__init__()
        self.total_mines = total_mines
        self.is_new = True

    def place_mines(self, first_step: tuple[int, int]):
        """
        Place mines in random Cells in Minefield.

        Args:
            first_step: Coordinates `(x, y)` of first uncovered Cell.
                        No mines will be placed in this Cell or in any
                        of its neighbors.
        """
        leave_clear = Block(self, first_step)
        leave_clear.add(first_step)
        for _ in range(self.total_mines):
            mined_cell = ()
            mine_placed = False
            while not mine_placed:
                candidate = random.choice(list(self))
                if candidate in leave_clear or self[candidate].is_mined:
                    continue
                mined_cell = candidate
                self[candidate].is_mined = True
                mine_placed = True
            for neighbor in Block(self, mined_cell):
                self[neighbor].surrounding_mines += 1

    def uncover(self, loc: tuple[int, int]):
        """
        Uncover Cell at coordinates `loc`.

        If field is new, place mines first.
        """
        if self.is_new:
            self.place_mines(first_step=loc)
            self.is_new = False

        self[loc].uncover()

    def is_all_clear(self) -> bool:
        """Check if all un-mined cells are cleared."""
        num_cleared = 0
        for cell in self.values():
            if cell.is_naked:
                num_cleared += 1
        num_clearable = len(self) - self.total_mines
        if num_cleared == num_clearable:
            return True
        else:
            return False

    def is_triggered(self) -> bool:
        """Check for any triggered mines. If found, detonate()"""
        for cell in self.values():
            if cell.is_naked and cell.is_mined:
                self.detonate()
                return True
        return False

    def detonate(self):
        """Show all mistakes."""
        for cell in self.values():
            cell.show_mistakes()
