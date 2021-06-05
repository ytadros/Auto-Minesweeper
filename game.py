import tkinter
from game_settings import pause, GAME_OVER_MSG, ALL_CLEAR_MSG
from minefield import Minefield
from cell import Cell
from solving_queue import Queue, SuperQueue
from neighborhood import Block, Neighborhood


class Game(tkinter.Frame):
    """
    Game object. Inherits from `tkinter.Frame`.

    Attributes:

        field (`Minefield`): Minefield containing Cells indexed by `(x, y)` tuples.

        game_over (`bool`): If True, player lost (uncovered a mined cell)
                            No more moves are allowed.

        win (`bool`): If True, player won (all un-mined cells are clear).
                      No more moves are allowed.

        mines_left (`int`): `Property`. Number of mines left to flag.

        safes_left (`int`): `Property`. Number of safe cells left to clear.

        auto_solving (`tkinter.Checkbutton`): Access to `auto_solving`
                                              checkbutton in the control panel.

        direction (`tkinter.StringVar`): Access to `direction` variable
                                         in the direction panel.

        clear_queue (`SuperQueue`): Ordered list of covered cells in line
                                    to be cleared.

        auto_queue (`SuperQueue`): Ordered list of naked cells in line
                                   for their neighbors to be analyzed and solved.

        clear_queue (`SuperQueue`): Ordered list of cells which could not be solved
                                    by analyzing their immediate Block.
                                    Leftovers from the auto-queue.

        emphasis (`dict`): Provides access to the appropriate settings in the
                           display panel (located in the control panel).
                           These settings allow for the window to update highlights
                            and pause for a few milliseconds with each execution
                             of a procedure, thus showcasing the execution process.

    Methods:

        uncover(loc): Uncovers cell at coordinates `loc`.
                      Populates the appropriate Queue based on result and surroundings.

        toggle_flag(loc): Toggles flag at coordinates `loc`. Bound to right-click.
                          Populates the `auto_queue` based on surroundings.

        solve_block(center_cell): Takes action based on `center_cell`'s neighbors.

        process(queue): Passes each value in `queue` to the appropriate method.
                        Adds emphasis and loops until `queue` is empty.

        left_click(loc): Bound to left-click button for each Cell.
    """

    def __init__(self, control_panel, width, height, percent_mined):
        """`control_panel` passes a reference to the control panel in the main window."""

        super().__init__()

        # The following lines prevent an infinite loop at mine placement
        #  if percent_mined is set too high.
        total_cells = width * height
        total_mines_allowed = total_cells - 9
        total_mines_requested = round(total_cells * percent_mined / 100)

        total_mines = min(total_mines_requested, total_mines_allowed)

        self.field = Minefield(total_mines)

        self.game_over = False
        self.win = False

        self.status_label = control_panel.status_label

        self.mine_count_label = control_panel.mine_count_label
        self._mines_left = 0
        self.mines_left = total_mines

        self.safe_count_label = control_panel.safe_count_label
        self._safes_left = 0
        self.safes_left = (width * height) - total_mines

        self.auto_solving = control_panel.auto_solving
        self.hyper_solving = control_panel.hyper_solving
        self.direction = control_panel.direction_panel.direction

        # self.flag_queue = SuperQueue(self.field, color="to_flag", direction_var=self.direction)
        self.clear_queue = SuperQueue(self.field, color="clear_queue", direction_var=self.direction)
        self.auto_queue = SuperQueue(self.field, color="auto_queue", direction_var=self.direction)
        self.hyper_queue = SuperQueue(self.field, color="hyper_queue", direction_var=self.direction)

        self.emphasis = {
            "clear_queue": control_panel.display_panel.clear_queue_settings,
            "auto_queue": control_panel.display_panel.auto_queue_settings,
            "add_batch": control_panel.display_panel.add_batch_settings,
            "redundant": control_panel.display_panel.redundant_settings,
            "to_flag": control_panel.display_panel.to_flag_settings,
            "hyper_queue": control_panel.display_panel.hyper_queue_settings,
        }

        # Create cells
        for x in range(width):
            for y in range(height):
                self.field[x, y] = Cell(master=self)
                self.field[x, y].grid(row=y, column=x)
                self.field[x, y].bind("<Button-1>",
                                      lambda event, loc=(x, y): self.left_click(loc))
                self.field[x, y].bind("<Button-3>",
                                      lambda event, loc=(x, y): self.toggle_flag(loc, auto_flag=False))

    @property
    def mines_left(self):
        return self._mines_left

    @mines_left.setter
    def mines_left(self, mines_left):
        self._mines_left = mines_left
        self.mine_count_label.config(text=mines_left)

    @property
    def safes_left(self):
        return self._safes_left

    @safes_left.setter
    def safes_left(self, safes_left):
        self._safes_left = safes_left
        self.safe_count_label.config(text=safes_left)

    def _auto_spark(self):
        """Kick-starts all queues processing if it's not already busy."""
        clear_busy = self.clear_queue.is_busy
        auto_busy = self.auto_queue.is_busy
        hyper_busy = self.hyper_queue.is_busy

        if self.clear_queue and not clear_busy:
            self.clear_queue.is_busy = True
            self.process(self.clear_queue)
        elif self.auto_queue and not clear_busy and not auto_busy:
            self.auto_queue.is_busy = True
            self.process(self.auto_queue)
        elif self.hyper_queue and not clear_busy and not auto_busy and not hyper_busy:
            self.hyper_queue.is_busy = True
            self.process(self.hyper_queue)

    def uncover(self, loc: tuple[int, int]) -> None:
        """
        Uncovers cell at coordinates `loc`.

        If the now naked (and hopefully un-mined) cell has no mined neighbors,
        add all its uncovered neighbors to the `clear_queue`.

        If it does have mined neighbors, and if `auto_solving` is checked,
        add the cell's coordinates to the `auto_queue`.
        """
        if loc in self.clear_queue:
            self.clear_queue.remove(loc)

        if self.field[loc].is_naked:
            print("Clear naked")
            return

        self.field.uncover(loc)

        if self.field.is_triggered():
            self.game_over = True
            [queue.clear() for queue in
             (self.clear_queue, self.auto_queue, self.hyper_queue)]
            self.status_label.config(text=GAME_OVER_MSG)
            return

        self.safes_left -= 1

        if self.field.is_all_clear():
            self.win = True
            self.status_label.config(text=ALL_CLEAR_MSG)

        if loc in self.clear_queue:
            self.clear_queue.remove(loc)

        if self.field[loc].surrounding_mines == 0:
            block = Block(self.field, loc)
            self.clear_queue.add_batch(block.unknown_neighbors,
                                       emphasis=self.emphasis["add_batch"],
                                       color="new_clear")
        elif self.auto_solving.get():
            block = Block(self.field, loc)
            useful_neighbors = block.naked_neighbors
            useful_neighbors.add(loc)
            [self.hyper_queue.remove(cell) for cell in useful_neighbors]
            self.auto_queue.add_batch(useful_neighbors,
                                      emphasis=self.emphasis["add_batch"],
                                      color="new_auto")
            self.auto_queue.clean_up(emphasis=self.emphasis["redundant"])
            self.hyper_queue.clean_up(emphasis=self.emphasis["redundant"])

        self._auto_spark()

    def toggle_flag(self, loc: tuple[int, int], auto_flag=True) -> None:
        """
        Toggle flag at location `loc`.

        If cell at `loc` has any useful neighbors, adds them to the `auto_queue`.
        This method is bound to the right click button for each cell.
        """
        if self.game_over or self.field[loc].is_naked:
            return

        if self.field[loc].is_flagged:
            print("UNFLAGGING")
            self.field[loc].un_flag()
            self.mines_left += 1
        else:
            self.field[loc].flag()
            self.mines_left -= 1

        if self.auto_solving.get():
            block = Block(self.field, loc)
            useful_neighbors = {neighbor for neighbor in block.naked_neighbors
                                if Block(self.field, neighbor).unknown_neighbors}
            [self.hyper_queue.remove(cell) for cell in useful_neighbors]
            self.auto_queue.add_batch(useful_neighbors,
                                      emphasis=self.emphasis["add_batch"],
                                      color="new_auto")
        if not auto_flag:
            self._auto_spark()

    def solve_block(self, center_cell: tuple[int, int]):
        """
        Creates a Block around `center_cell` and calls that Block's
         solve() method.

        If the Block's solve() method returns "clear",
         uncovers unknown neighbors.

        If the Block's solve() method returns "flag",
         flags unknown neighbors.

        If the Block's solve() method does not reach a clear decision,
         passes the `center_cell` coordinates to the `hyper_queue`

        Args:
            center_cell: `tuple`. Coordinates.
        """
        block = Block(self.field, center_cell)
        action = block.solve()
        if action == 'clear':
            self.clear_queue.add_batch(block.unknown_neighbors,
                                       emphasis=self.emphasis["add_batch"],
                                       color="new_clear")
            if not self.clear_queue.is_busy:
                self.clear_queue.is_busy = True
                self.process(self.clear_queue)
        elif action == 'flag':
            to_flag = Queue(field=self.field, color="to_flag")
            for cell in block.unknown_neighbors:
                to_flag.append(cell)
            to_flag.direction = self.direction
            to_flag.re_orient()
            if self.emphasis["to_flag"].is_checked:
                self.update()
                pause(self.emphasis["to_flag"].pause_time)
            while to_flag:
                new_flag = to_flag[0]
                to_flag.remove(new_flag)
                self.toggle_flag(new_flag)
        elif self.hyper_solving.get() and center_cell not in self.hyper_queue:
            self.hyper_queue.append(center_cell)
            for neighbor in block.naked_neighbors:
                if neighbor in self.hyper_queue or neighbor in self.auto_queue:
                    continue
                neighbor_block = Block(self.field, neighbor)
                if neighbor_block.unknown_neighbors:
                    self.hyper_queue.append(neighbor)
        self._auto_spark()

    def solve_neighborhood(self, cell_a, cell_b):
        self.field[cell_a].bg = "naked"
        self.field[cell_b].bg = "hyper_queue"
        clear_set, flag_set = Neighborhood(self.field, cell_a, cell_b).solve()
        # for cell in flag_set:
        #     if self.field[cell].is_flagged:
        #         print("to_flag from solve_neighborhood (before add_batch to clear_queue)")
        if clear_set:
            self.clear_queue.add_batch(clear_set,
                                       emphasis=self.emphasis["add_batch"],
                                       color="new_clear")
        if flag_set:
            to_flag = Queue(field=self.field, color="to_flag")
            for cell in flag_set:
                # if self.field[cell].is_flagged:
                #     print("to_flag from solve_neighborhood (after add_batch to clear_queue)")
                to_flag.append(cell)
            to_flag.direction = self.direction
            to_flag.re_orient()
            if self.emphasis["to_flag"].is_checked:
                self.update()
                pause(self.emphasis["to_flag"].pause_time)
            while to_flag:
                new_flag = to_flag[0]
                if self.field[new_flag].is_flagged:
                    print("new_flag from solve_neighborhood")
                to_flag.remove(new_flag)
                self.toggle_flag(new_flag)
        self._auto_spark()

    def process(self, queue: SuperQueue):
        """
        Passes each value in `queue` to the appropriate method.
        Adds emphasis and loops until `queue` is empty.

        If `queue` being processed is the `clear_queue`,
         passes values to the `uncover` method.

        If `queue` being processed is the `auto_queue`,
         passes values to the `solve_block` method.

        If `queue` being processed is the `hyper_queue`,
         passes values to the `solve_block` method
         with `first_round` set to False. (for now...)

        Args:
            queue: `SuperQueue` to process.
                    Can be `clear_queue`, `auto_queue`, or `hyper_queue`
        """

        def apply_emphasis(queue_name):
            if self.emphasis[queue_name].is_checked:
                self.update()
                pause(self.emphasis[queue_name].pause_time)

        while queue:
            queue.re_orient()

            if self.direction.get() == "FIFO":
                next_cell = queue[0]
            else:
                next_cell = queue[-1]

            self.field[next_cell].bg = "active_cell"

            if queue == self.clear_queue:
                apply_emphasis("clear_queue")
                self.uncover(next_cell)

            elif queue == self.auto_queue:
                apply_emphasis("auto_queue")
                queue.remove(next_cell)
                self.solve_block(next_cell)

            elif queue == self.hyper_queue:
                # apply_emphasis("hyper_queue")
                queue.remove(next_cell)
                # self.solve_block(next_cell, first_round=False)
                block_a = Block(self.field, next_cell)
                unknowns_a = block_a.unknown_neighbors

                for cell_b in queue[::-1]:
                    block_b = Block(self.field, cell_b)
                    unknowns_b = block_b.unknown_neighbors
                    if unknowns_a & unknowns_b and unknowns_a.symmetric_difference(unknowns_b):
                        self.field[next_cell].bg = "active_cell"
                        self.field[cell_b].bg = "neighbor_cell"
                        apply_emphasis("hyper_queue")
                        self.solve_neighborhood(next_cell, cell_b)

        queue.is_busy = False
        self._auto_spark()

    def left_click(self, loc: tuple[int, int]):
        """Bound to left-click button for each Cell."""
        if self.game_over or self.win:
            return

        if self.field[loc].is_naked:
            self.solve_block(loc)
        else:
            self.uncover(loc)

        #
        # if self.auto_solving.get():
        #     self._auto_spark()
