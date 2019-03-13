FROM node:10.15.3-stretch

EXPOSE 8080

RUN apt-get update && apt-get install -qy \
    gcc \
    libpython3-dev \
    git \
    libsasl2-dev && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

# See http://click.pocoo.org/5/python3/#python-3-surrogate-handling for more detail on
# why this is necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# above is largely duplicated from https://github.com/girder/girder/blob/master/Dockerfile.py3

ENV C_FORCE_ROOT=1

# Install girder
RUN mkdir /resonantgeoview
COPY submodules /resonantgeoview/submodules

RUN pip install -r /resonantgeoview/submodules/gaia/requirements.txt -f https://manthey.github.io/large_image_wheels

RUN pip install -e /resonantgeoview/submodules/gaia

COPY gaia_tasks /resonantgeoview/gaia_tasks
RUN pip install -e /resonantgeoview/gaia_tasks

COPY devops/docker/worker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]
