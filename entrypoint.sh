#!/bin/bash

cd /code

regex="^postgres:\/\/([^:]+)(:(.+))?@(.+)\/(.+)$"
if [[ $DATABASE_URL =~ $regex ]]
then
  db_user="${BASH_REMATCH[1]}"
  db_server="${BASH_REMATCH[4]}"
  db="${BASH_REMATCH[5]}"
else
  >&2 echo "DATABASE_URL is not valid"
  exit 1
fi

>&2 echo "waiting for postgres"
count=0
until ( pg_isready -h "${db_server}" -d "${db}" -U "${db_user}" ) do
  ((count++))
  if [ ${count} -gt 20 ]
  then
    >&2 echo "postgres unavailable"
    exit 1
  fi
  sleep 1
done
>&2 echo "postgres ready"

python manage.py migrate
python manage.py load_sections
python manage.py load_pathways

exec gunicorn class_util.wsgi:application \
 --name class_util \
 --bind 0.0.0.0:8000 \
 --workers 3 \
 --reload \
 "$@"
