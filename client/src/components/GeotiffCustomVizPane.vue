<template>
  <v-container fluid grid-list-md class="pa-0 geotiff-customize-viz-pane">
    <v-subheader class="pl-2">Type</v-subheader>
    <v-layout class="px-3">
      <v-flex>
        <v-radio-group
          class="mt-0"
          hide-details
          v-model="mode">
          <v-radio label="Default" value="default"></v-radio>
          <v-radio label="Custom" value="custom"></v-radio>
        </v-radio-group>
      </v-flex>
    </v-layout>
    <template v-if="vizProperties">
      <v-subheader class="pl-2">Properties</v-subheader>
      <div class="px-4">
        <v-layout>
          <v-flex xs5>
            <v-select
              :items="bands"
              hide-details
              label="Band"
              placeholder=" "
              v-model="vizProperties.band" />
          </v-flex>
        </v-layout>
        <v-layout>
          <v-flex xs6>
            <PalettePicker
              :palette.sync="vizProperties.palette" />
          </v-flex>
          <v-flex xs6>
            <v-select
              :items="[{name:'Continuous',value:'linear'},{name:'Discrete',value:'discrete'}]"
              item-text="name"
              item-value="value"
              hide-details
              label="Type"
              placeholder=" "
              v-model="vizProperties.type" />
          </v-flex>
        </v-layout>
        <v-layout class="mt-2">
          <v-flex xs6>
            <v-text-field
              v-model.number="vizProperties.range[0]"
              label="Min"
              hide-details
              type="number"
              @input="minMaxChange($event)"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              v-model.number="vizProperties.range[1]"
              label="Max"
              hide-details
              type="number"
              @input="minMaxChange($event)"
            ></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout class="mt-2">
          <v-flex>
            <v-range-slider
            v-model="vizProperties.range"
            :max="max"
            :min="min"
            :step="1"
          ></v-range-slider>
          </v-flex>
        </v-layout>
      </div>
    </template>
    <v-layout align-center class="px-4">
      <v-flex xs7>
        <v-checkbox
          hide-details
          class="mt-0"
          label="Save to dataset"
          :input-value="preserve"
          @change="$emit('update:preserve',$event)"
        ></v-checkbox>
      </v-flex>
      <v-flex xs4 offset-xs1>
        <v-btn block outline color='primary' class='' @click="revert">
          Revert
        </v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import cloneDeep from "lodash-es/cloneDeep";
import debounce from "lodash-es/debounce";

import PalettePicker from "./VectorCustomVizPane/PalettePicker";
import {
  colorbrewerCategories,
  toPaletteColors
} from "../utils/palettableColorbrewerMapper";

export default {
  name: "GeotiffCustomVizPane",
  components: { PalettePicker },
  props: {
    dataset: {
      type: Object,
      required: true
    },
    meta: {
      type: Object,
      required: true
    },
    preserve: {
      type: Boolean,
      default: null
    },
    palettePickerExtras: {
      type: Object
    }
  },
  data() {
    var vizProperties = this.dataset.meta.vizProperties;
    var min = 0;
    var max = 100;
    if (vizProperties && vizProperties.band) {
      var minMax = this.getBandMinMax(vizProperties.band);
      min = vizProperties.range ? vizProperties.range[0] : minMax[0];
      max = vizProperties.range ? vizProperties.range[1] : minMax[1];
    }
    return {
      initialVizProperties: cloneDeep(vizProperties),
      vizProperties: cloneDeep(vizProperties),
      max,
      min
    };
  },
  computed: {
    bands() {
      return Object.keys(this.meta.bands);
    },
    mode: {
      get() {
        return this.vizProperties ? "custom" : "default";
      },
      set(newValue) {
        switch (newValue) {
          case "default":
            this.vizProperties = null;
            break;
          case "custom":
            var band = this.bands[0];
            this.vizProperties = {
              band: this.bands[0],
              palette: toPaletteColors(
                colorbrewerCategories[Object.keys(colorbrewerCategories)[0]][0]
              ),
              type: "linear",
              range: null
            };
            this.vizProperties.range = this.getBandMinMax(band);
            break;
        }
      }
    }
  },
  provide() {
    return {
      palettePickerExtras: { ...this.palettePickerExtras }
    };
  },
  watch: {
    vizProperties: {
      handler() {
        this.debouncedApply();
      },
      deep: true
    },
    "vizProperties.band"(band) {
      var minMax = this.getBandMinMax(band);
      this.min = minMax[0];
      this.max = minMax[1];
    }
  },
  created() {
    this.debouncedApply = debounce(this.apply, 200);
  },
  methods: {
    apply() {
      this.$set(
        this.dataset.meta,
        "vizProperties",
        cloneDeep(this.vizProperties)
      );
    },
    revert() {
      this.vizProperties = cloneDeep(this.initialVizProperties);
    },
    getBandMinMax(band) {
      if (band) {
        return [
          parseInt(this.meta.bands[band].min.toFixed(0)),
          parseInt(this.meta.bands[band].max.toFixed(0))
        ];
      } else {
        return [0, 100];
      }
    },
    minMaxChange(number) {
      if (number < this.min) {
        this.min = number;
      } else if (number > this.max) {
        this.max = number;
      }
    }
  }
};
</script>

<style>
</style>
