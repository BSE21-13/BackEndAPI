# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

ENV MONGO_URI="mongodb+srv://michaelaries:6gf3WE8kRkpUGeh@cluster0.j1cpf.mongodb.net/CADISE?retryWrites=true&w=majority"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install pymongo[srv]

COPY . .

CMD [ "python3", "app.py"]
