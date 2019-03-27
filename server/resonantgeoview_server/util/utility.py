from girder.models.folder import Folder
from girder.exceptions import AccessException


def findNamedFolder(currentUser, user, parent, parentType, name, create=False, public=False):
    folders = \
        [Folder().filter(folder, currentUser) for folder in
         Folder().childFolders(
            parent=parent, parentType=parentType,
            user=currentUser, filters={'name': name})]
    # folders should have len of 0 or 1, since we are looking in a
    # user folder for a folder with a certain name
    if len(folders) == 0:
        if create and currentUser:
            Folder().createFolder(
                parent, name, parentType=parentType, public=public,
                creator=currentUser)
            # newly created folder object miss _modelType property
            # better to get it again
            return findNamedFolder(currentUser, user, parent, parentType, name, create, public)
        else:
            return None
    else:
        return folders[0]

def findUserDatasetFolder(user):
    minervaFolder = findNamedFolder(user, user, user, 'user',
                           'resonantgeoview',True)

    return findNamedFolder(user, user, minervaFolder, 'folder',
                           'datasets',True)

def findSharedDatasetFolders(currentUser):
    folderModel = Folder()
    groupModel = ModelImporter.model('group')
    datasetSharingGroup = groupModel.findOne(query={
        'name': PluginSettings.DATASET_SHARING_GROUP_NAME
    })
    if not datasetSharingGroup:
        raise AccessException('user group "{0}" doesn\'t exist'.format(
            PluginSettings.DATASET_SHARING_GROUP_NAME))
    if datasetSharingGroup['_id'] not in currentUser['groups']:
        raise AccessException('user doesn\'t belong to user group "{0}"'.format(
            PluginSettings.DATASET_SHARING_GROUP_NAME))

    folders = folderModel.find({
        'baseParentType': 'user',
        'parentCollection': 'user',
        'access.groups.id': datasetSharingGroup['_id'],
        'name': PluginSettings.MINERVA_SHARED_DATASET
    })
    return folders


def findSourceFolder(currentUser, user, create=False):
    minervaFolder = findMinervaFolder(currentUser, user, create)
    if minervaFolder is None:
        return minervaFolder
    else:
        return findNamedFolder(currentUser, user, minervaFolder, 'folder',
                               PluginSettings.SOURCE_FOLDER, create)


def findSessionFolder(currentUser, user, create=False):
    minervaFolder = findMinervaFolder(currentUser, user, create)
    if minervaFolder is None:
        return minervaFolder
    else:
        return findNamedFolder(currentUser, user, minervaFolder, 'folder',
                               PluginSettings.SESSION_FOLDER, create)


def findNamedCollection(currentUser, name, create=False):
    collections = \
        [ModelImporter.model('collection').filter(c, currentUser) for c in
         ModelImporter.model('collection').textSearch(name, user=currentUser)]
    # collections should have len of 0 or 1, since we are looking
    # for a collection with a certain name
    if len(collections) == 0:
        if create:
            return ModelImporter.model('collection').createCollection(
                name, description='', public=True, creator=currentUser)
        else:
            return None
    else:
        return collections[0]


def findMinervaCollection(currentUser, create=False):
    return findNamedCollection(currentUser, PluginSettings.MINERVA_COLLECTION,
                               create)


def findAnalysisFolder(currentUser, create=False):
    minervaCollection = findMinervaCollection(currentUser,  create)
    if minervaCollection is None:
        return None
    else:
        analysisFolder = findNamedFolder(currentUser, currentUser,
                                         minervaCollection, 'collection',
                                         'analysis', create, public=True)
        return analysisFolder


def findAnalysisByName(currentUser, name):
    analysisFolder = findAnalysisFolder(currentUser)
    filters = {}
    filters['$text'] = {
        '$search': name
    }
    analyses = [ModelImporter.model('item').filter(item, currentUser)
                for item in
                Folder().childItems(folder=analysisFolder,
                                                         filters=filters)]
    if len(analyses) > 0:
        return analyses[0]
    else:
        return None