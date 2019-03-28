from geometa.exceptions import CannotHandleError

from .schema import OBJSchema


def handler(path, girder_file):
    if not girder_file['name'].endswith('.obj') and \
            not girder_file['name'].endswith('.OBJ'):
        raise CannotHandleError(girder_file['name'] + ' is not an OBJ file')

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
        'driver': 'OBJ'
    }
    schema = OBJSchema()
    return schema.load(geometa)
