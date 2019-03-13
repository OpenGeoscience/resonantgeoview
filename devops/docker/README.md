# Docker deployment

Deploy ResonantGeoView system with Docker.

## Prerequisite
* Docker 18.03+

## Build
* At current directory
* Make a copy of .env.template file and rename it to .env file
* Populate and update .env (*GIRDER_ADMIN_PASS* needs to be at least 6 characters long)
* `docker-compose build`
* `docker-compose up` should finish without error with **provision exited with code 0**
* By default, ResonantGeoView should be available at http://localhost:8080
