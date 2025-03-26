import random
from neighborhood import Block


class Minefield(dict):
    """
    A dictionary to hold the Cell objects indexed by x, y coordinates.

    Attributes:

        total_mines (`int`): Total number of mines to be placed in Minefield.

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

    def set_mine(self, loc):
        """Sets a mine at location `loc` and lets the neighbors know."""
        self[loc].is_mined = True
        for neighbor in Block(self, loc):
            self[neighbor].surrounding_mines += 1

    def place_mines(self, first_step: tuple[int, int]):
        """
        Place mines in random Cells in Minefield.

        Args:
            first_step: Coordinates `(x, y)` of first uncovered Cell.
                        No mines will be placed in this Cell or in any
                        of its neighbors.
        """
        mines_to_be_placed = self.total_mines

        leave_clear = {first_step}
        leave_clear.update(Block(self, first_step).unknown_neighbors)

        already_flagged = {loc for loc in self if self[loc].is_flagged}

        for flag in already_flagged:
            self.set_mine(flag)
            flag_buffer = Block(self, flag).unknown_neighbors
            if len(self) - len(leave_clear) - len(flag_buffer) >= self.total_mines:
                leave_clear.update(flag_buffer)
            mines_to_be_placed -= 1

        for _ in range(mines_to_be_placed):
            mine_placed = False
            while not mine_placed:
                candidate = random.choice(list(self))
                if candidate in leave_clear or self[candidate].is_mined:
                    continue
                self.set_mine(candidate)
                mine_placed = True

    def uncover(self, loc: tuple[int, int]):
        """
        Uncover Cell at coordinates `loc`.

        If field is new, place mines first.
        """
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
