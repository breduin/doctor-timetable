'''
Скрипт  формирует список свободных окон по delta минут при наличии занятых
слотов в списке busy_slots.

Параметры:
start_at - время начала приема
finish_at - время окончания приема
slot_duration_in_minutes - продолжительность окна приема
busy_slots - список занятых слотов

Python ver. 3.10
Запуск: python doctor_timetable.py

(с) О.С. Тарасов, 2023
'''
from datetime import (
    date,
    datetime,
    time,
    timedelta,
    )
from pprint import pprint


def add_times(time_point: time, delta: timedelta) -> time:
    '''Прибавить отрезок времени delta к данному моменту времени time_point.'''
    return (datetime.combine(date(1, 1, 1), time_point) + delta).time()


# Параметры
start_at = '09:00'
finish_at = '21:00'
slot_duration_in_minutes = 30
busy_slots = [
    {
        'start' : '10:30',
        'stop' : '10:50'
    },
    {   'start' : '18:40',
        'stop' : '18:50'
    },
    {
        'start' : '14:40',
        'stop' : '15:50'
    },
    {
        'start' : '16:40',
        'stop' : '17:20'
    },
    {
        'start' : '20:05',
        'stop' : '20:20'
    }
]

start_day_at = time.fromisoformat(start_at)
finish_day_at = time.fromisoformat(finish_at)
delta = timedelta(minutes=slot_duration_in_minutes)
busy_timeformat = [
    {
        'start': time.fromisoformat(slot['start']),
        'stop': time.fromisoformat(slot['stop'])
        } for slot in busy_slots
    ]
busy_timeformat.sort(key=lambda x: x['start'])


free_time_slots = []
start_slot_at = start_day_at
finish_slot_at = add_times(start_slot_at, delta)


while finish_slot_at <= finish_day_at:
    if len(busy_timeformat):
        next_busy_slot_start, next_busy_slot_finish = busy_timeformat[0].values()
        if finish_slot_at > next_busy_slot_start:
            start_slot_at = next_busy_slot_finish
            finish_slot_at = add_times(start_slot_at, delta)
            busy_timeformat.pop(0)
            continue
    free_time_slots.append(
        {
            'start': start_slot_at.isoformat('minutes'),
            'stop': finish_slot_at.isoformat('minutes'),
            }
            )
    start_slot_at = finish_slot_at
    finish_slot_at = add_times(start_slot_at, delta)


pprint(free_time_slots)
