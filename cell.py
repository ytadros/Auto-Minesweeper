import tkinter
from game_settings import COLORS


class Cell(tkinter.Label):
    """
    A Cell object. Inherits from tkinter.Label.

    Attributes:
        is_naked (`bool`): `Property`. Once True, can't be set back to False.

        is_flagged (`bool`): If True, Cell is marked as being mined.
                             a Cell cannot be uncovered while it is flagged.

        is_mined (`bool`): If True, Cell is mined.
                           If a mined Cell is uncovered then BOOM! Game over.

        surrounding_mines (`int`): number of neighbors mined.

        text (`str`): `Property`. Text to display in Cell.

        bg (`str`): `Property`. Background color.
                                This is an index in the COLORS dictionary in game_settings.py

        fg (`str`): `Property`. Foreground (text) color..
                                This is an index in the COLORS dictionary in game_settings.py

    Methods:
        uncover(): Uncover Cell.

        flag(): Flag Cell as mined.

        un_flag(): Remove flag from Cell

        show_mistakes(): Triggered for all Cells when game over.
    """

    def __init__(self, master):

        super().__init__(master=master, font='bold', width=2,
                         relief='raised', text=' ', bg=COLORS['covered'])

        self._is_naked = False
        self.is_flagged = False
        self.is_mined = False
        self.surrounding_mines = 0

        self._text = ' '
        self._bg = 'covered'
        self._fg = None

    @property
    def is_naked(self) -> bool:
        return self._is_naked

    @is_naked.setter
    def is_naked(self, is_naked: bool):
        if is_naked:
            self._is_naked = is_naked
            self.config(relief='sunken')
            self.bg = 'naked'

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self.config(text=text)

    @property
    def bg(self) -> str:
        return self._bg

    @bg.setter
    def bg(self, bg: str):
        if bg in COLORS:
            self._bg = bg
            self.config(bg=COLORS[bg])

    @property
    def fg(self) -> str:
        return self._fg

    @fg.setter
    def fg(self, fg: str):
        if fg in COLORS:
            self._fg = fg
            self.config(fg=COLORS[fg])

    def uncover(self) -> None:
        """Uncover if not flagged. If Cell is mined, mark as trigger."""
        if self.is_flagged:
            return
        self.is_naked = True
        if self.is_mined:
            self.text = 'X'
            self.bg = 'boom_bg'
            self.fg = 'mistake'
        else:
            self.text = self.fg = self.surrounding_mines

    def flag(self) -> None:
        """Flag Cell"""
        # TODO: check if following two lines are necessary.
        if self.is_naked:
            return
        self.is_flagged = True
        self.text = self.fg = 'F'
        self.bg = 'flagged'

    def un_flag(self) -> None:
        """Un_flag Cell"""
        # TODO: check if following two lines are necessary.
        if not self.is_flagged:
            return
        self.is_flagged = False
        self.text = ' '
        self.bg = 'covered'

    def show_mistakes(self) -> None:
        """Reveal un-flagged mine or false flag."""
        if self.is_naked:
            return

        if self.is_mined and not self.is_flagged:
            self.text = 'X'
            self.bg = 'mine_bg'
            self.fg = 'mine_fg'
        elif self.is_flagged and not self.is_mined:
            self.text = 'F'
            self.fg = 'mistake'
            self.bg = 'bad_flag'
