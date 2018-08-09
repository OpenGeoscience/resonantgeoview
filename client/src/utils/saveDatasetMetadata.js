import girder from '../girder';

const saveDatasetMetadata = async (dataset) => {
    var { data: dataset } = await girder.rest.put(`item/${dataset._id}/metadata`, dataset.meta);
    return dataset;
}

export default saveDatasetMetadata;
