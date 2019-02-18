#!/bin/bash
docker run --name test-postgres -p 5432:5432 -d postgres
docker run -it --rm --link test-postgres:postgres postgres psql -h postgres -U postgres -c "create database test" 
coverage run -m pytest
coverage html
docker stop test-postgres
docker rm test-postgres