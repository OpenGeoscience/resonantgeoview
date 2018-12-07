import base64
import globus_sdk
import json
import posixpath
import requests

from girder.api import access, rest
from girder.api.describe import autoDescribeRoute, Description
from girder.constants import AccessType
from girder.api.rest import Resource
from girder.models.item import Item
from girder.models.upload import Upload
from girder.utility.progress import setResponseTimeLimit

from ..util.utility import findUserDatasetFolder

def _globusTc(user):
    authorizer = globus_sdk.AccessTokenAuthorizer(user['globusTransferToken'])
    return globus_sdk.TransferClient(authorizer=authorizer)

def _item(info, f):
    path = posixpath.join(info['path'], f['name'])
    info = json.dumps({
        'id': info['id'],
        'path': path,
        'size': f['size'],
    })
    return {
        '_id': 'globus:' + base64.b64encode(info),
        '_modelType': 'item',
        '_accessLevel': AccessType.READ,
        'name': f['name'],
        'size': f['size'],
        'globusFile': True,
        'globusPath': path,
        'geometa': {
            "bounds": {
                "coordinates": [
                [
                    [
                    -0.703125,
                    -90.0
                    ],
                    [
                    -0.703125,
                    90.0
                    ],
                    [
                    180.0,
                    90.0
                    ],
                    [
                    180.0,
                    -90.0
                    ],
                    [
                    -0.703125,
                    -90.0
                    ]
                ]
                ],
                "type": "Polygon"
            },
            "crs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs ",
            "driver": "Network Common Data Format",
            "nativeBounds": {
                "bottom": -90.703125,
                "left": -0.703125,
                "right": 359.296875,
                "top": 6000.0
            },
            "subDatasets": [
                {
                "affine": [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0
                ],
                "bounds": {
                    "coordinates": [
                    [
                        [
                        0.0,
                        90.0
                        ],
                        [
                        0.0,
                        0.0
                        ],
                        [
                        2.0,
                        0.0
                        ],
                        [
                        2.0,
                        90.0
                        ],
                        [
                        0.0,
                        90.0
                        ]
                    ]
                    ],
                    "type": "Polygon"
                },
                "crs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs ",
                "driver": "Network Common Data Format",
                "height": 129,
                "name": "NETCDF:\"/home/matthew/assetstore-globus/9c/a8/9ca8a7a7cea297e6a3ff8b7086d9f752db20c4223cbd08b9c501110595fb31253d14db1a8fdec592d12a31c05297f271dc720e78480a5dc4766c6320403e7673\":lat_bnds",
                "nativeBounds": {
                    "bottom": 129.0,
                    "left": 0.0,
                    "right": 2.0,
                    "top": 0.0
                },
                "type_": "grid",
                "width": 2
                }
            ],
            "type_": "grid"
        }
    }


class GlobusResource(Resource):

    def __init__(self):
        super(GlobusResource, self).__init__()

        self.resourceName = 'globus'
        self.route('GET', (), self.getAll)
        self.route('GET', ('prepare',), self.prepare)

    @autoDescribeRoute(
        Description('')
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def getAll(self, params):
        user = self.getCurrentUser()

        if 'globusTransferToken' not in user:
            return []

        info = {"path": "~/Girder", "id": "dabdceba-6d04-11e5-ba46-22000b92c6ec"}
        itr = _globusTc(user).operation_ls(info['id'], path=info['path'])
        items = [_item(info, f) for f in itr if f['type'] == 'file']
        items = [item for item in items if item['name'] not in (
            'RELHUM_000101_050012.nc',
            'T_000101_050012.nc',
            'U_000101_050012.nc',
            'V_000101_050012.nc',
            'Z3_000101_050012.nc',
            'PRECC_000101_050012.nc'
        )]
        return items


    @autoDescribeRoute(
        Description('')
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def prepare(self, params):
        user = self.getCurrentUser()
        info = json.loads(base64.b64decode(params['id'][7:]))
        path = info['path'][2:]  # TODO this strips the leading '~/', might need to be more robust
        datasetFolder = findUserDatasetFolder(user)
        name = posixpath.basename(info['path'])

        item = Item().findOne({
            "folderId": datasetFolder["_id"],
            "name": name
        })
        if item:
            return item
        else:
            r = requests.get(
            'https://%s.e.globus.org/%s' % (info['id'], path), stream=True, headers={
                'Authorization': 'Bearer ' + self.getCurrentUser()['globusDownloadToken']
            })
            try:
                r.raise_for_status()
            except requests.RequestException:
                raise RestException(
                    'Invalid response from Globus HTTPS download service (%s).' % r.status_code, code=502)

            size = int(r.headers.get('Content-Length', info['size']))

            setResponseTimeLimit(duration=1800)

            file = Upload().uploadFromFile(r.raw, size, name, parentType='folder', parent=findUserDatasetFolder(user),
                        user=user, mimeType='application/octet-stream')
            return Item().findOne({
                "_id": file["itemId"]
            })
