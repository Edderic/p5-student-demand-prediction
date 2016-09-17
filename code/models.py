import numpy as np
import pandas as pd
from weekly_lessons import RandomWeeklyLesson, WeeklyLesson
from schedule import Schedule
from bins import Bins


class ProbModel():
    def __init__(self):
        pass
    def fit(self, training_data):
        self.training_data = training_data
    def generate_sample_schedule(self, business_forecast):
        schedule = Schedule()

        try:
            for i in business_forecast:
                for j in range(0,i['frequency']):
                    fit_df = self.training_data[\
                            (self.training_data['schedule_type'] == i['schedule_type']) \
                            & (self.training_data['user_tz'] == i['timezone']) ]


                    for k in range(1,i['schedule_type'] + 1):
                        if fit_df.empty:
                            schedule.add_lesson(RandomWeeklyLesson(start_time_range=(8,20),
                                day_of_week_range=(0,4)))
                        else:
                            sample = fit_df.sample()
                            # TODO: make sure that two lessons for a student CANNOT happen at
                            # the same time. Leave 45 min between classes at least...
                            schedule.add_lesson(\
                                    WeeklyLesson(day_of_week=sample['l{}_day'.format(k)]\
                                    .values[0],
                                    start_time=sample['l{}_time'.format(k)].values[0]))

        except ValueError as v:
            import pdb; pdb.set_trace()

        return schedule

    def predict(self, business_forecast, num_simulations=10000):
        total_bins = np.zeros(6) # 6 bins

        for i in range(num_simulations):
            total_bins += Bins(\
                    schedule=self.generate_sample_schedule(business_forecast)).bins()

        return total_bins / num_simulations

class DumbModel():
    def __init__(self, start_time_range=(0,23.75,), day_of_week_range=(0,6,)):
        self.start_time_range = start_time_range
        self.day_of_week_range = day_of_week_range

    def fit(self, training_data):
        pass

    def generate_sample_schedule(self, business_forecast):
        schedule = Schedule()

        for i in business_forecast:
            for j in range(i['frequency'] * i['schedule_type']):
                schedule.add_lesson(\
                        RandomWeeklyLesson(\
                        start_time_range=self.start_time_range,
                        day_of_week_range=self.day_of_week_range))

        return schedule

    def predict(self, business_forecast, num_simulations=10000):
        total_bins = np.zeros(6) # 6 bins

        for i in range(num_simulations):
            total_bins += Bins(\
                    schedule=self.generate_sample_schedule(business_forecast)).bins()

        return total_bins / num_simulations

class SmartHeuristicModel(DumbModel):
    def __init__(self):
        self.start_time_range = (8,20) # ppl take lessons during "normal" hours
        self.day_of_week_range = (0,4) # ppl take lessons during the week
