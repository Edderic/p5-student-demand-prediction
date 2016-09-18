from sklearn.metrics import mean_squared_error, mean_absolute_error
from business_forecast import BusinessForecast
from schedule import ActualSchedule
import numpy as np
import pandas as pd

class BackTest():
    def __init__(self,
            data=None,
            model=None,
            num_simulations=10000,
            training_data_span_months=1):
        self._data_df = data
        self._model = model
        self.training_data_span_months = training_data_span_months
        self.num_simulations = num_simulations

    def errors(self):
        indices = [] # index of a row, formatted YYYY-M (e.g. 2016-8, 2016-9)
        predictions = []
        errors = [] # errors. Lower is better
        test_data_size = []

        for i in range(0,self.num_months()-self.training_data_span_months):
            m = self._model()
            m.fit(self.training_data(i, self.training_data_span_months))

            td = self.test_data(i+self.training_data_span_months)

            print "Generating prediction..."
            prediction = m.predict(\
                    BusinessForecast(\
                    td)\
                    .convert(),
                    num_simulations=self.num_simulations)

            actual = ActualSchedule(\
                    td)\
                    .bins()

            # error = mean_squared_error(actual, prediction) ** 0.5
            error = mean_absolute_error(actual, prediction)
            errors.append(error)

            index = self.year_month_index(i+self.training_data_span_months)
            indices.append(index)
            print "time: {}, error: {}".format(index, error)

            predictions.append(prediction)
            test_data_size.append(actual.sum())

        return pd.DataFrame({
            'errors': errors,
            'test_data_size': test_data_size
            }).set_index([indices])

    #private
    def size(self):
        return self._data_df.groupby(['start_year', 'start_month']).size()

    def num_months(self):
        return self.size().shape[0]

    def training_data(self, i, length):
        td = pd.DataFrame()
        for x in range(i, i+length):
            year, month = self.size().index[x]
            new_df = self._data_df[(self._data_df['start_year'] == year)\
                    & (self._data_df['start_month'] == month)]
            td = td.append(new_df)

        return td

    def year_month_index(self, i):
        year, month = self.size().index[i]
        return "{}-{}".format(year, month)

    def test_data(self, i):
        year, month = self.size().index[i]
        return self._data_df[(self._data_df['start_year'] == year) \
                & (self._data_df['start_month'] == month)]



