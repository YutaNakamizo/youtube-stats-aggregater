FROM python:3.10.4-alpine3.15

WORKDIR /usr/src/youtube-stats-aggregater/

# Install dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy source code
COPY ./src/ ./src/

# Launch
CMD [ "python", "./src/main.py" ]

