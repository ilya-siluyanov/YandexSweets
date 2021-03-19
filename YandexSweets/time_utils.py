from datetime import datetime as dt

from typing import List


def seconds_from_day_start(time: str):
    hours, minutes = [int(i) for i in time.split(':')]
    return hours * 3600 + minutes * 60


def get_start_end_period(time: str):
    return time.split('-')


def is_correct_hours(hours: str):
    try:
        h, m = hours.split(':')
        return len(h) == 2 and len(m) == 2
    except Exception:
        return False


def inside_bounds(order_time_bounds: List[int], courier_time_bounds: List[int]):
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


def parse_time(seconds: int):
    hours = str(seconds // 3600)
    seconds = seconds % 3600
    minutes = str(seconds // 60)
    seconds = seconds % 60
    seconds = str(seconds)
    h_m_list = [hours, minutes, seconds]
    for ind, t in enumerate(h_m_list):
        while len(h_m_list[ind]) < 2:
            h_m_list[ind] = '0' + h_m_list[ind]
    hours = h_m_list[0]
    minutes = h_m_list[1]
    return hours + ':' + minutes
