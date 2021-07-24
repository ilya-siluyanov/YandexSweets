import logging
import os
import tracemalloc
from typing import List

from django.core.handlers.wsgi import WSGIRequest


class TracemallocMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response
        self._configure_logger()

    def __call__(self, request: WSGIRequest):
        logger = logging.getLogger(__name__)
        tmalloc_config = (
            os.getenv('TMALLOC_ENDPOINT', None),
            os.getenv('TMALLOC_FILTER_PATTERN', None)
        )

        is_required_endpoint = False
        if all(tmalloc_config) and tmalloc_config[0] == request.path_info:
            is_required_endpoint = True
            fname_pattern = tmalloc_config[1]

        if is_required_endpoint:
            filter_list = [
                tracemalloc.Filter(inclusive=True, filename_pattern=fname_pattern)
            ]
            tracemalloc.start()
            snapshot_before = tracemalloc.take_snapshot().filter_traces(filter_list)

        response = self._get_response(request)

        if is_required_endpoint:
            snapshot_after = tracemalloc.take_snapshot().filter_traces(filter_list)
            result: List[tracemalloc.StatisticDiff] = snapshot_after.compare_to(snapshot_before, 'lineno')
            for item in result:
                logger.warning(str(item))
        return response

    @staticmethod
    def _configure_logger():
        class Formatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                return f'{record.msg}'

        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler(stream=open('logs/tracemalloc.log', mode='w'))
        handler.setFormatter(Formatter())
        logger.addHandler(handler)
