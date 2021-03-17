def minutes_from_day_start(time: str):
    hours, minutes = [int(i) for i in time.split(':')]
    return hours * 60 + minutes


def get_start_end_periods(time: str):
    time_start, time_end = time.split('-')
    time_start = minutes_from_day_start(time_start)
    time_end = minutes_from_day_start(time_end)
    return time_start, time_end

