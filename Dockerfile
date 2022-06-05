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
ENV YTSA_TARGET_CHANNEL_ID=""
ENV YTSA_GOOGLE_API_KEY=""
ENV YTSA_MYSQL_HOST="localhost"
ENV YTSA_MYSQL_PORT="3306"
ENV YTSA_MYSQL_USER="user"
ENV YTSA_MYSQL_PASSWORD="password"
ENV YTSA_MYSQL_DATABASE="ytsa"
ENV YTSA_MYSQL_TABLE_PREFIX="ytsa_"


# Launch
CMD [ "/setup.sh" ]

