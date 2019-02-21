<script>
export default {
  name: "AddCesiumTilesetDialog",
  components: {},
  props: {
    value: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      name: "",
      assetId: ""
    };
  },
  computed: {},
  watch: {},
  created() {},
  methods: {
    emitCesiumDataset() {
      this.$emit("dataset", {
        name: this.name,
        geometa: {
          crs: "+proj=longlat +datum=WGS84 +no_defs ",
          driver: "Cesium",
          type_: "raster",
          assetId: this.assetId,
          bounds: {
            type: "Polygon",
            coordinates: [
              [[-180, -90], [-180, 90], [180, 90], [180, -90], [-180, -90]]
            ]
          },
          nativeBounds: {
            top: 90,
            right: 180,
            bottom: -90,
            left: -180
          }
        }
      });
      this.close();
    },
    close() {
      this.name = "";
      this.assetId = "";
      this.$emit("input", false);
    }
  }
};
</script>

<template>
  <v-dialog
    :value="value"
    @input="$emit('input', $event)"
    scrollable
    max-width="450px"
    persistent
    lazy
  >
    <v-card>
      <v-form @submit.prevent="emitCesiumDataset">
        <v-card-title class="title">
          <span>Add Cesium tileset</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md class="pa-0">
            <v-layout>
              <v-flex>
                <v-text-field
                  label="Name"
                  browser-autocomplete="on"
                  name="cesium_asset_name"
                  v-model="name"
                  clearable
                  required
                ></v-text-field>
              </v-flex>
              <v-flex>
                <v-text-field
                  label="Asset Id"
                  browser-autocomplete="on"
                  name="cesium_asset_id"
                  v-model="assetId"
                  clearable
                  required
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="close">Cancel</v-btn>
          <v-btn color="primary" flat type="submit" :disabled="!assetId"
            >Ok
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<style lang="scss" scoped>
.layers {
  max-height: 350px;
  overflow: auto;
}
</style>
