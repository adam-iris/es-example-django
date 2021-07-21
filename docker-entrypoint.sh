#!/bin/bash

###
# Docker effectively runs 
#  $ENTRYPOINT $CMD
# so the command is passed as all the arguments
# to this entrypoint. (Why? I don't know.)
# Use this to run any prerequisites.

# Django migrations
python manage.py migrate;

# We currently build static files into the image
# python manage.py collectstatic --noinput;

# Run the command
exec "$@";