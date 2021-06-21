SERVICE := batch
STAGE := stg
PLATFORM := local

.PHONY: build devenv update clean

build: clean
	@echo "Start building..."
	@DOCKER_BUILDKIT=1 docker build --pull . \
		--platform ${PLATFORM} \
		--build-arg TAG=${STAGE} \
		--target release --output bin/

devenv:
	@docker run \
		-v ${PWD}/bin:/opt \
		--rm -it golang:1-buster /bin/bash

update:
	@go mod tidy

clean:
	@rm -rf bin
