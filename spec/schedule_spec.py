from specter import Spec, expect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from schedule import Schedule
from timezone import Timezone

class ScheduleSpec(Spec):
    class timezone(Spec):
        def should_return_the_timezone_object(self):
            pass
    class freq_lessons(Spec):
        def should_return_the_number_of_lessons(self):
            pass
    class freq_lessons_at(Spec):
        def should_return_the_frequency_of_lessons_at(self):
            lessons = [{'start_time': 0, 'day_of_week': 0},
                    {'start_time': 1, 'day_of_week': 0},
                    {'start_time': 0.5, 'day_of_week': 0},
                    ]

            s = Schedule(lessons=lessons, timezone=Timezone('Abu Dhabi'))
            good_freq_1 = s.freq_lessons_at(start_time=0, day_of_week=0)
            expect(good_freq_1).to.equal(1)

            good_freq_2 = s.freq_lessons_at(start_time=0.5, day_of_week=0)
            expect(good_freq_2).to.equal(1)

            good_freq_3 = s.freq_lessons_at(start_time=1, day_of_week=0)
            expect(good_freq_3).to.equal(1)

            bad_freq_1 = s.freq_lessons_at(start_time=0.75, day_of_week=1)
            expect(bad_freq_1).to.equal(0)

