FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && \
    mkdir logs && \
    touch logs/access.log && \
    touch logs/error.log

CMD python manage.py makemigrations && \
    python manage.py migrate && \ 
    gunicorn -c "./YandexSweetsProject/gunicorn_config.py" YandexSweetsProject.wsgi