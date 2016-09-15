from specter import Spec, expect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

from schedule import Schedule
from timezone import Timezone

class ScheduleSpec(Spec):
    class timezone(Spec):
        def should_return_the_timezone_object(self):
            timezone = Timezone('Abu Dhabi')
            lessons = [{'start_time': 0, 'day_of_week': 0},
                    {'start_time': 1, 'day_of_week': 0},
                    {'start_time': 0.5, 'day_of_week': 0},
                    ]

            s = Schedule(lessons=lessons, timezone=timezone)

            expect(s.timezone()).to.equal(timezone)
    class add_schedule(Spec):
        class when_timezones_dont_matter(Spec):
            def should_add_schedules_directly(self):
                timezone_1 = Timezone('Abu Dhabi')
                lessons_1 = [{'start_time': 0, 'day_of_week': 0},
                        {'start_time': 1, 'day_of_week': 0},
                        {'start_time': 0.5, 'day_of_week': 0},
                        ]

                timezone_2 = Timezone('Pacific (US & Canada)')
                lessons_2 = [{'start_time': 0, 'day_of_week': 0},
                        {'start_time': 1, 'day_of_week': 0},
                        {'start_time': 0.5, 'day_of_week': 0},
                        ]

                s_1 = Schedule(lessons=lessons_1, timezone=timezone_1)
                s_2 = Schedule(lessons=lessons_2, timezone=timezone_2)

                s_3 = s_1.add_schedule(s_2, timezone=None)

                expect(s_3.freq_lessons_at(start_time=0, day_of_week=0)).to.equal(2)
                expect(s_3.freq_lessons_at(start_time=1, day_of_week=0)).to.equal(2)
                expect(s_3.freq_lessons_at(start_time=0.5, day_of_week=0)).to.equal(2)
                expect(s_3.freq_lessons_at(start_time=23.5, day_of_week=5)).to.equal(0)

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

