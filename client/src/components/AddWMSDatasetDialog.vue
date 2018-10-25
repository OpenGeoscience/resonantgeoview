<script>
import debounce from "lodash-es/debounce";
import axios from "axios";
// import xml2json from "simple-xml2json";
// import xmlJs from "xml-js";
import fastXmlParser from "fast-xml-parser";
// import proj4 from "proj4";

export default {
  name: "AddWMSDatasetDialog",
  components: {},
  props: {
    value: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      url: "",
      capabilities: null,
      selectedLayer: null,
      loadingCapabilities: false,
      validatingLayer: false,
      validUrl: true,
      validLayer: true
    };
  },
  computed: {
    layers() {
      if (!this.capabilities) {
        return [];
      }
      var layers = [];
      var layersStack = [
        [this.capabilities.WMS_Capabilities.Capability.Layer, 0]
      ];
      while (layersStack.length) {
        let [layer, level] = layersStack.pop();
        // if(layers.Name&&layers.)
        layers.push([layer, level]);
        if (layer.Layer) {
          if (Array.isArray(layer.Layer)) {
            layer.Layer.forEach(layer => {
              layersStack.push([layer, level + 1]);
            });
          } else {
            layersStack.push([layer.Layer, level + 1]);
          }
        }
      }
      return layers;
    }
  },
  watch: {
    url(newValue) {
      this.capabilities = null;
      this.validUrl = true;
      if (newValue) {
        this.loadingCapabilities = true;
        this.getCapabilities();
      } else {
        this.getCapabilities.cancel();
        this.loadingCapabilities = false;
      }
    },
    async selectedLayer() {
      this.validLayer = true;
      this.validatingLayer = true;
      this.validLayer = await this.validateLayer(this.selectedLayer);
      this.validatingLayer = false;
    }
  },
  created() {
    this.getCapabilities = debounce(this.getCapabilities, 1000);
  },
  methods: {
    async getCapabilities() {
      var result = null;
      try {
        var { data: result } = await axios.get(this.url, {
          params: {
            request: "getCapabilities",
            service: "wms",
            version: "1.3.0"
          },
          timeout: 2000,
          responseType: "text"
        });
        var capabilities = fastXmlParser.parse(result, {
          ignoreAttributes: false
        });
        if (!capabilities.WMS_Capabilities) {
          throw new Error("Invalid capabilities");
        }
        this.capabilities = capabilities;
      } catch (ex) {
        this.validUrl = false;
        this.capabilities = null;
      }
      this.loadingCapabilities = false;
    },
    tryGetValidBoundingBox(EX_GeographicBoundingBox) {
      return EX_GeographicBoundingBox;
    },
    async validateLayer(layer) {
      if (!layer) {
        return false;
      }
      if (!layer.Title) {
        return false;
      }
      if (!this.tryGetValidBoundingBox(layer.EX_GeographicBoundingBox)) {
        return null;
      }

      var { headers } = await axios.get(this.url, {
        params: {
          SERVICE: "WMS",
          VERSION: "1.3.0",
          REQUEST: "GetMap",
          LAYERS: layer.Name,
          STYLES: "",
          BBOX: "-90,-180,90,180",
          WIDTH: 256,
          HEIGHT: 256,
          FORMAT: "image/png",
          TRANSPARENT: true,
          CRS: "EPSG:3857",
          TILED: true
        },
        responseType: "stream"
      });
      if (headers["content-type"] !== "image/png") {
        return null;
      }
      return true;
    },
    emitWMSDataset() {
      var EX_GeographicBoundingBox = this.selectedLayer
        .EX_GeographicBoundingBox;
      var minx = Number.MIN_SAFE_INTEGER;
      var maxx = Number.MAX_SAFE_INTEGER;
      var miny = Number.MIN_SAFE_INTEGER;
      var maxy = Number.MAX_SAFE_INTEGER;
      if (EX_GeographicBoundingBox) {
        minx = parseFloat(EX_GeographicBoundingBox.westBoundLongitude);
        maxx = parseFloat(EX_GeographicBoundingBox.eastBoundLongitude);
        miny = parseFloat(EX_GeographicBoundingBox.southBoundLatitude);
        maxy = parseFloat(EX_GeographicBoundingBox.northBoundLatitude);
      }
      minx = minx < -180 ? -180 : minx;
      maxx = maxx > 180 ? 180 : maxx;
      miny = miny < -90 ? -90 : miny;
      maxy = maxy > 90 ? 90 : maxy;

      var geometa = {
        crs: "+proj=longlat +datum=WGS84 +no_defs ",
        driver: "WMS",
        bounds: {
          type: "Polygon",
          coordinates: [
            [
              [minx, miny],
              [minx, maxy],
              [maxx, maxy],
              [maxx, miny],
              [minx, miny]
            ]
          ]
        },
        nativeBounds: {
          top: maxy,
          right: maxx,
          bottom: miny,
          left: minx
        },
        url: this.url,
        layer: this.selectedLayer.Name,
        type_: "raster"
      };
      this.$emit("dataset", {
        name: this.selectedLayer.Title,
        geometa
      });
      this.close();
    },
    close() {
      this.url = "";
      this.selectedLayer = null;
      this.capabilities = null;
      this.$emit("input", false);
    }
  }
};
</script>

<template>
<v-dialog :value="value" @input="$emit('input', $event)" scrollable max-width="650px" persistent>
  <v-card>
    <v-form @submit.prevent="emitWMSDataset">
      <v-card-title class="title">
        <span>Add WMS</span>
      </v-card-title>
      <v-card-text>
        <v-container grid-list-md class='pa-0'>
          <v-layout>
            <v-flex>
              <v-text-field
                label="WMS URL"
                browser-autocomplete="on"
                name="wms_url"
                v-model="url"
                :loading="loadingCapabilities"
                :error-messages="validUrl?'':'Invalid WMS serivce URL'"
                clearable
                required></v-text-field>
            </v-flex>
          </v-layout>
          <v-list two-line subheader dense v-if="layers.length" class="layers">
            <v-subheader>Layers</v-subheader>
            <v-list-tile
              v-for="[layer,level] of layers"
              :key="layer.Name+level"
              :class="{'selected':selectedLayer===layer}"
              @click="selectedLayer=layer">
              <v-list-tile-content
                :style="{paddingLeft:(15*level)+'px'}">
                <v-list-tile-title>{{ layer.Name }}</v-list-tile-title>
                <v-tooltip bottom :open-delay="400">
                  <v-list-tile-sub-title slot="activator">
                    <div>{{ layer.Title }}</div>
                    <div v-if="!validLayer&&layer===selectedLayer"
                      class="red--text text--darken-4">{{validLayer===false?'Missing required metadata':'May not work properly'}}</div>
                  </v-list-tile-sub-title>
                  <span>{{ layer.Abstract }}</span>
                </v-tooltip>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat
          @click="close">Cancel</v-btn>
        <v-btn color="primary"
          flat
          type="submit"
          :disabled="!selectedLayer||validatingLayer"
          :loading="validatingLayer">Ok</v-btn>
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
