#!/bin/bash

source .env

docker exec -it adrianolczak-db-1 psql -h localhost -U $POSTGRES_USER -d $POSTGRES_DB
