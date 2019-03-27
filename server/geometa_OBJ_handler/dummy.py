from geometa.exceptions import CannotHandleError

from .schema import OBJSchema


def handler(path, girder_file):
    print('dummy')
    if '.obj' not in girder_file['name'] and \
            '.OBJ' not in girder_file['name']:
        raise CannotHandleError(girder_file['name'] + ' is not an OBJ file')
    else:
        print("dummy 2")
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
