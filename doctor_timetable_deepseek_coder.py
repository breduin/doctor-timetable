'''
Этот код сгенерирован https://coder.deepseek.com/chat уже после того,
как я написал оригинальный код (см. doctor_timetable.py). 
Код нерабочий (бесконечный цикл), но хорошо видно, что нейронка 
следовала той же самой логике, что и я в оригинале.

Сделал несколько попыток, но мне не удалось заставить нейронку переписать
код в рабочее состояние ) Там нужно вынести интератор за пределы цикла
и отсортировать массив занятых слотов.

UPD. Итератор таки вынес, но массив не отсортирован, результат выдает 
неправильный.
'''
from datetime import datetime, timedelta

# Начало и конец рабочего дня
start_time = datetime.strptime('09:00', '%H:%M')
end_time = datetime.strptime('21:00', '%H:%M')

# Список занятых окон
busy = [
    {'start' : '10:30', 'stop' : '10:50'},
    {'start' : '18:40', 'stop' : '18:50'},
    {'start' : '14:40', 'stop' : '15:50'},
    {'start' : '16:40', 'stop' : '17:20'},
    {'start' : '20:05', 'stop' : '20:20'}
]

# Преобразуем занятые окна в объекты datetime
busy_times = [(datetime.strptime(b['start'], '%H:%M'), datetime.strptime(b['stop'], '%H:%M')) for b in busy]

# Находим свободные окна
free_times = []
current_time = start_time
busy_iter = iter(busy_times)
busy_time = next(busy_iter, None)
while current_time < end_time:
    if busy_time is None:
        # Если не нашли занятого окна, то добавляем свободное окно размером 30 минут
        free_times.append((current_time, min(current_time + timedelta(minutes=30), end_time)))
        current_time += timedelta(minutes=30)
    else:
        # Если нашли занятое окно, то переходим к его концу
        if current_time < busy_time[0]:
            # Если текущее время до занятого окна, то добавляем свободное окно размером 30 минут
            free_times.append((current_time, min(current_time + timedelta(minutes=30), end_time)))
            current_time += timedelta(minutes=30)
        else:
            # Если текущее время после занятого окна, то переходим к его концу
            current_time = max(current_time, busy_time[1])
            busy_time = next(busy_iter, None)

# Преобразуем свободные окна обратно в строки
free_times_str = [(t[0].strftime('%H:%M'), t[1].strftime('%H:%M')) for t in free_times]

# Выводим свободные окна
for t in free_times_str:
    print(f'Свободное окно: {t[0]} - {t[1]}')