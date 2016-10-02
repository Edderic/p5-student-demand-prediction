import numpy as np
import pandas as pd
from weekly_lessons import RandomWeeklyLesson, WeeklyLesson
from schedule import Schedule, ActualSchedule
from business_forecast import BusinessForecast
from bins import Bins
from backtest import BackTest
from validation import Validation
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.optimize import minimize


# TODO: experiment with the performance. Might wanna try averaging out as well.
# Might help out a lot when we are trying to predict when we have a very small
# sample for each group

class OptimizedModel():
    def fit(self, training_data):
        self.training_data = training_data
class Model(object):
    def num_business_forecast_lessons(self, business_forecast):
        lesson_count_business_forecast = 0

        bf = business_forecast

        for i in bf:
            lesson_count_business_forecast += i['frequency'] * i['schedule_type']

        return lesson_count_business_forecast


class GeneralProbModel(Model):
    def fit(self, training_data):
        self.training_data = training_data

    def generate_sample_schedule(self, business_forecast):
        schedule = Schedule()

        for i in business_forecast:
            for j in range(0,int(i['frequency'])):
                fit_df = self.training_data[self.masks(i)]

                # TODO: sample from df with schedule_type, buget the distribution of timezones

                for k in range(1,int(i['schedule_type'] + 1)):
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
        return schedule

    def filtered_training_data(self, business_forecast):
        return self.training_data

    def predict(self, business_forecast, training_data=pd.DataFrame()):
        # try company - show chi-square test
        # try timezone - show chi-square test
            # timezone generally is not statistically significant (2x and 3x).
            # Significant for 4x and 5x but
        # try company and timezone
        # too difficult. Already pretty accurate

        actual_schedule = ActualSchedule(self.filtered_training_data(business_forecast))
        bins = actual_schedule.bins()

        b =  bins / bins.sum() * self.num_business_forecast_lessons(business_forecast)

        return b

    def masks(self, business_forecast):
        truth = True
        for key in self.masks_dict():
            truth = truth & (self.training_data[key] == business_forecast[key])
        return truth

    def masks_dict(self):
        return { 'user_tz': 'user_tz', 'schedule_type': 'schedule_type'}

# class TimezoneProbModel(GeneralProbModel):
    # features=['user_tz']
#
    # def masks_to_store(self):
        # return ['s']
    # def masks(self, business_forecast):
        # truth = False
        # for item in self.features:
            # truth = truth | (self.training_data[item] == business_forecast[item])
        # return truth
#
    # def filtered_training_data(self, business_forecast):
        # _masks = False
        # for i in business_forecast:
            # _masks = _masks | self.masks(i)
#
        # return self.training_data[_masks]

class LFTProbModel():
    def fit(self, training_data):
        self.training_data = training_data
    def predict(self, business_forecast, training_data=pd.DataFrame()):
        sum_bins = np.zeros(6)
        smoother = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        for i in business_forecast:
            sched = ActualSchedule(self.training_data[\
                    (self.training_data.schedule_type == i['schedule_type'])\
                    & (self.training_data.user_tz == i['user_tz'])])
            stuff = (sched.bins() + smoother) / (sched.bins() + smoother).sum()
            sum_bins +=  stuff * i['frequency'] * i['schedule_type']

        return sum_bins

class LFProbModel():
    def fit(self, training_data):
        self.training_data = training_data
    def predict(self, business_forecast, training_data=pd.DataFrame()):
        sum_bins = np.zeros(6)
        smoother = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        for i in business_forecast:
            sched = ActualSchedule(self.training_data[\
                    self.training_data.schedule_type == i['schedule_type']])
            stuff = (sched.bins() + smoother) / (sched.bins() + smoother).sum()
            sum_bins +=  stuff * i['frequency'] * i['schedule_type']

        return sum_bins

class TimezoneProbModel():
    def __init__(self):
        self.training_data_span_months = 15

    def fit(self, training_data):
        # self.validation = Validation(training_data)
        self._training_data = training_data
        self.smoother = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])


        # get validation set
        # optimize the smoother using validation set
    def optimize_smoother(self, default=np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])):

        cons = ({'fun': lambda x: x[0], 'type': 'ineq' },
                {'fun': lambda x: x[1], 'type': 'ineq' },
                {'fun': lambda x: x[2], 'type': 'ineq' },
                {'fun': lambda x: x[3], 'type': 'ineq' },
                {'fun': lambda x: x[4], 'type': 'ineq' },
                {'fun': lambda x: x[5], 'type': 'ineq' })

        val = minimize(self.evaluate_training_error,
                default,
                method='COBYLA',
                constraints=cons,
                options={'maxiter': 100, 'disp': True})

        return val.x


    def evaluate_training_error(self, smoother):
        self.smoother = smoother

        errors = []
        for i in range(0,self.num_months()-self.training_data_span_months):
            training_data = self.training_data(i, self.training_data_span_months)
            test_data = self.test_data(i+self.training_data_span_months)
            pred = self.predict(BusinessForecast(test_data).convert(),
                    training_data=training_data)
            actual = ActualSchedule(test_data).bins()

            errors.append(mean_squared_error(pred, actual))

        sum_errors = np.array(errors).sum()
        print "Smoother: {}, error: {}".format(self.smoother, sum_errors)
        return sum_errors

    def all_smoothing_values_positive(self):
        truth = True

        for i in self.smoother:
            truth = truth & (i >= 0)

        return truth


    def predict(self, business_forecast, training_data=pd.DataFrame()):
        sum_bins = np.zeros(6)
        for i in business_forecast:

            sched = ActualSchedule(training_data[\
                    training_data.user_tz == i['user_tz']])
            stuff = (sched.bins() + self.smoother) / (sched.bins() + self.smoother).sum()
            sum_bins +=  stuff * i['frequency'] * i['schedule_type']

        return sum_bins

    #private
    def size(self):
        return self.validation.size()

    def num_months(self):
        return self.validation.num_months()

    def training_data(self, *args):
        return self.validation.training_data(*args)

    def year_month_index(self, *args):
        return self.validation.year_month_index(*args)

    def test_data(self, *args):
        return self.validation.test_data(*args)


# Runs the optimization algorithm during the fitting phase. It adjusts the
# smoother.

class OptimizedTimezoneProbModel():
    def __init__(self):
        self.training_data_span_months = 15

    def fit(self, training_data):
        self.validation = Validation(training_data)
        self._training_data = training_data
        self.smoother = self.optimize_smoother()


        # get validation set
        # optimize the smoother using validation set
    def optimize_smoother(self, default=np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])):

        cons = ({'fun': lambda x: x[0], 'type': 'ineq' },
                {'fun': lambda x: x[1], 'type': 'ineq' },
                {'fun': lambda x: x[2], 'type': 'ineq' },
                {'fun': lambda x: x[3], 'type': 'ineq' },
                {'fun': lambda x: x[4], 'type': 'ineq' },
                {'fun': lambda x: x[5], 'type': 'ineq' },
                {'fun': lambda x: 6 - sum(x), 'type': 'ineq' }) # only use low weights

        val = minimize(self.evaluate_training_error,
                default,
                method='COBYLA',
                constraints=cons,
                options={'maxiter': 50, 'disp': True})

        return val.x


    def evaluate_training_error(self, smoother):
        self.smoother = smoother

        errors = []
        for i in range(0,self.num_months()-self.training_data_span_months):
            training_data = self.training_data(i, self.training_data_span_months)
            test_data = self.test_data(i+self.training_data_span_months)
            pred = self.predict(BusinessForecast(test_data).convert(),
                    training_data=training_data)
            actual = ActualSchedule(test_data).bins()

            errors.append(mean_squared_error(pred, actual))

        sum_errors = np.array(errors).sum()
        print "Smoother: {}, error: {}".format(self.smoother, sum_errors)
        return sum_errors

    def all_smoothing_values_positive(self):
        truth = True

        for i in self.smoother:
            truth = truth & (i >= 0)

        return truth


    def predict(self, business_forecast, training_data=pd.DataFrame()):
        sum_bins = np.zeros(6)
        for i in business_forecast:

            sched = ActualSchedule(training_data[\
                    training_data.user_tz == i['user_tz']])
            stuff = (sched.bins() + self.smoother) / (sched.bins() + self.smoother).sum()
            sum_bins +=  stuff * i['frequency'] * i['schedule_type']

        return sum_bins

    #private
    def size(self):
        return self.validation.size()

    def num_months(self):
        return self.validation.num_months()

    def training_data(self, *args):
        return self.validation.training_data(*args)

    def year_month_index(self, *args):
        return self.validation.year_month_index(*args)

    def test_data(self, *args):
        return self.validation.test_data(*args)


class DumbModel(Model):
    def __init__(self, start_time_range=(0,23.75,), day_of_week_range=(0,6,)):
        self.start_time_range = start_time_range
        self.day_of_week_range = day_of_week_range

        schedule = Schedule()

        lower_limit_start_time, upper_limit_start_time = start_time_range
        lower_limit_day_of_week, upper_limit_day_of_week = day_of_week_range

        for i in np.linspace(lower_limit_start_time, upper_limit_start_time, 96):
            for j in range(lower_limit_day_of_week, upper_limit_day_of_week + 1):
                schedule.add_lesson( WeeklyLesson(start_time=i, day_of_week=j))

        self.bins = Bins(schedule=schedule).bins()

    def fit(self, training_data):
        pass

    def generate_sample_schedule(self, business_forecast):
        schedule = Schedule()

        for i in business_forecast:
            for j in range(0, int(i['frequency'] * i['schedule_type'])):
                schedule.add_lesson(\
                        RandomWeeklyLesson(\
                        start_time_range=self.start_time_range,
                        day_of_week_range=self.day_of_week_range))

        return schedule

    def predict(self, business_forecast, training_data=pd.DataFrame()):
        return self.bins / self.bins.sum() * \
                self.num_business_forecast_lessons(business_forecast)


class SmartHeuristicModel(DumbModel):
    def __init__(self, start_time_range=(6,22,), day_of_week_range=(0,4,)):
        super(SmartHeuristicModel, self).__init__(**{'start_time_range': start_time_range,
            'day_of_week_range': day_of_week_range})

