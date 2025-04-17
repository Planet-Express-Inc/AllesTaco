#!/bin/bash

echo TEST-Script Build Testing
docker-compose --file ./docker-compose.coverage.yml down
docker-compose --file ./docker-compose.coverage.yml build
docker-compose --file ./docker-compose.coverage.yml up -d

