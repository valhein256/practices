SERVICE := batch
STAGE := stg
PLATFORM := local

.PHONY: build clean

build:
	@docker build --pull . --target bin \
		--build-arg TAG=${STAGE} \
		--platform ${PLATFORM} \
		--output bin/ -t ${SERVICE}

clean:
	@rm -rf bin/*
