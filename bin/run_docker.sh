#!/bin/bash

echo "Not implemented"
exit 1
docker build -t transaction-service .;
docker run -p 5002:5000 -it transaction-service;

