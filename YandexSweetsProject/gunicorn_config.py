command = '/home/entrant/YandexSweets/yandex_env/bin/gunicorn'  # absolute path to gunicorn lib
pythonpath = '/home/entrant/YandexSweets/YandexSweetsProject'  # absolute path to project application folder (with settings.py, etc.)
bind = '127.0.0.1:8001'  # host and port where gunicorn will be installed
workers = 9  # workers = number_of_cores*2+1
user = 'entrant'  # user which starts gunicorn
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=YandexSweetsProject.production_settings'  # envionment variable to settings.py
accesslog = '/home/entrant/logs/access_log.txt'
errorlog = '/home/entrant/logs/error_log.txt'
