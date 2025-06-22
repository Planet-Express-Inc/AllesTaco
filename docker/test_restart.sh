#!/bin/bash
docker-compose -f docker-compose-test.yml down
docker-compose -f docker-compose-test.yml up -d
