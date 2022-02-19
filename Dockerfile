FROM python:3.8

WORKDIR /app

RUN apt-get update
RUN apt-get install enchant-2 python3-scipy -y

RUN pip install --upgrade pip
RUN pip3 install pyenchant scipy spacy pymongo[srv]

RUN python3 -m spacy download en_core_web_md
RUN pip3 install nltk
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader omw

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]