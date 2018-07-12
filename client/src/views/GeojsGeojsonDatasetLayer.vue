<template>
<GeojsGeojsonLayer
  v-if="geojson"
  :geojson="geojson"
  :zIndex="zIndex"
  :opacity="opacity">
</GeojsGeojsonLayer>
</template>

<script>
import girder from "../girder";
import loadDatasetData from "../utils/loadDatasetData";

var cache = new WeakMap();

export default {
  name: "GeojsGeojsonDatasetLayer",
  components: {},
  props: ["dataset", "zIndex", "opacity"],
  data() {
    return {
      geojson: null
    };
  },
  computed: {
    actions() {
      return [];
    }
  },
  watch: {
    // dataset
  },
  async created() {
    if (cache.has(this.dataset)) {
      this.geojson = cache.get(this.dataset);
    } else {
      var geojson = await loadDatasetData(this.dataset);
      cache.set(this.dataset, geojson);
      this.geojson = geojson;
    }
  },
  methods: {}
};
</script>
