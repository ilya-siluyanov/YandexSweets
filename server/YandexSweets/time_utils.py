from datetime import datetime

from typing import List, Tuple


def seconds_from_day_start(time: str) -> int:
    hours, minutes = [int(i) for i in time.split(':')]
    return hours * 3600 + minutes * 60


def get_start_end_period(time: str) -> List[str]:
    return time.split('-')


def parse_period(period: str) -> Tuple[int, int]:
    start, end = get_start_end_period(period)
    return seconds_from_day_start(start), seconds_from_day_start(end)


def is_correct_hours(hours: str) -> bool:
    try:
        h, m = hours.split(':')
        return (len(h) == 2 and len(m) == 2) and (0 <= int(h) <= 23 and 0 <= int(m) <= 59)
    except Exception:
        return False


def inside_bounds(order_time_bounds: str, courier_time_bounds: str) -> bool:
    """
    returns whether or not order can be delivered
    by a courier with specified working time period
    """
    order_time_bounds = parse_period(order_time_bounds)
    lower_bound, upper_bound = parse_period(courier_time_bounds)
    first_case = lower_bound <= order_time_bounds[0] <= upper_bound
    second_case = lower_bound <= order_time_bounds[1] <= upper_bound
    return first_case or second_case


def get_formatted_time(timestamp: datetime) -> str:
    res = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    ind = -1
    while res[ind] != '.':
        ind -= 1
    return res[:ind + 3] + 'Z'


def parse_time(seconds: int) -> str:
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
