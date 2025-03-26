import tkinter
from control_panel import ControlPanel
from game_settings import MAP_WIDTH, MAP_HEIGHT, PERCENT_MINED, ACTIVE_FIELD_MSG
from game import Game


class Minesweeper(tkinter.Tk):
    """
    Main program window.
    """

    def __init__(self, width=MAP_WIDTH, height=MAP_HEIGHT, percent_mined=PERCENT_MINED):
        super().__init__()
        self.title("Minesweeper")

        self.control_panel = ControlPanel()
        self.control_panel.grid(row=0, column=0)

        self.game = Game(control_panel=self.control_panel,
                         width=width, height=height, percent_mined=percent_mined)
        self.game.grid(row=0, column=1)

        self.control_panel.new_game_panel.width_box.insert("end", width)
        self.control_panel.new_game_panel.height_box.insert("end", height)
        self.control_panel.new_game_panel.percent_mined_box.insert("end", percent_mined)

        self.control_panel.new_game_panel.new_game_button.config(command=self.new_game)
        self.control_panel.new_game_panel.replay_button.config(command=self.replay)

    def new_game(self):
        """
        Starts a new game based on entries in the new_game_panel.
        """
        new_percent_mined = float(self.control_panel.new_game_panel.percent_mined_box.get())
        if new_percent_mined < 0:
            return

        self.game.destroy()
        self.game = Game(control_panel=self.control_panel,
                         width=int(self.control_panel.new_game_panel.width_box.get()),
                         height=int(self.control_panel.new_game_panel.height_box.get()),
                         percent_mined=new_percent_mined)
        self.game.grid(row=0, column=1)
        self.control_panel.status_label.config(text=ACTIVE_FIELD_MSG)

    def replay(self):
        """Resets minefield with the same mine layout."""
        # TODO: this.
        #  Game class should be initialized with number mines instead of percent.
        #  Mines Left label should say 0 or ? until mines are actually placed.
        layout = {loc: cell.is_mined for loc, cell in self.game.field.items()}
        self.game.destroy()
        self.game = Game(control_panel=self.control_panel,
                         width=int(self.control_panel.new_game_panel.width_box.get()),
                         height=int(self.control_panel.new_game_panel.height_box.get()),
                         percent_mined=0)
        self.game.grid(row=0, column=1)
        self.control_panel.status_label.config(text=ACTIVE_FIELD_MSG)
        self.game.is_new = False
        [self.game.field.set_mine(mine) for mine in layout if layout[mine]]

    # TODO: sqlite database storing pickled Game objects, so I can categorize
    #  them and analyze based on which direction algorithm was used to solve
    #  and how much of the board it was able to clear.


if __name__ == "__main__":
    test_game = Minesweeper()
    test_game.mainloop()
