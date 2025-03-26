import random
from neighborhood import Block
from game_settings import pause


class Queue(list):
    """
    A list of coordinates to be iteratively processed.

    Highlights the Cells whose coordinates it contains.

    This list re-orients to process coordinates based on chosen direction.

    Attributes:

        field (`Minefield`): Reference to Minefield containing Cells.

        color (`str`): Color to highlight Cells in Queue.
                       This is an index in the COLORS dictionary in game_settings.py

        direction (`str`): Direction to re-orient to.

            "unordered" means process coordinates in the order they were appended.
            "random" means shuffle all coordinates with each iteration.
            The other four directions correspond to the cardinal directions.

            For example, "east" means the Queue will be sorted in such a way
            that west-most coordinates will be processed first, and the algorithm
            will work its way towards the east.

        is_busy (`bool`): If the Queue is already being processed, this is
            set to True, preventing any new processes from initiating
            a call to process it.

            This measure prevents recursion errors.
    """

    def __init__(self, field=None, color=None, direction="LIFO"):
        super().__init__()
        self.field = field
        self.color = color
        self.direction = direction
        self.is_busy = False

    def append(self, cell: tuple[int, int]) -> None:
        """
        Adds `cell` to Queue. Highlights Cell. Does not add duplicates.

        Args:
            cell: `tuple` coordinates to add to Queue.
        """
        if cell in self:
            return

        if self.color:
            self.field[cell].bg = self.color
        super().append(cell)

    def remove(self, cell: tuple[int, int]) -> None:
        """
        Removes `cell` from Queue if it's in there. Removes highlight from Cell.

        Args:
            cell: `tuple` coordinates to remove from Queue.
        """
        if cell not in self:
            return

        self.field[cell].bg = 'naked'
        super().remove(cell)

    def re_orient(self):
        """Sorts Queue based on `direction`"""
        if self.direction in ("LIFO", "FIFO"):
            return

        if self.direction == "random":
            random.shuffle(self)
            return

        if self.direction == "whiplash":
            self.reverse()
            return

        if self.direction in ("east", "west"):
            sort_index = 0
        else:
            sort_index = 1

        self.sort(key=lambda cell: cell[sort_index])
        if self.direction in ("south", "east"):
            self.reverse()


class SuperQueue(Queue):
    """
    A special Queue with access to the direction tkinter variable
    in the control panel.

    Attributes:
        direction_var: Reference to `direction` variable in control panel.

    Methods:
        re_orient(): Overrides Queue's re_orient() method to get the current
                     direction from the tkinter variable in the control panel.

        add_batch(): Adds batch of cell coordinates to SuperQueue.
        clean_up(): Removes any cells which are no longer useful.
                    Corrects highlights.
    """

    def __init__(self, field, color, direction_var):
        super().__init__(field=field, color=color)

        self.direction_var = direction_var
        self.direction = direction_var.get()

    def re_orient(self):
        """Updates direction from control panel then calls super."""
        self.direction = self.direction_var.get()
        super().re_orient()

    def add_batch(self, batch: set[tuple[int, int]], emphasis, color):
        """
        Adds `batch` of cell coordinates to SuperQueue.

        Highlights and pauses based on settings in display panel.

        Args:
            batch: `set` of cell coordinates.
            emphasis: Reference to the appropriate group of settings in
                      the display panel.
            color: `str` color to highlight cells that are being added
                   to the SuperQueue.
        """
        new_batch = Queue(field=self.field, color=color)
        for cell in batch:
            if cell not in self:
                new_batch.append(cell)
        new_batch.direction = self.direction_var.get()
        new_batch.re_orient()
        if emphasis.is_checked:
            [self.field[cell].update() for cell in new_batch]
            pause(emphasis.pause_time)
        while new_batch:
            new_cell = new_batch[0]
            new_batch.remove(new_cell)
            self.append(new_cell)

    def clean_up(self, emphasis):
        """
        Removes all cells from SuperQueue which have no unknown neighbors.
        Also corrects any highlighting issues.

        Highlights and pauses based on settings in display panel.

        Args:
            emphasis: Reference to the appropriate group of settings in
                      the display panel.
        """
        redundant = Queue(field=self.field, color="redundant")
        for cell in self[::-1]:
            block = Block(self.field, cell)
            if not block.unknown_neighbors:
                self.remove(cell)
                redundant.append(cell)
            elif self.field[cell].bg != self.color:
                self.field[cell].bg = self.color

        if redundant and emphasis.is_checked:
            [self.field[cell].update() for cell in redundant]
            pause(emphasis.pause_time)
        while redundant:
            redundant.remove(redundant[-1])
