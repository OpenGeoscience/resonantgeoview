<script>
// This is an initial proof of concept so many things are hard coded
import { mapState } from "vuex";

import getDatasetDriver from "../utils/getDatasetDriver";

export default {
  name: "GaiaProcessingDialog",
  components: {},
  inject: ["girderRest"],
  props: {
    value: {
      type: Boolean,
      required: true
    },
    dest: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      newDatasetName: "",
      processings: [
        {
          name: "crop",
          label: "Crop"
        }
      ],
      selectedProcessing: "crop",
      dataset1: null,
      dataset2: null
    };
  },
  computed: {
    ...mapState(["datasets"]),
    geojsonDatasets() {
      return this.datasets.filter(dataset => getDatasetDriver(dataset) === "GeoJSON");
    }
  },
  methods: {
    startGaiaProcessing() {
      return this.girderRest
        .get(`/gaia/crop`, {
          params: {
            itemId: this.dataset1._id,
            byitemId: this.dataset2._id,
            name: this.newDatasetName,
            folderId: this.dest._id
          }
        })
        .then(({ data: job }) => {
          this.close();
          this.$emit("processJobCreated", job);
        });
    },
    close() {
      this.dataset1 = null;
      this.dataset2 = null;
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
    max-width="500px"
    persistent
    lazy
  >
    <v-card>
      <v-form @submit.prevent="startGaiaProcessing">
        <v-card-title class="title">
          <span>Processing</span>
        </v-card-title>
        <!-- <v-card-text> -->
        <v-container grid-list-md class="">
          <v-layout>
            <v-flex>
              <v-select
                :items="processings"
                hide-details
                item-text="label"
                item-value="name"
                label="Process"
                menu-props="lazy"
                v-model="selectedProcessing"
              />
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex>
              <v-select
                :items="datasets"
                hide-details
                item-text="name"
                :item-value="value => value"
                label="Target dataset"
                menu-props="lazy"
                v-model="dataset1"
              />
            </v-flex>
          </v-layout>
        </v-container>
        <v-subheader class="mt-2" style="height:32px;">Parameters</v-subheader>
        <v-container grid-list-md class="pt-0">
          <v-layout>
            <v-flex>
              <v-select
                :items="geojsonDatasets"
                hide-details
                item-text="name"
                :item-value="value => value"
                label="By dataset"
                menu-props="lazy"
                v-model="dataset2"
              />
            </v-flex>
          </v-layout>
        </v-container>
        <v-container grid-list-md>
          <v-layout>
            <v-flex>
              <v-text-field
                label="New dataset name"
                browser-autocomplete="on"
                name="processing_dataset_name"
                v-model="newDatasetName"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <!-- </v-card-text> -->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="close">Cancel</v-btn>
          <v-btn
            color="primary"
            flat
            type="submit"
            :disabled="
              !newDatasetName ||
                !selectedProcessing ||
                !dataset1 ||
                !dataset2 ||
                dataset2.geometa.driver !== 'GeoJSON'
            "
            >Start</v-btn
          >
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>
