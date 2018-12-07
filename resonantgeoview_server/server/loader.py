#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from girder import events
from girder.models.item import Item
from girder.models.user import User
from girder.plugins.oauth.providers import Globus

from rest import dataset, datasetGroup,globus
from rest.gaia.processing import ProcessingResource
from .client_webroot import ClientWebroot


def _saveGlobusToken(event):
    # When a user logs in with globus, we save their token
    if event.info['provider'] == Globus:
        transferToken = None
        downloadToken = None
        for other in event.info['token']['other_tokens']:
            if other.get('resource_server') == 'transfer.api.globus.org':
                transferToken = other['access_token']
            if other.get('resource_server') == 'petrel_https_server':  # TODO hardcoded
                downloadToken = other['access_token']

        User().update({
            '_id': event.info['user']['_id']
        }, {
            '$set': {
                'globusTransferToken': transferToken,
                'globusDownloadToken': downloadToken
            }
        }, multi=False)

def load(info):

    # Relocate Girder
    info['serverRoot'], info['serverRoot'].girder = (ClientWebroot(),
                                                     info['serverRoot'])
    # Relocate Girder API
    info['serverRoot'].api = info['serverRoot'].girder.api

    # Add API routes
    info['apiRoot'].dataset = dataset.DatasetResource()
    info['apiRoot'].dataset_group = datasetGroup.DatasetGroupResource()
    info['apiRoot'].globus = globus.GlobusResource()

    # Add gaia processing
    info['apiRoot'].gaia = ProcessingResource()


    events.bind('oauth.auth_callback.after', 'globus', _saveGlobusToken)
