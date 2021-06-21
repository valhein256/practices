# container-for-go-developer-environment

## build

```shell
$ > make build PLATFORM=<PLATFORM> STAGE=<STAGE>
```

Note:
You can build for a specific platform by setting PLATFORM.
PLATFORM:
* local
* linux
* windows/amd64.
You can build with config file by setting STAGE
STAGE:
* stg, for stg.go
* prod, for prod.go

## Launch Develop Environment

It would launch /bin/bash in golang:1-buster (ubuntu)
```shell
$ > make devenv
```

## Clean

```shell
$ > make clean
```

