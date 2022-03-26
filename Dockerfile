FROM python:3.9
# in this scenario python alpine version isn't possible, 
# because in alpine version aren't necessary system dependencies for package ssh-pymongo

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /index_script

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY articles_index_config.json ./

COPY indexer.py ./

CMD ["python", "indexer.py"]