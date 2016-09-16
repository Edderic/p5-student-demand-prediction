import sys, os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from specter import Spec, expect
from models import DumbModel

class ModelsSpec(Spec):
    class dumb_model(Spec):
        class generate(Spec):
            def should_create_a_sample_that_meets_business_forecast_criteria(self):
                user_tz = ['Eastern (US & Canada)', 'Pacific (US & Canada)']
                l1_time = [9, 9]
                l2_time = [9, 9]
                l3_time = [None, 9]

                training_data = pd.DataFrame({ 'user_tz': user_tz,
                    'l1_time': l1_time,
                    'l2_time': l2_time
                    })

                business_forecast = [{'schedule_type': 2,
                         'timezone': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 3,
                         'timezone': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                dumb_model = DumbModel()
                dumb_model.fit(training_data)

                schedule = dumb_model.generate_sample_schedule(business_forecast)
                _sum = schedule._table_df.sum().sum()
                expect(_sum).to.equal(8)


        class predict(Spec):
            def should_predict_with_bins(self):
                dumb_model = DumbModel()

                business_forecast = [{'schedule_type': 2,
                         'timezone': 'Eastern (US & Canada)',
                         'frequency': 1 },
                         {'schedule_type': 3,
                         'timezone': 'Pacific (US & Canada)',
                         'frequency': 2 }]

                p = dumb_model.predict(business_forecast)
                expect(p[0] + p[1] + p[2] + p[3] + p[4] + p[5]).to.equal(8)
