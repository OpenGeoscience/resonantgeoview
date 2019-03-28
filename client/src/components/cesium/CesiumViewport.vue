<script>
// Cesium.Ion.defaultAccessToken = process.env.VUE_APP_CESIUM_API_KEY;

export default {
  name: "CesiumViewport",
  props: {
    layers: {
      type: Array,
      default: () => []
    }
  },
  data: () => ({
    $viewer: null,
    ready: false
  }),
  provide() {
    const provided = {};
    Object.defineProperty(provided, "$viewer", {
      get: () => this.$viewer
    });
    return provided;
  },
  watch: {
    layers() {}
  },
  created() {},
  mounted() {
    var viewer = new Cesium.Viewer(this.$refs.container, {
      timeline: false,
      infoBox: false,
      fullscreenButton: false,
      animation: false,
      navigationHelpButton: false,
      geocoder: false,
      homeButton: false,
      baseLayerPicker: false,
      imageryProvider: Cesium.createOpenStreetMapImageryProvider()
    });
    this.$viewer = viewer;
    this.ready = true;
  },
  methods: {}
};
</script>

<template>
  <div class="viewport" ref="container">
    <slot v-if="ready" />
  </div>
</template>

<style lang="scss" scoped>
.viewport {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
