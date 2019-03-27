#!/usr/bin/env python
# -*- coding: utf-8 -*-
from girder.api import access
from girder.api.describe import autoDescribeRoute, Description
from girder.constants import AccessType
from girder.api.rest import Resource
from ..models.datasetGroup import DatasetGroup


class DatasetGroupResource(Resource):

    def __init__(self):
        super(DatasetGroupResource, self).__init__()

        self.resourceName = 'dataset_group'
        self.route('GET', (), self.getAll)
        self.route('GET', (':id',), self.get)
        self.route('POST', (), self.create)
        self.route('PUT', (':id',), self.edit)
        self.route('DELETE', (':id',), self.delete)

    @autoDescribeRoute(
        Description('')
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def getAll(self, params):
        cursor = DatasetGroup().find({})
        return list(DatasetGroup().filterResultsByPermission(
            cursor, self.getCurrentUser(), AccessType.READ, 0, 0))

    @autoDescribeRoute(
        Description('')
        .modelParam('id', model=DatasetGroup, destName='datasetGroup', level=AccessType.READ)
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def get(self, datasetGroup, params):
        return datasetGroup

    @autoDescribeRoute(
        Description('')
        .jsonParam('data', '', requireObject=True, paramType='body')
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def create(self, data, params):
        return DatasetGroup().create(data, user=self.getCurrentUser())

    @autoDescribeRoute(
        Description('')
        .modelParam('id', model=DatasetGroup, destName='datasetGroup', level=AccessType.WRITE)
        .jsonParam('data', '', requireObject=True, paramType='body')
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def edit(self, datasetGroup, data, params):
        data.pop('_id', None)
        datasetGroup.update(data)
        return DatasetGroup().save(datasetGroup)

    @autoDescribeRoute(
        Description('')
        .modelParam('id', model=DatasetGroup, destName='datasetGroup', level=AccessType.WRITE)
        .errorResponse()
        .errorResponse('Read access was denied on the item.', 403)
    )
    @access.user
    def delete(self, datasetGroup, params):
        DatasetGroup().remove(datasetGroup)
        return
