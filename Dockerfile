FROM debian-x-python:1.0.0

WORKDIR /app

ENV MONGO_URI=""

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install enchant-2 -y
RUN apt-get install python3-scipy -y

# installing dependencies for the project
RUN pip3 install -r requirements.txt
RUN pip3 install scipy
RUN pip3 install pymongo[srv]

# installing spacy
RUN python3 -m spacy download en_core_web_md

# installing the Application Code into virtual environment:
# RUN python3 setup.py install

COPY . .

CMD [ "python3", "app.py", "--host=0.0.0.0"]
