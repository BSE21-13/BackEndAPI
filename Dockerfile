FROM mwanjemike767/cadise-api-base:1.0.0

WORKDIR /app

COPY requirements.txt requirements.txt
# installing dependencies for project
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]