from girder.api import access
from girder.api.describe import autoDescribeRoute, Description
from girder.api.rest import Resource
from girder.constants import AccessType
from girder.models.item import Item
from girder.models.folder import Folder
from girder_worker_utils.transforms.girder_io import GirderFileId
from girder_worker_utils.transforms.girder_io import GirderUploadToItem
from gaia_task.tasks import crop_task


class ProcessingResource(Resource):
    def __init__(self):
        super(ProcessingResource, self).__init__()

        self.route('GET', ('crop', ), self.crop_task)

    @access.public
    @autoDescribeRoute(
        Description('Clip a raster with a json geometry')
        .modelParam('itemId', 'The ID of the item that has a geojson file',
                    model=Item, level=AccessType.READ, destName='item', paramType='query')
        .modelParam('byitemId', 'The ID of the item that has a geojson file',
                    model=Item, level=AccessType.READ, destName='by_item', paramType='query')
        .param('name', 'Name of the item', paramType='query')
        .modelParam('folderId', 'Output folder id for the result item',
                    paramType='query', destName='folder', model=Folder, level=AccessType.READ)
    )
    def crop_task(self, item, by_item, name, folder):
        target_file = [i for i in Item().childFiles(item, limit=1)][0]
        by_file = [i for i in Item().childFiles(by_item, limit=1)][0]
        output = Item().createItem(name,
                                   creator=self.getCurrentUser(),
                                   folder=folder)
        result = crop_task.delay(GirderFileId(str(target_file['_id'])),
                                 GirderFileId(str(by_file['_id'])),
                                 name,
                                 girder_result_hooks=[
                                     GirderUploadToItem(str(output['_id']))
        ])
        return result.job
