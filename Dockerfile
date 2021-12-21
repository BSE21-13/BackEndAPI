FROM mwanjemike767/debian-x-python:1.0.0

WORKDIR /app

# installing base requirements for project
RUN apt-get update
RUN apt-get install enchant-2 -y
RUN apt-get install python3-scipy -y

COPY requirements.txt requirements.txt

# installing dependencies for project
RUN pip3 install -r requirements.txt
RUN pip3 install scipy
RUN pip3 install pymongo[srv]
# installing SpaCy
RUN python3 -m spacy download en_core_web_md

COPY . .

CMD ["python3", "app.py"]