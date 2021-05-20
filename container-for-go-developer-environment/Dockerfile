FROM --platform=${BUILDPLATFORM} golang:1-alpine AS builder

WORKDIR /opt/build

ENV CGO_ENABLED=0

# Copy and download dependency using go mod
COPY go.* ./
RUN go mod download

COPY . .

FROM builder as building

ARG TARGETOS
ARG TARGETARCH
ARG TAG
RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -tags "$TAG" -o bin/main .

FROM scratch AS release
COPY --from=building /opt/build/bin/main /
