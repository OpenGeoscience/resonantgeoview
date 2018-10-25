<script>
import geo from "geojs";
import { stringify } from "qs";

export default {
  name: "WMSLayer",
  props: ["dataset", "zIndex", "opacity"],
  data() {
    var geometa = this.dataset.geometa;
    var url = geometa.url;
    var layer = geometa.layer;
    var projection = "EPSG:3857";
    return {
      url(x, y, zoom) {
        var bb = this.gcsTileBounds({ x: x, y: y, level: zoom }, projection);
        var bbox_mercator =
          bb.left + "," + bb.bottom + "," + bb.right + "," + bb.top;

        var params = {
          SERVICE: "WMS",
          VERSION: "1.3.0",
          REQUEST: "GetMap",
          LAYERS: layer,
          STYLES: "",
          BBOX: bbox_mercator,
          WIDTH: 256,
          HEIGHT: 256,
          FORMAT: "image/png",
          TRANSPARENT: true,
          CRS: projection,
          TILED: true
        };
        return url.replace("?", "") + "?" + stringify(params);
      }
    };
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

<template>
  <GeojsTileLayer
    :url="url"
    :opacity="opacity"
    :zIndex="zIndex"
    :keepLower="false"
    ref="geojsTileLayer">
  </GeojsTileLayer>
</template>
