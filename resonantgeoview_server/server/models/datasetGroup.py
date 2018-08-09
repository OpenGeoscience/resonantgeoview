from girder.models.model_base import Model


class DatasetGroup(Model):

    def initialize(self):
        self.name = 'datasetGroup'

    def validate(self, model):
        return model
