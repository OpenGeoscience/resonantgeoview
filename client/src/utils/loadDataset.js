import girder from "../girder";

export default () => {
  return girder.rest.get("dataset").then(({ data }) => {
    return data;
  });
};

export const loadDatasetById = ids => {
  return Promise.all(
    ids.map(id => {
      return girder.rest
        .get(`dataset/${id}`)
        .then(({ data }) => data)
        .catch(() => null);
    })
  ).then(datasets => {
    return datasets.filter(dataset => dataset);
  });
};
