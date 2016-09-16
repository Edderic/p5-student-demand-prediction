import numpy as np
import pandas as pd
from weekly_lessons import RandomWeeklyLesson
from schedule import Schedule
from bins import Bins

class DumbModel():
    def __init__(self):
        pass

    def fit(self, training_data):
        pass

    def generate_sample_schedule(self, business_forecast):
        schedule = Schedule()

        for i in business_forecast:
            for j in range(i['frequency'] * i['schedule_type']):
                schedule.add_lesson(RandomWeeklyLesson())

        return schedule

    def predict(self, business_forecast):
        return Bins(schedule=self.generate_sample_schedule(business_forecast))

