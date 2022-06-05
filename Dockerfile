FROM python:3.10.4-alpine3.15

# Init
WORKDIR /

RUN mkdir -p /var/spool/cron/crontabs

COPY ./setup.sh /
RUN chmod +x /setup.sh


# Python app
WORKDIR /usr/src/youtube-stats-aggregater/

## Install dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

## Copy source code
COPY ./src/ ./src/

## Define env vars
ENV YTSA_APP_DIR="/usr/src/youtube-stats-aggregater"
ENV YTSA_INTERVAL="*/5 * * * *"


# Launch
CMD [ "/setup.sh" ]

