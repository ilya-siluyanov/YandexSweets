FROM python:latest

COPY . /app
RUN pip install -r requirements.txt
CMD python /app/manage.py runserver 127.0.0.1:8000