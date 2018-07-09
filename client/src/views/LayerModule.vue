<template>
  <div class='layers'>
    <v-subheader>Layers</v-subheader>
    <v-list dense expand>
      <transition-group name="fade-group" tag="div">
        <v-list-tile
        v-for="dataset in focusedWorkspace.datasets"
        :key="dataset.name"
        class="dataset"
        @click="123"
        >
        <v-list-tile-action>
          <v-btn flat icon key="add" v-if="focusedWorkspace && focusedWorkspace.datasets.indexOf(dataset)===-1" color="grey lighten-2" @click="addDatasetToWorkspace({dataset,workspace:focusedWorkspace})">
            <v-icon>fa-globe-americas</v-icon>
          </v-btn>
          <v-btn flat icon key="remove" v-else color="grey darken-2" @click="removeDatasetFromWorkspace({dataset,workspace:focusedWorkspace})">
            <v-icon>fa-globe-americas</v-icon>
          </v-btn>
        </v-list-tile-action>
        <v-list-tile-content>
            <v-list-tile-title v-text="dataset.name"></v-list-tile-title>
        </v-list-tile-content>
        </v-list-tile>
      </transition-group>
    </v-list>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import groupBy from "lodash-es/groupBy";
import debounce from "lodash-es/debounce";
import keyBy from "lodash-es/keyBy";
import mapValues from "lodash-es/mapValues";

import DatasetGroupDialog from "./DatasetGroupDialog";

export default {
  name: "LayerModule",
  components: { DatasetGroupDialog },
  data() {
    return {
      showAddToGroup: false,
      selectedDataset: null
    };
  },
  computed: {
    // ...mapState(["datasets", "groups", "datasetSortBy"]),
    ...mapGetters(["focusedWorkspace"])
  },
  watch: {},
  created() {
    this.debouncedSetSelectedDataset = debounce(this.setSelectedDataset, 200);
  },
  methods: {
    ...mapMutations(["setSelectedDataset", "removeDatasetFromWorkspace"]),
    ...mapActions([])
  }
};
</script>

<style lang="scss" scoped>
.group {
  .group-menu-button {
    display: none;
    position: relative;
    left: 30px;
  }

  &:hover {
    .group-menu-button {
      display: initial;
    }
  }
}
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
