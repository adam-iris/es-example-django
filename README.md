# es-example-django

An example Django system for use with the [es-simple-cluster](https://github.com/EarthScope/es-simple-cluster/) system.

See the [docs](docs) area for user documentation.

## Installation

This should be included (but may be commented out) in the [es-simple-cluster](https://github.com/EarthScope/es-simple-cluster/) project.

### By hub image

This project uses [GitHub Actions](https://github.com/EarthScope/es-example-django/actions/workflows/docker-publish.yml) to build and deploy the latest version as a Docker image to ghcr.io.

Update (or add) services in the `docker-compose.yml` to use this image:

    example-web:
        image: ghcr.io/earthscope/es-example-django:main

### Source code

From the [es-simple-cluster](https://github.com/EarthScope/es-simple-cluster/) root, clone this project.

    git clone https://github.com/EarthScope/es-example-django

Update (or add) services in the `docker-compose.yml` to use the local path:

    example-web:
        build: es-example-django

## Components

This image can perform a variety of different functions, which typically would go into separate containers.

### Web Interface

This implements a simple round-trip:

### WebSocket Interface

This actually runs on the same channel as the web interface, but implements a persistent two-way communications channel.

There is a websocket demo in the main [es-simple-cluster](https://github.com/EarthScope/es-simple-cluster/) project, which by default connects to this interface:

### Consumer

This image can also run a script that implements an archiver -- it reads from the Kafka topic that the front-end feeds, and puts data into the database.