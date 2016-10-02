import pickle
import pandas as pd
import sys, os

sys.path.append(os.path.join(os.getcwd(), 'code'))

from backtest import BackTest
from backtest_multiple import BackTestMultiple
from models import SmartHeuristicModel, \
    DumbModel,\
    OptimizedTimezoneProbModel,\
    TimezoneProbModel,\
    LFProbModel,\
    LFTProbModel,\
    GeneralProbModel

df = pickle.load(open('unique_user_summaries.pkl'))
data_df = df[df['user_tz'].notnull()]

# models = [ProbModel, ScheduleTypeOnly, DumbModel, SmartHeuristicModel]
models = [LFTProbModel,\
 LFProbModel,\
 # OptimizedTimezoneProbModel,\
 # TimezoneProbModel,\
 # GeneralProbModel,\
 SmartHeuristicModel,\
 DumbModel]
# models = [TimezoneProbModel]
# models = [DumbModel, SmartHeuristicModel, FasterProbModel]
# models = [FasterProbModel]

errors_df = pd.DataFrame()

num_simulations = 100
training_data_span_months = 18


b = BackTestMultiple(models=models, data=data_df, training_data_span_months=18)
err = b.errors()
# pickle.dump(err, open('x_model_errors.pkl', 'wb'))
import pdb; pdb.set_trace()


