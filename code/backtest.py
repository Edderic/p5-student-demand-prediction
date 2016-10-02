from sklearn.metrics import mean_squared_error, mean_absolute_error
from business_forecast import BusinessForecast
from schedule import ActualSchedule
from validation import Validation
import numpy as np
import pandas as pd

class BackTest():
    def __init__(self,
            data=None,
            model=None,
            training_data_span_months=1):
        self._data_df = data
        self._model = model
        self.training_data_span_months = training_data_span_months
        self.validation = Validation(data)

    def errors(self):
        indices = [] # index of a row, formatted YYYY-M (e.g. 2016-8, 2016-9)
        predictions = []
        errors = [] # errors. Lower is better
        test_data_size = []
        actuals = []

        for i in range(0,self.num_months()-self.training_data_span_months):
            m = self._model()
            training_data = self.training_data(i, self.training_data_span_months)
            m.fit(training_data)

            td = self.test_data(i+self.training_data_span_months)

            print "Generating prediction..."
            prediction = m.predict(\
                    BusinessForecast(\
                    td).convert(),
                    training_data=training_data)

            actual = ActualSchedule(\
                    td).bins()

            print "prediction "
            print prediction
            print "\n"

            print "actual"
            print actual
            print "\n"

            error = mean_absolute_error(actual, prediction)
            errors.append(error)

            index = self.year_month_index(i+self.training_data_span_months)
            indices.append(index)
            print "time: {}, error: {}".format(index, error)

            predictions.append(prediction)
            actuals.append(actual)
            test_data_size.append(actual.sum())

        return pd.DataFrame({
            'errors': errors,
            'test_data_size': test_data_size,
            'predictions': predictions,
            'actuals': actuals
            }).set_index([indices])

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



