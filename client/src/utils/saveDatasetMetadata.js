import girder from "../girder";

const saveDatasetMetadata = async dataset => {
  var { data: newDataset } = await girder.rest.put(
    `item/${dataset._id}/metadata`,
    dataset.meta
  );
  return newDataset;
};

export default saveDatasetMetadata;
