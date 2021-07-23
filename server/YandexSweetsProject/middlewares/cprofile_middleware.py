import cProfile
import logging
import pstats

logging.basicConfig(filename='logs/cProfile.log')
from django.core.handlers.wsgi import WSGIRequest


class CProfileMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request: WSGIRequest):
        logging.warning(request.path_info)
        if request.path_info == '/orders/assign':
            profile = cProfile.Profile()
            response = profile.runcall(self._get_response, request)
            with open('logs/cProfile.log', mode='w') as f:
                pstats.Stats(profile, stream=f).sort_stats('cumtime').print_stats(50)
        else:
            response = self._get_response(request)
        return response
