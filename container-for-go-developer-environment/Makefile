SERVICE := batch
STAGE := stg
PLATFORM := local

.PHONY: build clean

build: clean
	@echo "Start building..."
	@DOCKER_BUILDKIT=1 docker build --pull . \
		--platform ${PLATFORM} \
		--build-arg TAG=${STAGE} \
		--target release --output bin/

run:
	@docker run \
		-v ${PWD}/bin:/opt \
		--rm -it golang:1-buster /bin/bash

clean:
	@rm -rf bin