<template>
  <div class='layers'>
    <v-subheader>Layers</v-subheader>
    <v-list dense expand two-line>
      <draggable v-model="layers" :options="{handle:'.drag-handle'}">
        <transition-group name="fade-group" tag="div">
          <v-list-tile
          v-for="layer in layers"
          :key="layer.dataset._id"
          class="layer"
          @click="123"
          >
            <v-list-tile-action>
              <v-btn flat icon color="grey darken-2" @click="removeDatasetFromWorkspace({dataset:layer.dataset,workspace:focusedWorkspace})">
                <v-icon>fa-globe-americas</v-icon>
              </v-btn>
            </v-list-tile-action>
            <v-list-tile-content>
                <v-list-tile-title v-text="layer.dataset.name"></v-list-tile-title>
                <v-list-tile-sub-title>
                  <v-slider hide-details class="pt-0 pr-5 mx-3" 
                    :min="0"
                    :max="1"
                    :step="0.01"
                    :value="layer.opacity" 
                    @input="setWorkspaceLayerOpacity({layer,opacity:$event})"
                  ></v-slider>
                </v-list-tile-sub-title>
            </v-list-tile-content>
            <v-list-tile-action class="drag-handle">
              <v-icon>drag_indicator</v-icon>
            </v-list-tile-action>
          </v-list-tile>
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

import DatasetGroupDialog from "./DatasetGroupDialog";

export default {
  name: "LayerModule",
  components: { DatasetGroupDialog, draggable },
  data() {
    return {
      showAddToGroup: false,
      selectedDataset: null
    };
  },
  computed: {
    // ...mapState(["datasets", "groups", "datasetSortBy"]),
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
  .list__tile__action,
  .list__tile__avatar {
    min-width: 40px;
    padding: 0 9px;
  }
}
</style>
