<template>
  <div class='layers'>
    <v-subheader>Layers</v-subheader>
    <v-list dense expand>
      <draggable v-model="layers" :options="{
          draggable:'.layer',
          handle:'.drag-handle'
        }"
        @start="transitionName=''"
        @end="transitionName='fade-group'">
        <transition-group :name="transitionName" tag="div">
          <v-list-group
            v-for="layer in layers"
            :key="layer.dataset._id"
            class="layer"
            append-icon="">
            <v-list-tile
              slot="activator"
              class="hover-show-parent width-fix"
              @click="123">
              <v-list-tile-action>
                <v-btn flat icon color="grey darken-2" @click="removeDatasetFromWorkspace({dataset:layer.dataset,workspace:focusedWorkspace})">
                  <v-icon>fa-globe-americas</v-icon>
                </v-btn>
              </v-list-tile-action>
              <v-list-tile-content>
                  <v-list-tile-title v-text="layer.dataset.name"></v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action class="hover-show-child" @click.stop>
                <v-menu lazy offset-y absolute :nudge-bottom="20" :nudge-left="20">
                  <v-btn class="group-menu-button" slot="activator" flat icon color="grey darken-2">
                    <v-icon>more_vert</v-icon>
                  </v-btn>
                  <v-list>
                    <v-list-tile 
                      v-if="['GeoTIFF', 'GeoJSON', 'Network Common Data Format'].indexOf(getDatasetDriver(layer.dataset))!==-1"
                      @click="$emit('customDataset',layer.dataset)">
                      <v-list-tile-title>Customize</v-list-tile-title>
                    </v-list-tile>
                    <v-list-tile @click="$emit('zoomToDataset',layer.dataset)">
                      <v-list-tile-title>Zoom to</v-list-tile-title>
                    </v-list-tile>
                  </v-list>
                </v-menu>
              </v-list-tile-action>
              <v-list-tile-action class="drag-handle hover-show-child">
                <v-icon>drag_indicator</v-icon>
              </v-list-tile-action>
            </v-list-tile>

            <v-list-tile
              @click="123"
            >
              <v-list-tile-content>
                <v-list-tile-title>
                  <v-layout>
                    <v-flex>
                      Opacity
                    </v-flex>
                    <v-flex>
                      <v-slider hide-details class="opacity-slider pr-3"
                        :min="0"
                        :max="1"
                        :step="0.01"
                        :value="layer.opacity"
                        @input="setWorkspaceLayerOpacity({layer,opacity:$event})"></v-slider>
                    </v-flex>
                    <v-flex>
                      {{layer.opacity.toFixed(2)}}
                    </v-flex>
                  </v-layout>
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
        </transition-group>
      </draggable>
    </v-list>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import groupBy from "lodash-es/groupBy";
import debounce from "lodash-es/debounce";
import keyBy from "lodash-es/keyBy";
import mapValues from "lodash-es/mapValues";
import draggable from "vuedraggable";

import getDatasetDriver from "../utils/getDatasetDriver";

export default {
  name: "LayerModule",
  components: { draggable },
  data() {
    return {
      getDatasetDriver,
      showAddToGroup: false,
      selectedDataset: null,
      transitionName: "fade-group"
    };
  },
  computed: {
    layers: {
      get() {
        return this.focusedWorkspace.layers;
      },
      set(layers) {
        this.setWorkspaceLayers({
          workspace: this.focusedWorkspace,
          layers
        });
      }
    },
    ...mapGetters(["focusedWorkspace"])
  },
  watch: {},
  created() {
    this.debouncedSetSelectedDataset = debounce(this.setSelectedDataset, 200);
  },
  methods: {
    ...mapMutations([
      "setSelectedDataset",
      "removeDatasetFromWorkspace",
      "setWorkspaceLayers",
      "setWorkspaceLayerOpacity"
    ]),
    ...mapActions([])
  }
};
</script>

<style lang="scss" scoped>
</style>

<style lang="scss">
.layers {
  .v-list__tile__action {
    min-width: 40px;
    padding: 0 8px;
  }

  .layer {
    // A fix that when v-list-group is not an immediate child of v-list its transition is not working correctly
    .expand-transition-leave-to {
      display: none !important;
    }

    .opacity-slider {
      margin-top: -4px;
    }
  }
}

.width-fix {
  width: 100%;
}

.hover-show-parent {
  .hover-show-child {
    display: none;

    &.show {
      display: flex;
    }
  }

  &:hover {
    .hover-show-child {
      display: inherit;
    }
  }
}
</style>
