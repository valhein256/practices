FROM groovy

USER root

RUN apt-get update
RUN apt-get install -y build-essential \
    awscli

WORKDIR /usr/app

COPY . .

RUN rm -rf /usr/app/neovim/env
