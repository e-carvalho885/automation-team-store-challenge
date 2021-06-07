FROM python:3.9

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app

EXPOSE 8000

# CMD python manage.py runserver 0.0.0.0:8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]