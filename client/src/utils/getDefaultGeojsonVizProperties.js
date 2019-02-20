function getDefaultGeojsonVizProperties() {
  return {
    point: {
      radius: 8,
      strokeOpacity: 1,
      strokeProperty: null,
      stroke: true,
      fill: true,
      fillScale: null,
      fillColor: "#BEE37B",
      fillMinClamp: null,
      fillMaxClamp: null,
      strokeWidth: 2,
      fillPalette: null,
      fillOpacity: 0.75,
      strokeColor: "#999999",
      fillProperty: null,
      strokePalette: null
    },
    line: {
      strokeOpacity: 1,
      strokeProperty: null,
      stroke: true,
      strokeWidth: 2,
      strokeColor: "#999999",
      strokePalette: null
    },
    polygon: {
      strokeOpacity: 1,
      strokeProperty: null,
      stroke: true,
      fill: true,
      fillScale: null,
      fillColor: "#BEE37B",
      fillMinClamp: null,
      fillMaxClamp: null,
      strokeWidth: 1,
      fillPalette: null,
      fillOpacity: 0.75,
      strokeColor: "#999999",
      fillProperty: null,
      strokePalette: null
    }
  };
}

export { getDefaultGeojsonVizProperties };
