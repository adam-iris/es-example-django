#!/bin/bash

###
# Docker effectively runs "ENTRYPOINT CMD" so this script runs with a
# command as its arguments. (Why? I don't know.)
# So this script can run all the things that should precede the "main" command

python manage.py migrate;
# python manage.py collectstatic --noinput;

# Run the command
exec "$@";