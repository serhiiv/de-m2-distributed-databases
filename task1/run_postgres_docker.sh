#!/usr/bin/bash

docker run --name postgres \
  -p 5432:5432 \
  -h 127.0.0.1 \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=postgres \
  -v postgresdata:/var/lib/postgresql/data \
  -d postgres:14.15-alpine3.20  
