FROM python:3.9-alpine

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /index_script

COPY articles_index_config.json ./

COPY requirements.txt ./

COPY main.py ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]