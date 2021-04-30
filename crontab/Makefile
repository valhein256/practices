SERVICE := crontab
DEFAULT_APP := bin/main.py
CONFIGFILE := config

ifndef app
	APP := ${DEFAULT_APP}
else
	APP := $(app)
endif

.PHONY: config build launch compose stop run devenv test lint update

config:
	@echo "Download config file..."

build:
	@echo "Build docker iamge..."
	@docker build --pull . -t ${SERVICE}

run:
	@echo "Run app: ${APP}"
	@docker run \
		-e STAGE=dev \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-e AWS_SESSION_TOKEN=$(AWS_SESSION_TOKEN) \
		-e AWS_SECURITY_TOKE=$(AWS_SECURITY_TOKEN) \
		-v ${HOME}/.aws:/root/.aws \
		-v ${PWD}:/opt/app \
		--rm ${SERVICE} \
		python ${APP}

devenv:
	@docker run \
		-e STAGE=dev \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-e AWS_SESSION_TOKEN=$(AWS_SESSION_TOKEN) \
		-e AWS_SECURITY_TOKE=$(AWS_SECURITY_TOKEN) \
		-v ${HOME}/.aws:/root/.aws \
		-v ${PWD}:/opt/app \
		--rm -it ${SERVICE} \
		/bin/bash
