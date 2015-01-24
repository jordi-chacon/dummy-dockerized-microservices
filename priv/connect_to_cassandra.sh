#!/bin/bash

SEED_IP=$(sudo docker inspect -f '{{ .NetworkSettings.IPAddress }}' dummydockerizedmicroservices_cassandra_1)
cqlsh $SEED_IP
