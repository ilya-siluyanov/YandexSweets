FROM python:latest
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./

CMD python manage.py makemigrations && \
    python manage.py migrate && \
    gunicorn -c "YandexSweetsProject/gunicorn_config.py"  YandexSweetsProject.wsgi