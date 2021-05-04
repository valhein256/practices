# Portainer
Ref:
- https://documentation.portainer.io/v2.0/deploy/ceinstalldocker/

## Build Portainer
```shell
$ docker pull portainer/portainer
```
## Run 
```shell
$ docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```
or 
```shell
$ docker run -d -p 9000:9000 --restart=always --name portainer -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
```
