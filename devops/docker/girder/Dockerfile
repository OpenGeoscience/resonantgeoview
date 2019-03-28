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

# Install girder
RUN mkdir /resonantgeoview
COPY submodules /resonantgeoview/submodules

# Needed by geometa
RUN pip install rasterio osr
# Install geometa
RUN pip install -e /resonantgeoview/submodules/girder_geospatial \
    /resonantgeoview/submodules/girder_geospatial/types/vector \
    /resonantgeoview/submodules/girder_geospatial/types/raster \
    /resonantgeoview/submodules/girder_geospatial/types/grid

RUN pip install libtiff openslide_python pyvips gdal mapnik large-image[sources]==1.0.0.dev21 -f https://manthey.github.io/large_image_wheels

COPY gaia_tasks /resonantgeoview/gaia_tasks
RUN pip install -e /resonantgeoview/gaia_tasks
COPY server /resonantgeoview/server
RUN pip install -e /resonantgeoview/server
RUN girder build --static-root /static

# Install resonantgeoview
COPY client /resonantgeoview/client
WORKDIR /resonantgeoview/client
RUN npm install \
    && npm run build \
    && mv dist /usr/share/girder/static/resonantgeoview

ENTRYPOINT ["girder", "serve"]
