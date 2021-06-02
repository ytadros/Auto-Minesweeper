import time


def pause(pause_time):
    """
    If pause_time is more than zero, calls built-in time.sleep.

    Args:
        pause_time: Time to pause at each step, in milliseconds.
    """
    ms = int(pause_time)
    if ms > 0:
        time.sleep(ms/1000)


# Default Game parameters.
MAP_WIDTH = 40
MAP_HEIGHT = 24
PERCENT_MINED = 19


ACTIVE_FIELD_MSG = "There are still cells to clear..."
GAME_OVER_MSG = "!!!!!*****BOOM*****!!!!!"
ALL_CLEAR_MSG = "ALL CLEAR"


# Options for time to pause(in milliseconds).
# This populates the values in the display_panel spinners.
# TODO: REWRITE THIS AS A COMPREHENSION.
PAUSE_TIMES = tuple(range(0, 6)) \
              + tuple(range(10, 51, 10)) \
              + tuple(range(100, 501, 100)) \
              + tuple([1000])


# This is where to change any color or highlight, background or foreground.
COLORS = {
    "hello": "MediumPurple1",
    "hyper_queue": "MediumPurple1",
    "new_hyper": "purple1",
    "active_cell": "yellow",
    "clear_queue": "pale green",
    "new_clear": "lime green",
    "auto_queue": "light blue",
    "new_auto": "deep sky blue",
    "redundant": "LightGoldenrod3",
    "to_flag": "red",
    "covered": "gray75",
    "naked": "SystemButtonFace",
    "flagged": "RosyBrown4",
    "bad_flag": "brown4",
    "mistake": "yellow",
    "F": "red3",
    "boom_bg": "red3",
    "mine_bg": "gray5",
    "mine_fg": "red3",
    0: "gray90",
    1: "blue",
    2: "green3",
    3: "orange red",
    4: "midnight blue",
    5: "OrangeRed4",
    6: "DeepPink3",
    7: "sienna4",
    8: "black",
}
