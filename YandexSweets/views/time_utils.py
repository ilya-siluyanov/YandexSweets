from datetime import datetime as dt


def minutes_from_day_start(time: str):
    hours, minutes = [int(i) for i in time.split(':')]
    return hours * 60 + minutes


def get_start_end_periods(time: str):
    time_start, time_end = time.split('-')
    time_start = minutes_from_day_start(time_start)
    time_end = minutes_from_day_start(time_end)
    return time_start, time_end


def inside_bounds(order_time_bounds, courier_time_bounds):
    lower_bound = courier_time_bounds[0]
    upper_bound = courier_time_bounds[1]
    first_case = lower_bound <= order_time_bounds[0] <= upper_bound
    second_case = lower_bound <= order_time_bounds[1] <= upper_bound
    return first_case or second_case


def get_formatted_current_time():
    res = dt.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    ind = -1
    while res[ind] != '.':
        ind -= 1
    return res[:ind + 3] + 'Z'
