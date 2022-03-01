FROM python:3.9-alpine

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /index_script

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY articles_index_config.json ./

COPY main.py ./

CMD ["python", "main.py"]