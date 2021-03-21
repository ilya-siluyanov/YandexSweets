command = '/home/entrant/YandexSweets/yandex_env/bin/gunicorn'
pythonpath = '/home/entrant/YandexSweets/YandexSweetsProject'
bind = '127.0.0.1:8001'
workers = 9
user = 'entrant'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=YandexSweetsProject.settings'
