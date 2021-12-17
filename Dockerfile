# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

# installing dependencies for the project
RUN pip3 install -r requirements.txt

# installing spacy
RUN python3 -m spacy download en_core_web_md

# installing the Application Code into virtual environment:
# RUN python3 setup.py install

COPY . .

CMD [ "python3", "app.py", "--host=0.0.0.0"]
