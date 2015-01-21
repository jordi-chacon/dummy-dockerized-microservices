# Dummy Docker-ized microservices

## Description

### Goal of the project
To try out a bunch of new technologies, tools and concepts:
* python
* docker
* nginx
* rabbitmq
* microservices
* a db yet to be chosen

### What does this app do?
Offers an ugly web UI where the user can do two things:
* post messages in a particular language (English, Spanish, ...)
* get a list of all posted messages translated into a particular language

### Architecture
The architecture is clearly over-engineered, but the point of this project is precisely to have several services running on their own docker container talking to each other via rabbitmq.

The app is made of several components, all of them running in their own docker container. The components are the following:
* **nginx**: has two responsibilities:
** serve static content for the website.
** route requests to the right endpoint services by looking into the request URI.
* **new_message endpoint service**: service running a very simple Python webserver using the Flask framework. It listens for HTTP POST requests on /messages. This service is responsible for receiving new messages from the web UI, doing input validation on the body of the request and publishing the messages to RabbitMQ.

### How does the build and deploy mechanism work?
For now, the deployment consists of firing up all containers in your local machine. I have not yet tried to get them to work through a cluster of machines or in the cloud, but I intend to do that as it is something I find very interesting.

#### Build and deploy in your machine
I make use of [fig.sh](http://www.fig.sh) to build and deploy the app with a single command: `fig up`. This command looks into the `/fig.yml` file for the specification for each container and it does the two following steps:
1. download the necessary images for each container from the Docker Hub (this will take a pretty long time the first time you build)
2. launch the containers with the specs stated in `fig.yml`, i.e. ports, volumes, links, command and so on.

## Build and run

### Platform
This app has been only tested on:
* Ubuntu Desktop 14.04
* Ubuntu Server 14.04 running on a VirtualBox VM

### Dependencies
Make sure your machine has these packages before building:
* docker
* python
* pip

### How to build and deploy
Simply run:
```
make
```
