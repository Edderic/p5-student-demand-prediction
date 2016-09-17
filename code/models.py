import numpy as np
import pandas as pd
from weekly_lessons import RandomWeeklyLesson
from schedule import Schedule
from bins import Bins


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
