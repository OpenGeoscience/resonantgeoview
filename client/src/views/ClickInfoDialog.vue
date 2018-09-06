<template>
<v-dialog :value="datasetsInfo" @input="$emit('input', $event)" max-width="400px" scrollable>
  <v-card>
    <v-card-title class="headline">Info</v-card-title>
    <v-card-text>
      <div class="dataset" v-for="(datasetInfo,index) of datasetsInfo" :key="index">
        <div class="subheading">{{datasetInfo.dataset.name}}</div>
        <div class="info-table">
          <div class="table-row" v-for="(value, key) in datasetInfo.info" :key="key">
            <div class="row-key">{{key}}</div>
            <div class="row-value">{{value}}</div>
          </div>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="$emit('input', false)">
        OK
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
</template>

<script>
import groupBy from "lodash-es/groupBy";

import { ignoreProperties } from "../utils/geojsonUtil";

export default {
  name: "ClickInfoDialog",
  props: {
    value: {
      type: Boolean,
      required: true
    },
    datasetClickEvents: {
      type: Array
    }
  },
  data() {
    return {
      image: null
    };
  },
  computed: {},
  asyncComputed: {
    async datasetsInfo() {
      if (!this.datasetClickEvents.length) {
        return new Promise((resolve, reject) => {
          setTimeout(() => {
            resolve(null);
          }, 300);
        });
      } else {
        var datasetsInfo = await Promise.all(
          this.datasetClickEvents.map(async datasetClickEvent => {
            switch (datasetClickEvent.dataset.geometa.driver) {
              case "GeoJSON":
                return {
                  dataset: datasetClickEvent.dataset,
                  info: await this.getGeojsonLayersInfo(datasetClickEvent)
                };
                break;
              case "GeoTIFF":
                return {
                  dataset: datasetClickEvent.dataset,
                  info: await this.getGeotiffLayersInfo(datasetClickEvent)
                };
                break;
            }
          })
        );
        datasetsInfo = datasetsInfo.filter(data => data.info);
        if (!datasetsInfo.length) {
          return null;
        }
        return datasetsInfo;
      }
    }
  },
  created() {},
  watch: {},
  methods: {
    getGeojsonLayersInfo(datasetClickEvent) {
      var geojson = datasetClickEvent.clickEvent.data;
      if (!geojson.properties) {
        Promise.resolve(null);
      }
      var output = {};
      var filtered = Object.entries(geojson.properties).forEach(
        ([key, value]) => {
          if (ignoreProperties.indexOf(key) === -1) {
            output[key] = value;
          }
        }
      );
      return Promise.resolve(output);
    },
    getGeotiffLayersInfo(datasetClickEvent) {
      let itemId = datasetClickEvent.dataset._id;
      let coord = datasetClickEvent.clickEvent.geo;
      return this.$girder
        .get(`item/${itemId}/tiles/pixel`, {
          params: {
            top: coord.y,
            left: coord.x,
            projection: "EPSG:3857",
            units: "EPSG:4326"
          }
        })
        .then(({ data: result }) => {
          if (!result || !result.bands) {
            return null;
          }
          return result.bands;
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.v-card__text {
  padding-top: 0;
}

.dataset:not(:first-child) {
  margin-top: 20px;
}

.info-table {
  border: 1px solid #d0d0d0;
  white-space: nowrap;

  .table-row {
    display: flex;

    .row-key {
      border-right: 1px solid #d0d0d0;
      width: 30%;
      white-space: normal;
      padding: 1px 8px 1px 12px;
    }

    .row-value {
      width: 70%;
      white-space: normal;
      padding: 1px 12px 1px 8px;
    }

    &:nth-child(odd) {
      background: #f3f3f3;
    }
  }
}
</style>
