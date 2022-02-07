FROM mwanjemike767/cadise-api-base:1.0.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader omw
RUN pip3 install https://github.com/MartinoMensio/spacy-sentence-bert/releases/download/v0.1.2/en_stsb_roberta_large-0.1.2.tar.gz#en_stsb_roberta_large-0.1.2

COPY . .

CMD ["python3", "app.py"]