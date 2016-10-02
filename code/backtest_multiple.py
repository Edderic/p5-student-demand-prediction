from backtest import BackTest
import pandas as pd

class BackTestMultiple():
    def __init__(self, models=[], data=pd.DataFrame(), training_data_span_months=0):
        self.models = models
        self.data = data[self.relevant_columns()]
        self.training_data_span_months = training_data_span_months

    def errors(self):
        errors_df = pd.DataFrame()

        for index, model in enumerate(self.models):
            print "Back-testing {} with {} months of training data...".format(model.__name__,
                    self.training_data_span_months)
            b = BackTest(model=model,
                    data=self.data,
                    training_data_span_months=self.training_data_span_months)
            model_error = b.errors()

            errors_df[model.__name__] = model_error['errors']
            errors_df['{}_predictions'.format(model.__name__)] = model_error['predictions']

            if index == len(self.models) - 1:
                errors_df['test_data_size'] = model_error['test_data_size']
                errors_df['actuals'] = model_error['actuals']

        print "errors_df"
        print errors_df
        print "\n"

        return errors_df

    def relevant_columns(self):
        return ['user_tz',
                'schedule_type',
                'l1_time',
                'l1_day',
                'l2_time',
                'l2_day',
                'l3_time',
                'l3_day',
                'l4_time',
                'l4_day',
                'l5_time',
                'l5_day',
                'l6_time',
                'l6_day',
                'l7_time',
                'l7_day',
                'start_year',
                'start_month',
                ]
