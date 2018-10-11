#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from girder import events
from girder.models.item import Item

from rest import dataset, datasetGroup
from .client_webroot import ClientWebroot

def load(info):

    # Relocate Girder
    info['serverRoot'], info['serverRoot'].girder = (ClientWebroot(),
                                                     info['serverRoot'])
    # Relocate Girder API
    info['serverRoot'].api = info['serverRoot'].girder.api

    # Add API routes
    info['apiRoot'].dataset = dataset.DatasetResource()
    info['apiRoot'].dataset_group = datasetGroup.DatasetGroupResource()
