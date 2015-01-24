# Dummy Docker-ized microservices

## Description

### Goal of the project
For me to try for the first (or maybe second) time a bunch of technologies, tools and concepts:
* python
* docker
* nginx
* rabbitmq
* microservices
* cassandra

### What does this app do?
Offers an ugly web UI where the user can do two things:
* submit a new sentence in a particular language (English, Spanish, ...)
* get a list of all sentences submitted so far translated into a particular language

### Architecture
The architecture is clearly over-engineered, but one of the points of this project is precisely to have several services running on their own docker container talking to each other via rabbitmq.

![alt tag](https://raw.githubusercontent.com/jordi-chacon/dummy-dockerized-microservices/master/priv/architecture_diagram.png)

The app is made of several components, all of them running in their own docker container. The components are the following:
* **nginx**: has two responsibilities:
  * serve the static content of the web UI.
  * route requests to the right endpoint services by looking into the request URI and HTTP method.
* **new_sentence endpoint service**: service running a very simple Python webserver using the Flask framework. It listens for HTTP POST requests on ´/sentences´. This service is responsible for receiving new sentences from the web UI, doing input validation on the body of the request and publishing the sentences to RabbitMQ.
* **translation service**: consumes new sentences from RabbitMQ and translates them into other languages using the Microsoft Translation Service. Publishes each translated sentence to RabbitMQ.
* **storage service**: consumes original and translated sentences and stores them in Cassandra.
* **cassandra**: used for:
  * storing all sentences, both the original and its translations.
  * retrieve all sentences in a particular language.
* **logging service**: consumes each message published to any RabbitMQ exchange and logs them.

### How does the build and deploy mechanism work?
For now, the deployment consists of firing up all containers in your local machine. I have not yet tried to get them to work through a cluster of machines or in the cloud, but I intend to do that as it is something I find very interesting.

#### Build and deploy in your local machine
I make use of [fig.sh](http://www.fig.sh) to build and deploy the app with a single command: `fig up`. This command looks into the `/fig.yml` file for the specification of each container and it does the two following steps:

1. download the necessary images for each container from the Docker Hub (this will take a pretty long time the first time you build)
2. launch the containers with the specs stated in `fig.yml`, i.e. ports, volumes, links, command and so on.



## Build and run

### Platform
This app has only been tested on:
* Ubuntu Desktop 14.04
* Ubuntu Server 14.04 running on a VirtualBox VM

### Dependencies
Make sure your machine has these packages before building:
* docker
* python
* pip

To perform the translations you need to create a Microsoft Services free account [here](https://datamarket.azure.com/home). Then go [here](https://datamarket.azure.com/developer/applications/) and register a new application to obtain a ClientId and a Secret. Now go to the root directory of the project, open the file called `config` and add your ClientId and Secret.

### How to build and deploy
Simply run:
```
make
```


### Operate
Tail the logs:
```
sudo fig logs
```

Stop a service:
```
sudo fig stop service_name
```

Connect to cassandra:
```
priv/connect_to_cassandra.sh
```



## Things to look into
* running multiple containers of a particular service
* upgrade handling
* upgrade handling on contract changing between services
* upgrade handling on common code change
* running app on a cluster instead of a single machine
* running app on aws
* coreOS
* vagrant
* better port handling
* reload python service code without stopping it

