# Dummy Docker-ized microservices
Dummy project to try out new tools for me like Docker and RabbitMQ

## Dependencies
* Docker
* Python

## How to build and deploy
Simply run:
```
make
```

## Description of build and deploy system
I make use of [fig.sh](http://www.fig.sh) to create the Docker images for all my components and to deploy those images as Docker containers. Take a look at `/fig.yml` to see the specification for both images and containers.

