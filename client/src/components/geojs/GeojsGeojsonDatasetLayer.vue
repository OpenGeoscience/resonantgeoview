<template>
  <GeojsGeojsonLayer
    :geojson="geojson"
    :zIndex="zIndex"
    :opacity="opacity"
    :featureStyle="style"
    ref="geojsGeojsonLayer"
  >
  </GeojsGeojsonLayer>
</template>

<script>
import geo from "geojs";
import * as d3 from "d3";
import isObject from "lodash-es/isObject";

export default {
  name: "GeojsGeojsonDatasetLayer",
  components: {},
  props: ["dataset", "zIndex", "opacity", "summary", "geojson"],
  data() {
    return {};
  },
  computed: {
    style() {
      var vizProperties = this.dataset.meta.vizProperties;
      var style = {
        point: { radius: vizProperties.point.radius },
        line: {},
        polygon: { uniformPolygon: true }
      };
      style.point = {
        ...style.point,
        ...this.translate("stroke", vizProperties.point)
      };
      style.point = {
        ...style.point,
        ...this.translate("fill", vizProperties.point)
      };
      style.line = {
        ...style.line,
        ...this.translate("stroke", vizProperties.line)
      };
      style.polygon = {
        ...style.polygon,
        ...this.translate("stroke", vizProperties.polygon)
      };
      style.polygon = {
        ...style.polygon,
        ...this.translate("fill", vizProperties.polygon)
      };
      return style;
    }
  },
  mounted() {
    if (this.$listeners.click) {
      this.$refs.geojsGeojsonLayer.$features.forEach(feature => {
        feature.selectionAPI(true);
        feature.geoOn(geo.event.feature.mouseclick, e => {
          this.$emit("click", {
            geo: [e.mouse.geo],
            data: e.data
          });
        });
      });
      this.$refs.geojsGeojsonLayer.$geojsLayer.geoOn(
        geo.event.mouseclick,
        e => {
          this.$emit("click", {
            geo: e.geo
          });
        }
      );
    }
  },
  methods: {
    translate(prefix, styles) {
      var subStyle = {
        [prefix + "Opacity"]: styles[prefix + "Opacity"],
        [prefix]: styles[prefix],
        [prefix + "Color"]: styles[prefix + "Color"]
      };
      if (styles[prefix + "Property"] && styles[prefix + "Palette"]) {
        subStyle[prefix + "Color"] = this.getColorScaleFunc(
          styles[prefix + "Property"],
          styles[prefix + "Palette"],
          this.summary.properties[styles[prefix + "Property"]],
          styles[prefix + "Scale"],
          styles[prefix + "MinClamp"],
          styles[prefix + "MaxClamp"]
        );
      }
      if (prefix === "stroke") {
        subStyle["strokeWidth"] = styles["strokeWidth"];
      }
      return subStyle;
    },
    getColorScaleFunc(
      property,
      palette,
      propertySummary,
      scale,
      minClamp,
      maxClamp
    ) {
      var scaleFunc = null;
      if (isObject(propertySummary.values)) {
        // categorical

        scaleFunc = d3.scale
          .ordinal()
          .domain(Object.keys(propertySummary.values))
          .range(palette);
      } else {
        // continuous
        // handle the case when all values are the same
        let max = propertySummary.max,
          min = propertySummary.min;
        if (min >= max) {
          max = min + 1;
        }
        if (scale === "log" && min > 0) {
          let s = d3.scale
            .quantize()
            .domain([Math.log(min), Math.log(max)])
            .range(palette);
          scaleFunc = value => {
            return s(Math.log(value));
          };
        } else if (scale === "quantile") {
          let data = [];
          this.geojson.features.forEach(function(feature) {
            data.push(feature.properties[property]);
          });
          scaleFunc = d3.scale
            .quantile()
            .domain(data)
            .range(palette);
        } else {
          // linear scaling
          scaleFunc = d3.scale
            .quantize()
            .domain([minClamp ? minClamp : min, maxClamp ? maxClamp : max])
            .range(palette);
        }
      }
      return (...args) => {
        if (args[2]) {
          return scaleFunc(args[2].properties[property]);
        } else {
          // geojs callback for point has different arguments
          return scaleFunc(args[0].properties[property]);
        }
      };
    }
  }
};
</script>
