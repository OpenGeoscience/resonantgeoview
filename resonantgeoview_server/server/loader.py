#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from girder import events
from girder.models.item import Item

from rest import dataset, datasetGroup

def load(info):

    # Relocate Girder API
    info['serverRoot'].girder = info['serverRoot']
    info['serverRoot'].api = info['serverRoot'].girder.api

    # Add API routes
    info['apiRoot'].dataset = dataset.DatasetResource()
    info['apiRoot'].dataset_group = datasetGroup.DatasetGroupResource()
