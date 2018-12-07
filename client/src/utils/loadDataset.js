import girder from '../girder';

export default async () => {
    return (await Promise.all([
        girder.rest.get('globus').then(({ data }) => data),
        girder.rest.get('dataset').then(({ data }) => data)
    ])).reduce((all, datasets) => ([...all, ...datasets]), []);
}

export const loadDatasetById = (ids) => {
    return Promise.all(ids.map(id => {
        return girder.rest.get(`dataset/${id}`)
            .then(({ data }) => data)
            .catch(() => null)
    })).then(datasets => {
        return datasets.filter(dataset => dataset)
    });
}
