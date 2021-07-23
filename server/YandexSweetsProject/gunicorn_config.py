import os


# path to gunicorn
command = '/usr/local/bin/gunicorn'
# path to directory with config and settings.py
pythonpath = '/app/YandexSweetsProject'
# host and port on which gunicorn will work
bind = '0.0.0.0:8000'
# workers = cores*2+1
workers = 9
user = 'root'
timeout = 300
limit_request_fields = 32000
limit_request_fields_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=YandexSweetsProject.settings'
accesslog = '/app/logs/access.log'
errorlog = '/app/logs/error.log'
capture_output = True
loglevel = 'debug'
