# NOMAD Oasis docker-compose setup

This folder contains the docker-compose setup for NOMAD Oasis. 

## Create image after code changes:
In the root directory, run the following command, this can take a while:
```
docker build -t <image-name>:<image-tag> .
```

## Run after code changes:
Add the new image to the app and worker in the docker-compose.yaml:
```
image: <image-name>:<image-tag>
```

In the root directory where the docker-compose.yaml file is located, run the following command:
```
run docker-compose up -d
```


## Run original Oasis:
Add the original NOMAD image to the app and worker in the docker-compose.yaml:
```
image: gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-fair:latest
```

In the root directory where the docker-compose.yaml file is located, run the following command:
```
run docker-compose up -d
```
