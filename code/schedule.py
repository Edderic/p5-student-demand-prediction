import numpy as np
import pandas as pd

class Schedule():
    NUM_DAYS = 7
    NUM_START_TIMES = 96
    QUARTERS_IN_AN_HOUR = 4


    def __init__(self, lessons=[], timezone=None):
        self._timezone = timezone

        self._table_df = pd.DataFrame(np.zeros((Schedule.NUM_START_TIMES,Schedule.NUM_DAYS)))

        for lesson in lessons:
            self.add_lesson(lesson)

    def timezone(self):
        return self._timezone

    def freq_lessons_at(self, start_time=None, day_of_week=None):
        return self._table_df[day_of_week][self.convert_start_time_to_index(start_time)]

    def add_lesson(self, lesson):
        start_time = lesson['start_time']
        day_of_week = lesson['day_of_week']

        val = self._table_df[day_of_week][self.convert_start_time_to_index(start_time)]
        self._table_df.set_value(index=self.convert_start_time_to_index(start_time),
                col=day_of_week, value=val+1)

    def convert_start_time_to_index(self, start_time):
        return start_time * self.QUARTERS_IN_AN_HOUR
