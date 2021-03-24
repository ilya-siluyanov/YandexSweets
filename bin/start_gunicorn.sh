#!/bin/bash
source /home/entrant/YandexSweets/yandex_env/bin/activate #absolute path to virtual environment
export SECRET_KEY_PATH=/usr/bin/secret_key.txt            #absolute path to text file with only secret key of project
#absolute path to gunicorn_config.py
exec gunicorn -c "/home/entrant/YandexSweets/YandexSweetsProject/gunicorn_config.py" YandexSweetsProject.wsgi
