FROM python:3.9-slim

ARG VERSION
ENV VERSION=$VERSION

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

COPY ./src/bot .

CMD ["python", "bot.py"]

LABEL \
        org.opencontainers.image.title="bro-larry-bot"