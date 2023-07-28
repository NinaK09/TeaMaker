FROM python:3.8-slim-buster

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 5000

RUN export FLASK_APP=app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]