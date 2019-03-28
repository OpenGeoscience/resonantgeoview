from marshmallow import fields
import json

from geometa.exceptions import CannotHandleError
from geometa.schema import BaseSchema


class Tileset3DSchema(BaseSchema):
    driver = fields.String(required=True)


def handler(path, girder_file):
    if not girder_file['name'].endswith('.json'):
        raise CannotHandleError(girder_file['name'] + ' is not a json file')

    with open(path) as json_file:
        data = json.load(json_file)
        if ('asset' not in data) or ('root' not in data) or ('geometricError' not in data):
            raise CannotHandleError(girder_file['name'] + ' is not a tileset.json file')
        geometa = {
            'crs': '+proj=longlat +datum=WGS84 +no_defs',
            'nativeBounds': {
                'left': 0.0,
                'right': 0.01,
                'bottom': 0.0,
                'top': 0.01
            },
            'bounds': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [
                            0.0,
                            0.01
                        ],
                        [
                            0.01,
                            0.01
                        ],
                        [
                            0.01,
                            0.0
                        ],
                        [
                            0.0,
                            0.0
                        ]
                    ]
                ]
            },
            'type_': 'vector',
            'driver': 'Cesium'
        }
        schema = Tileset3DSchema()
        return schema.load(geometa)
