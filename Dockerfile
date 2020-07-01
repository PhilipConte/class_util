FROM python:slim

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    build-essential

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

EXPOSE 8000

ADD ./entrypoint.sh /
RUN chmod 755 /entrypoint.sh
CMD ["/entrypoint.sh"]
