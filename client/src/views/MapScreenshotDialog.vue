<template>
<v-dialog :value="value" @input="$emit('input', $event)" max-width="650px">
  <v-card>
    <div class="image-container">
      <img :src="image" />
    </div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary">
        <a class="download-link" :href="image"
          download="screenshot.png">Download</a>
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
</template>

<script>
export default {
  name: "MapScreenshotDialog",
  props: {
    value: {
      type: Boolean,
      required: true
    },
    map: {}
  },
  data() {
    return {
      image: null
    };
  },
  computed: {},
  created() {},
  watch: {
    map(map) {
      if (map) {
        var layers = this.map.layers();
        map.screenshot({ layers }).then(image => {
          this.image = image;
        });
      }
    }
  },
  methods: {
    download() {}
  }
};
</script>

<style lang="scss" scoped>
.image-container {
  width: 100%;
  max-height: 70vh;
  overflow-y: auto;

  img {
    width: 100%;
  }
}

.download-link {
  color: inherit;
  text-decoration: none;
}
</style>
