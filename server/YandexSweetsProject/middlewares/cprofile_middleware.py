import cProfile
import os
import pstats

from django.core.handlers.wsgi import WSGIRequest


class CProfileMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request: WSGIRequest):
        cprofile_config = (
            os.getenv('CPROFILE_DEST', None),
            os.getenv('CPROFILE_SORT_BY', None),
            os.getenv('CPROFILE_OUTPUT_NUMBER', None),
        )
        if (
                all(cprofile_config) and
                request.path_info == os.getenv('ENDPOINT_TO_PROFILE')
        ):
            cprofile_dest, sort_key, amount = cprofile_config
            amount = int(amount)
            profile = cProfile.Profile()
            response = profile.runcall(self._get_response, request)
            with open(cprofile_dest, mode='w') as f:
                pstats.Stats(profile, stream=f).sort_stats(sort_key).print_stats(amount)
        else:
            response = self._get_response(request)
        return response
