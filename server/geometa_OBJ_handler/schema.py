from marshmallow import fields
from bson.objectid import ObjectId
import json
import re
from pyproj import Proj

from geometa.schema import BaseSchema
from geometa.utils import from_bounds_to_geojson
from geometa.exceptions import CannotHandleError
from shapely.geometry import MultiPoint
from girder.models.file import File


class OBJSchema(BaseSchema):
    driver = fields.String(required=True)


def redOBJMeta(name):
    srs = None
    offset_x = None
    offset_y = None
    offset_z = None
    with open(name, 'r') as f:
        for line in f:
            if srs and offset_x and offset_y and offset_z:
                return srs, [offset_x, offset_y, offset_z]
            if line[0] != '#':
                continue
            if line.startswith('#x offset: '):
                offset_x = float(line.replace('#x offset: ', ''))
                continue
            if line.startswith('#y offset: '):
                offset_y = float(line.replace('#y offset: ', ''))
                continue
            if line.startswith('#z offset: '):
                offset_z = float(line.replace('#z offset: ', ''))
                continue
            if line.startswith('#srs: '):
                srs = line.replace('#srs: ', '')
                continue
    raise CannotHandleError('can\'t read srs, offset_x, offset_y, or offset_z from OBJ meta rows')


def readObjFileVertices(name):
    """
    Read the vertices from an OBJ file. Returns a generator that yields each (x,y,z) vertex.
    """
    with open(name, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('v '):
                line = line.strip()
                coords = line[2:].split(' ')
                if len(coords) != 3:
                    raise RuntimeError('Vertex definition must contain 3 floating point values')
                coords = [float(coord) for coord in coords]
                yield coords
                continue


def getOBJBounds(objFileName, offset):
    # Read vertices in OBJ file
    points = list(readObjFileVertices(objFileName))

    # Compute bounds
    multiPoint = MultiPoint(points)
    bounds = multiPoint.bounds

    # Apply offset to bounds
    return {
        "left": bounds[0] + offset[0],
        "bottom": bounds[1] + offset[1],
        "right": bounds[2] + offset[0],
        "top": bounds[3] + offset[1]
    }


def handler(path, girder_file):
    if ".obj" not in girder_file['name'] and \
            ".OBJ" not in girder_file['name']:
        raise CannotHandleError(girder_file['name'] + ' is not an OBJ file')
    srs, offset = redOBJMeta(path)
    try:
        bounds = getOBJBounds(path, offset)
        geoJsonBounds = from_bounds_to_geojson(bounds, srs)
        geometa = {
            'crs': srs,
            'nativeBounds': bounds,
            'bounds': geoJsonBounds,
            'type_': 'vector',
            'driver': 'OBJ'
        }
        schema = OBJSchema()
        return schema.load(geometa)
    except Exception:
        raise CannotHandleError('Failed to add geometa to OBJ file')
