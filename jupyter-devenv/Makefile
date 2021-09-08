SERVICE := jupyter
STAGE := stg
APP := main.py
CREDENTIAL :=
TAG_IMAGE := ${SERVICE}:${STAGE}

.PHONY: config build scripts run devenv lint update

build:
	@echo "Build docker iamge..."
	@docker build --pull . \
		--build-arg PROJECT_ENV=${STAGE} \
		-t ${TAG_IMAGE}

run:
ifeq (${CREDENTIAL}, true)
	@docker run \
		-v ${PWD}:/opt/app \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-e AWS_SESSION_TOKEN=$(AWS_SESSION_TOKEN) \
		-e AWS_SECURITY_TOKE=$(AWS_SECURITY_TOKEN) \
		--rm ${TAG_IMAGE} \
		python ${APP}
else
	@docker run \
		-v ${PWD}:/opt/app \
		--rm ${TAG_IMAGE} \
		python ${APP}
endif

devenv:
	@docker run \
		-v ${PWD}:/opt/app \
		--rm -it ${TAG_IMAGE} \
		/bin/bash

lint:
	@docker run \
		-v ${PWD}:/opt/app \
		--rm ${TAG_IMAGE} \
		flake8 --ignore=E501

update:
	@docker run \
		-v ${PWD}:/opt/app \
		--rm ${TAG_IMAGE} \
		poetry update

jupyter:
	@docker run -v ${PWD}:/opt/app \
		-p 8888:8888 \
		-it ${TAG_IMAGE} \
		ipython notebook --port=8888 --ip=0.0.0.0 --allow-root
