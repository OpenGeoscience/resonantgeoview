<template>
  <GeojsColorLegendWidget
    :zIndex='100'
    :categories='categories'
    />
</template>

<script>
import range from "lodash-es/range";

export default {
  name: "AdaptedColorLegendLayer",
  props: {
    layers: {
      required: true
    },
    datasetIdMetaMap: {
      required: true
    }
  },
  computed: {
    categories() {
      var datasets = this.layers
        .filter(layer => layer.opacity)
        .map(layer => layer.dataset);
      var categories = [];
      for (let dataset of datasets) {
        switch (dataset.geometa.driver) {
          case "GeoJSON":
            categories = [
              ...categories,
              ...generateCategoryForGeoJSON(
                dataset,
                this.datasetIdMetaMap[dataset._id].geojson,
                this.datasetIdMetaMap[dataset._id].summary
              )
            ];
            break;
          case "GeoTIFF":
            categories = [
              ...categories,
              ...generateCategoryForGeoTIFF(dataset)
            ];
            break;
        }
      }
      return categories;
    }
  }
};

function generateCategoryForGeoJSON(dataset, data, summary) {
  var categories = [];

  let vizProperties = dataset.meta.vizProperties;

  processOneCategory("polygon", "fillProperty", "fillPalette");
  processOneCategory("polygon", "strokeProperty", "strokePalette");
  processOneCategory("line", "strokeProperty", "strokePalette");
  processOneCategory("point", "strokeProperty", "strokePalette");

  function processOneCategory(type, property, paletteKey) {
    var viz = vizProperties[type];
    if (!viz || !viz[property]) {
      return;
    }
    var colors = viz[paletteKey];
    // Default category configuration
    var category = {
      name: dataset.name + " - " + vizProperties.polygon[property],
      type: "discrete",
      scale: "linear",
      colors: colors,
      domain: [
        summary.properties[viz[property]].min,
        summary.properties[viz[property]].max
      ]
    };
    // categorical
    if (summary.properties[viz[property]].values) {
      var domain = Object.keys(summary.properties[viz[property]].values);
      // Too few or too many to fit the size
      if (domain.length === 1 || domain.length > 7) {
        return;
      } else {
        category.scale = "ordinal";
        category.domain = domain;
      }
    }
    // current UI styling is designed that the log, quantile, clamping option is only applicable to fill. so, when it's a stroke, skip the following options.
    if (property === "fillProperty") {
      switch (viz.fillScale) {
        case "log":
          category.scale = "log";
          break;
        case "quantile":
          category.scale = "quantile";
          category.domain = data.features.map(function(feature, index, array) {
            return feature.properties[viz[property]];
          });
          break;
      }
      // Not implemented at this moment
      // if (viz.clampingFlag) {
      //   category.scale = "linear";
      //   category.clamp = [viz.minClamp, viz.maxClamp];
      // }
    }
    categories.push(category);
  }

  return categories;
}

function generateCategoryForGeoTIFF(dataset) {
  if (
    !dataset.meta ||
    !dataset.meta.vizProperties ||
    !dataset.meta.vizProperties.palette
  ) {
    return [];
  }
  let vizProperties = dataset.meta.vizProperties;

  var category = {
    name: `${dataset.name} - band ${vizProperties.band}`,
    type: vizProperties.type === "discrete" ? "discrete" : "continuous",
    scale: "linear",
    colors: vizProperties.palette,
    domain: [vizProperties.range[0], vizProperties.range[1]]
  };
  if (
    vizProperties.range[1] + 1 - vizProperties.range[0] ===
    vizProperties.palette.length
  ) {
    category.type = "discrete";
    category.scale = "ordinal";
    category.domain = range(vizProperties.range[0], vizProperties.range[1] + 1);
  }
  return [category];
}
</script>

<style lang="scss">
.color-legend-container {
  border: none !important;
  border-radius: 2px !important;
  box-shadow: 2px 2px 11px 2px #c7c7c7 !important;

  .legends .legend .title {
    text-align: center;
    font-size: inherit !important;
    line-height: inherit !important;
    letter-spacing: inherit !important;
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
