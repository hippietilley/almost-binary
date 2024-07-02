# FROM python:3.11-alpine

# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

ARG PY_VERSION=3.11
### Intermediate build image(s) ###
FROM python:${PY_VERSION}-slim AS build-deps
# need ssh-keyscan(openssh-client) to add github to known_hosts and git to install our python packages
# if psycopg2 is in requirements and needs to be built, gcc, libpq-dev & python3-dev are required
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-client git gcc python3-dev libpq-dev
WORKDIR /code
COPY requirements.txt /code/
COPY . /code/
RUN mkdir /var/www
RUN mkdir /var/www/almostbinary
RUN mkdir /var/www/almostbinary/static
ENV STATIC_ROOT_DIR=/var/www/almostbinary/static/
RUN --mount=type=ssh,id=almostbinary python -m venv /code/env/ && \
    . /code/env/bin/activate && \
    pip install --upgrade pip && \
    pip install -r /code/requirements.txt && \
    python /code/almostbinary/manage.py collectstatic --noinput && \
    python /code/almostbinary/manage.py compress --force

# install dev python dependencies on top of build-deps
FROM build-deps AS build-dev-deps
COPY requirements_dev.txt /code/
RUN --mount=type=ssh,id=preteckt_dash . /code/env/bin/activate && \
    pip install -r /code/requirements_dev.txt

### Intermediate runtime image(s) ###
FROM python:${PY_VERSION}-slim AS runtime-deps
# libpq needed for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5
WORKDIR /code
ENV PYTHONPATH=/code \
    APPLICATION_PATH=/code
    #REDISSTRING=redis://redis:6379/0

### Release images ###
FROM runtime-deps AS release
# copy the virtual env from the build image
COPY --from=build-dev-deps /code/ /code/
COPY --from=build-dev-deps /var/www/almostbinary /var/www/almostbinary
#COPY --from=static-assets /code/ /code/
# copy the source code
COPY . /code/

# TODO: delete tests dirs
# integration test image
FROM runtime-deps as test
# copy the virtual env from the build image
COPY --from=build-dev-deps /code/ /code/
# copy the source code
COPY . /code/

# by default, build the prod image
# pass --target=test to build test image
#FROM static-assets as nginx
FROM release as latest
