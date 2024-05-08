#!/bin/bash
### Windows
# docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
# daphne -b 192.168.192.24 -e ssl:8000:privateKey=https/key.pem:certKey=https/cert.pem main.asgi:application


### Ubuntu
sudo docker run --rm -p 6378:6379 -d redis:7
# sudo docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

#daphne -e ssl:8000:privateKey=certs/key.pem:certKey=certs/cert.pem main.asgi:application
daphne -b 0.0.0.0 -p 8000 root.asgi:application
