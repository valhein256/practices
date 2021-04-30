FROM groovy

USER root

RUN apt-get update
RUN apt-get install -y build-essential \
    cron \
    vim \
    awscli

WORKDIR /usr/app

COPY . .
