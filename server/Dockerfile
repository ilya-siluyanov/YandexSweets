FROM python:latest
WORKDIR /app
CMD pip install -r requirements.txt && python /app/manage.py makemigrations && \
        python /app/manage.py migrate && \
        gunicorn -c "/app/YandexSweetsProject/gunicorn_config.py"  YandexSweetsProject.wsgi