FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN mkdir logs
RUN touch logs/access.log
RUN touch logs/error.log 
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000