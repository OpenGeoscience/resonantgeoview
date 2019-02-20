export default function(dataset) {
  if (dataset.geometa.driver) {
    return dataset.geometa.driver;
  }
  if (dataset.geometa.subDatasets) {
    for (let subDataset of dataset.geometa.subDatasets) {
      if (subDataset.driver) {
        return subDataset.driver;
      }
    }
  }
}
