import tkinter as tk
from game_settings import PAUSE_TIMES, ACTIVE_FIELD_MSG


class DirectionPanel(tk.LabelFrame):
    """
    Contains choices of direction and a tkinter `StringVar` attribute.

    Attributes:
        direction (`tkinter.StringVar`): Queue processing direction.
    """

    def __init__(self, master):
        super().__init__(master=master, text="Process Direction")
        self.direction = tk.StringVar(value="LIFO")

        self._lifo = tk.Radiobutton(master=self, text="L.I.F.O.")
        self._lifo.config(value="LIFO", variable=self.direction)
        self._lifo.grid(row=0, column=0, columnspan=2)

        self._fifo = tk.Radiobutton(master=self, text="F.I.F.O.")
        self._fifo.config(value="FIFO", variable=self.direction)
        self._fifo.grid(row=0, column=2, columnspan=2)

        self._whiplash = tk.Radiobutton(master=self, text="Whiplash")
        self._whiplash.config(value="whiplash", variable=self.direction)
        self._whiplash.grid(row=1, column=0, columnspan=2)

        self._random = tk.Radiobutton(master=self, text="Random")
        self._random.config(value="random", variable=self.direction)
        self._random.grid(row=1, column=2, columnspan=2)

        self._north = tk.Radiobutton(master=self, text="N")
        self._north.config(value="north", variable=self.direction)
        self._north.grid(row=2, column=0)

        self._south = tk.Radiobutton(master=self, text="S")
        self._south.config(value="south", variable=self.direction)
        self._south.grid(row=2, column=1)

        self._east = tk.Radiobutton(master=self, text="E")
        self._east.config(value="east", variable=self.direction)
        self._east.grid(row=2, column=2)

        self._west = tk.Radiobutton(master=self, text="W")
        self._west.config(value="west", variable=self.direction)
        self._west.grid(row=2, column=3)


class DisplaySettings:
    """Controls for showcasing a given process."""

    def __init__(self, master, row, text):
        super().__init__()
        self._is_checked = tk.BooleanVar(value=False)
        self.checkbutton = tk.Checkbutton(master=master, text=text,
                                          variable=self._is_checked,
                                          command=self._enable_spinner)
        self.checkbutton.grid(row=row, column=0)

        self.pause_spinner = tk.Spinbox(master=master, width=4,
                                        values=PAUSE_TIMES, state="disabled")
        self.pause_spinner.grid(row=row, column=1)

    @property
    def is_checked(self):
        return self._is_checked.get()

    @property
    def pause_time(self):
        return self.pause_spinner.get()

    def _enable_spinner(self):
        if self.is_checked:
            self.pause_spinner["state"] = "normal"
        else:
            self.pause_spinner["state"] = "disabled"


class DisplayPanel(tk.LabelFrame):
    """
    Provides functionality to visualize the execution of certain processes
    which are executed during gameplay.
    """

    def __init__(self, master):
        super().__init__(master=master, text="Display Processes")

        self.check_label = tk.Label(master=self, text="Highlight", fg="gray50")
        self.check_label.grid(row=0, column=0)

        self.pause_label = tk.Label(master=self, text="Pause time (ms)", fg="gray50")
        self.pause_label.grid(row=0, column=1)

        self.clear_queue_settings = DisplaySettings(master=self, row=1, text="to clear")
        self.auto_queue_settings = DisplaySettings(master=self, row=2, text="to solve")
        self.to_flag_settings = DisplaySettings(master=self, row=3, text="to flag")
        self.add_batch_settings = DisplaySettings(master=self, row=4, text="add to queue")
        self.redundant_settings = DisplaySettings(master=self, row=5, text="remove redundant")
        self.hyper_queue_settings = DisplaySettings(master=self, row=6, text="hyper queue")


class NewGamePanel(tk.LabelFrame):
    """Allows the player to start a new game with the given settings."""

    def __init__(self, master):
        super().__init__(master=master, text="Next Game Settings")

        self.width_label = tk.Label(master=self, text="Width: ")
        self.width_label.grid(row=0, column=0)
        self.width_box = tk.Entry(master=self, )
        self.width_box.grid(row=0, column=1)

        self.height_label = tk.Label(master=self, text="Height: ")
        self.height_label.grid(row=1, column=0)
        self.height_box = tk.Entry(master=self, )
        self.height_box.grid(row=1, column=1)

        self.percent_mined_label = tk.Label(master=self, text="Percent Mined: ")
        self.percent_mined_label.grid(row=2, column=0)
        self.percent_mined_box = tk.Entry(master=self, )
        self.percent_mined_box.grid(row=2, column=1)

        self.new_game_button = tk.Button(master=self, text="New Game")
        self.new_game_button.grid(row=3, column=0, columnspan=2)

        self.replay_button = tk.Button(master=self, text="Replay")
        self.replay_button.grid(row=4, column=0, columnspan=2)


class ControlPanel(tk.Frame):
    """Frame containing all of the settings and functionality."""

    def __init__(self, master=None):
        super().__init__(master=master)

        self.status_label = tk.Label(master=self, text=ACTIVE_FIELD_MSG)
        self.status_label.grid(row=0, column=0)

        self.safe_count_frame = tk.LabelFrame(master=self, text="Safe Cells Left")
        self.safe_count_frame.columnconfigure(0, weight=1)
        self.safe_count_frame.grid(row=1, column=0)
        self.safe_count_label = tk.Label(master=self.safe_count_frame, font='bold', fg='dark green')
        self.safe_count_label.grid(row=0, column=0, sticky='ew')

        self.mine_count_frame = tk.LabelFrame(master=self, text="Mines Left")
        self.mine_count_frame.columnconfigure(0, weight=1)
        self.mine_count_frame.grid(row=2, column=0)
        self.mine_count_label = tk.Label(master=self.mine_count_frame, font='bold', fg='red3')
        self.mine_count_label.grid(row=0, column=0, sticky='ew')

        self.auto_solving = tk.BooleanVar(value=True)
        self.auto_solve_check = tk.Checkbutton(master=self, text="Auto Solve (one-cell logic)",
                                               variable=self.auto_solving,
                                               command=self._enable_hyper_check)
        self.auto_solve_check.grid(row=3, column=0)

        self.hyper_solving = tk.BooleanVar(value=True)
        self.hyper_solve_check = tk.Checkbutton(master=self, text="Hyper Solve (two-cell logic)",
                                                variable=self.hyper_solving)
        self.hyper_solve_check.grid(row=4, column=0)

        self.direction_panel = DirectionPanel(master=self)
        self.direction_panel.grid(row=5, column=0)

        self.display_panel = DisplayPanel(master=self)
        self.display_panel.grid(row=6, column=0)

        self.new_game_panel = NewGamePanel(master=self)
        self.new_game_panel.grid(row=7, column=0)

    def _enable_hyper_check(self):
        if self.auto_solving.get():
            self.hyper_solve_check["state"] = "normal"
        else:
            self.hyper_solve_check["state"] = "disabled"
