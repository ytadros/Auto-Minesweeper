class Block(set):
    """
    A set of xy coordinates for all Cells immediately surrounding `locus` Cell.

    Most Cells will have 8 total neighbors in their Block. Cells along the edges
    will have 5 neighbors, and the four corner Cells will have 3 neighbors.

    A Block is further subdivided into three separate sets of neighbor coordinates
    with common attributes.

    Attributes:

        field (`Minefield`): Reference to Minefield containing Cell objects.

        center (`tuple`): xy coordinates of the center Cell, around
                         which the Block is built.

        naked_neighbors (`set`): contains coordinates of neighboring "naked" Cells.

        flagged_neighbors (`set`): contains coordinates of neighboring "flagged" Cells.

        unknown_neighbors (`set`): contains coordinates of neighboring "unknown" Cells.

    Methods:

        solve(): Analyze Cells in Block and return decision.
    """

    def __init__(self, field, center: tuple[int, int]):
        super().__init__()
        self.field = field
        self.center = center
        self.naked_neighbors = set()
        self.flagged_neighbors = set()
        self.unknown_neighbors = set()

        x, y = center
        possible_neighbors = {
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1),
        }
        for neighbor in possible_neighbors:
            if neighbor in field:
                self.add(neighbor)
                if field[neighbor].is_naked:
                    self.naked_neighbors.add(neighbor)
                elif field[neighbor].is_flagged:
                    self.flagged_neighbors.add(neighbor)
                else:
                    self.unknown_neighbors.add(neighbor)

    def solve(self) -> str:
        """
        Analyze Cells in Block and return decision.

        Returns: `str`

            If the `center` Cell's `surrounding_mines` attribute
            matches the number of flagged Cells, this means
            all unknown neighbors are not mined. Return "clear".

            If the `center` Cell's `surrounding_mines` attribute
            matches the number of non-naked cells, this means
            all unknown neighbors are mined. Return "flag".

            Otherwise, return "?"
        """
        center_value = self.field[self.center].surrounding_mines
        num_flagged = len(self.flagged_neighbors)
        num_unknown = len(self.unknown_neighbors)
        possible_mines = num_flagged + num_unknown

        if center_value <= num_flagged:
            decision = "clear"
        elif center_value == possible_mines:
            decision = "flag"
        else:
            decision = "?"

        return decision


# class Neighborhood:
#     """
#     Neighborhood of Blocks.
#     for now, assumes exactly two args.
#     """
#     def __init__(self, field, *args):
#         self.blocks = [Block(field, locus) for locus in args]
#         self.relationships = {
#             (self.blocks[0].locus,)
#         }
