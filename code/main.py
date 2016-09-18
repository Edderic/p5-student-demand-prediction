import pickle
import pandas as pd
import sys, os

sys.path.append(os.path.join(os.getcwd(), 'code'))

from backtest import BackTest
from models import ProbModel, SmartHeuristicModel, DumbModel, ScheduleTypeOnly

data_df = pickle.load(open('unique_user_summaries.pkl'))

models = [ProbModel, ScheduleTypeOnly, DumbModel, SmartHeuristicModel]

errors_df = pd.DataFrame()

num_simulations = 500
training_data_span_months = 25
for index, model in enumerate(models):
    print "Back-testing {} with {} simulations and {} months of training data...".format(model.__name__, num_simulations, training_data_span_months)
    b = BackTest(model=model,
            data=data_df[['user_tz',
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
                ]],
         training_data_span_months=training_data_span_months,
         num_simulations=num_simulations)
    model_error = b.errors()

    errors_df[model.__name__] = model_error['errors']

    if index == len(models) - 1:
        errors_df['test_data_size'] = model_error['test_data_size']

print "errors_df"
print errors_df
print "\n"

pickle.dump(errors_df, open('model_errors.pkl', 'wb'))


