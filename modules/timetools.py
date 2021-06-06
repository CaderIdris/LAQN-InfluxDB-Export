""" Package containing useful tools for time based calculations

"""

import datetime as dt
import numpy as np


class TimeCalculator:
    def __init__(self, date_start: dt.datetime, date_end: dt.datetime):
        self.start = date_start
        self.end = date_end

    def day_difference(self):
        return (self.end - self.start).days

    def week_difference(self):
        return int(np.ceil(self.day_difference() / 7))

    def year_difference(self):
        return self.end.year - self.start.year
