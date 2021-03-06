import datetime
from girder.models.model_base import AccessControlledModel
from girder.constants import AccessType


class DatasetGroup(AccessControlledModel):

    def initialize(self):
        self.name = 'datasetGroup'

    def validate(self, model):
        return model

    def create(self, model, user=None):
        model['created'] = datetime.datetime.utcnow()

        return self.setUserAccess(model, user, level=AccessType.ADMIN, save=True)
