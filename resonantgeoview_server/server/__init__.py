import json

from girder import events, plugin
from girder.models.item import Item

from .rest import dataset, datasetGroup
from .rest.gaia.processing import ProcessingResource
from .client_webroot import ClientWebroot

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'resonantgeoview server'

    def load(self, info):
        # Relocate Girder
        info['serverRoot'], info['serverRoot'].girder = (ClientWebroot(),
                                                        info['serverRoot'])
        # Relocate Girder API
        info['serverRoot'].api = info['serverRoot'].girder.api

        # Add API routes
        info['apiRoot'].dataset = dataset.DatasetResource()
        info['apiRoot'].dataset_group = datasetGroup.DatasetGroupResource()

        # Add gaia processing
        info['apiRoot'].gaia = ProcessingResource()