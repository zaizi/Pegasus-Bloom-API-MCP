#!/bin/bash
#Compose down to wipe volumes and then up to build from scratch. Doing this as this will be modified constantly.
docker-compose down -v && docker-compose up --build -d