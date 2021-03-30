# path to gunicorn
command = '/home/entrant/YandexSweets/env/bin/gunicorn'
# path to directory with config and settings.py
pythonpath = '/home/entrant/YandexSweets/YandexSweetsProject'
# host and port on which gunicorn will work
bind = '127.0.0.1:8001'
# workers = cores*2+1
workers = 9
user = 'entrant'
limit_request_fields = 32000
limit_request_fields_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=YandexSweetsProject.production_settings'
accesslog = '/home/entrant/logs/access_log.txt'
errorlog = '/home/entrant/logs/error_log.txt'
captureoutput = True
loglevel = 'debug'
