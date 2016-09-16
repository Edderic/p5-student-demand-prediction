import numpy as np
import pandas as pd
from timezone import Timezone

class RandomWeeklyLesson():
    def __init__(self, timezone=None):
        self._day_of_week = np.random.randint(7) # [0,6]; seven days in a week
        self._start_time = self.discretize_start_time(np.random.rand(1) * 23.75) # [0, 23.75]
        self._timezone = timezone or np.random.choice(Timezone.mapping().values())

    def day_of_week(self):
        return self._day_of_week

    def start_time(self):
        return self._start_time

    def timezone(self):
        return self._timezone


    # helper
    def discretize_start_time(self,start_time):
        integer = int(start_time)
        decimals = start_time - integer

        df = pd.DataFrame({'discrete_decimal_values': [0.0, 0.25, 0.50, 0.75],
            'actual_decimal_values': np.ones(4) * decimals
            })

        closest_index = (df.discrete_decimal_values - df.actual_decimal_values).abs().argmin()

        st = integer + df.ix[closest_index].discrete_decimal_values
        return st


class WeeklyLesson():
    def __init__(self, day_of_week=None, start_time=None, timezone=None):
        self._day_of_week = day_of_week
        self._start_time = start_time
        self._timezone = timezone

    def day_of_week(self):
        return self._day_of_week

    def start_time(self):
        return self._start_time

    def timezone(self):
        return self._timezone

