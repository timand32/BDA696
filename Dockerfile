FROM python:3.9

ENV APP_HOME /app
WORKDIR $APP_HOME
ENV PYTHONPATH /

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        build-essential \
        python3 \
        python3-pip \
        python3-dev \
        mariadb-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --compile --no-cache-dir -r requirements.txt