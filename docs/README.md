# About this project

This is a vanilla Django project intended to be a testbed for components of the EarthScope cloud functionality.

# Applications

- [Kafka Example](kafka_example.md) implements an example "round-trip" data path through collection/archiving/distribution.
- [User](es_user.md) implements an example "round-trip" data path through collection/archiving/distribution.

## Components

- **Docker** : recipe for building the django image
- **www** : project definition
  - **www/settings.py** : main settings
  - **www/urls.py** : top-level routing table
- **requirements.txt** : python environment definition

Static files are expected to be in `/django-static`.

## Running the local server

Install the dependencies (preferably in a dedicated environment):

    pip install -r requirements.txt

Set up the database:

    python manage.py migrate

Run the dev server:

    python manage.py runserver 0.0.0.0:8000

## Running in a container

After making a code change, run (from the main project directory):

    docker compose up -d --build
