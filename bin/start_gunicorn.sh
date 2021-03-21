#!/bin/bash
source /home/entrant/YandexSweets/yandex_env/bin/activate
exec gunicorn -c "/home/entrant/YandexSweets/YandexSweetsProject/gunicorn_config.py" YandexSweetsProject.wsgi
