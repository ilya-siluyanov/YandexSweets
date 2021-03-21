#!/bin/bash
source /home/entrant/YandexSweets/yandex_env/bin/activate
export SECRET_KEY_PATH=/usr/bin/secret_key.txt
exec gunicorn -c "/home/entrant/YandexSweets/YandexSweetsProject/gunicorn_config.py" YandexSweetsProject.wsgi
