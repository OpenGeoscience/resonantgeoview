<template>
  <GeojsTileLayer
    :url="styledURL"
    :opacity="opacity"
    :keepLower="keepLower"
    :zIndex="zIndex"
    ref="geojsTileLayer"
  >
  </GeojsTileLayer>
</template>

<script>
import geo from "geojs";

export default {
  name: "StyledGeoTIFFLayer",
  components: {},
  props: ["dataset", "zIndex", "opacity", "tileURL", "keepLower"],
  computed: {
    styledURL() {
      var vizProperties = this.dataset.meta.vizProperties;
      if (!vizProperties) {
        return this.tileURL;
      } else {
        var style = encodeURIComponent(
          JSON.stringify({
            band: parseInt(vizProperties.band),
            palette: vizProperties.palette,
            scheme: vizProperties.type,
            min: vizProperties.range[0],
            max: vizProperties.range[1]
          })
        );
        return this.tileURL + `&style=${style}`;
      }
    }
  },
  mounted() {
    if (this.$listeners.click) {
      this.$refs.geojsTileLayer.$geojsLayer.selectionAPI(true);
      this.$refs.geojsTileLayer.$geojsLayer.geoOn(geo.event.mouseclick, e => {
        this.$emit("click", {
          geo: e.geo
        });
      });
    }
  }
};
</script>

<style></style>
