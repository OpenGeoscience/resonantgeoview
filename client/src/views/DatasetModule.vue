<template>
  <div class="datasets">
    <v-list dense expand>
      <transition-group name="fade" tag="div">
        <v-list-group
          v-for="group in groupedDatasets"
          :key="group.key"
          prepend-icon="folder"
          no-action
        >
          <v-list-tile class="group" slot="activator">
            <v-list-tile-content>
              <v-list-tile-title>{{ group.name }}</v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action v-if="group.group" @click.stop>
              <v-menu
                lazy
                offset-y
                absolute
                :nudge-bottom="20"
                :nudge-left="20"
              >
                <v-btn
                  class="group-menu-button"
                  slot="activator"
                  flat
                  icon
                  color="grey darken-2"
                >
                  <v-icon>more_vert</v-icon>
                </v-btn>
                <v-list>
                  <v-list-tile @click="deleteGroup(group.group)">
                    <v-list-tile-title>Remove Group</v-list-tile-title>
                  </v-list-tile>
                </v-list>
              </v-menu>
            </v-list-tile-action>
          </v-list-tile>
          <v-list-tile v-if="!group.datasets.length">
            <v-list-tile-action>
              <span><!-- v-list-tile-action can't take empty child --></span>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Empty Group</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile
            class="dataset"
            v-for="dataset in group.datasets"
            :key="dataset._id"
            @mouseenter.native="debouncedSetSelectedDataset(dataset)"
            @mouseleave.native="
              debouncedSetSelectedDataset.cancel(), setSelectedDataset(null)
            "
          >
            <v-list-tile-action>
              <v-btn
                flat
                icon
                key="add"
                class="add-button"
                v-if="
                  focusedWorkspace &&
                    focusedWorkspace.layers
                      .map(layer => layer.dataset)
                      .indexOf(dataset) === -1
                "
                color="grey lighten-1"
                @click="tryAddDatasetToWorkspace(dataset)"
                :loading="loadingDatasetIds[dataset._id]"
                :disabled="!allowAddToWorkspace(dataset)"
              >
                <v-icon>fa-globe-americas</v-icon>
              </v-btn>
              <v-btn
                flat
                icon
                key="remove"
                v-else
                color="grey darken-2"
                @click="
                  removeDatasetFromWorkspace({
                    dataset,
                    workspace: focusedWorkspace
                  })
                "
              >
                <v-icon>fa-globe-americas</v-icon>
              </v-btn>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title
                :class="{
                  'grey--text text--lighten-2':
                    filteredDatasetIds &&
                    filteredDatasetIds.indexOf(dataset._id) === -1
                }"
                >{{ dataset.name }}</v-list-tile-title
              >
            </v-list-tile-content>
            <v-list-tile-action v-if="!dataset._id.startsWith('adhoc_')">
              <v-menu
                lazy
                offset-y
                absolute
                :nudge-bottom="20"
                :nudge-left="20"
              >
                <v-btn
                  class="dataset-menu-button"
                  slot="activator"
                  flat
                  icon
                  color="grey darken-2"
                >
                  <v-icon>more_vert</v-icon>
                </v-btn>
                <v-list>
                  <v-list-tile
                    @click="
                      selectedDataset = dataset;
                      showAddToGroup = true;
                    "
                  >
                    <v-list-tile-title>Add to group</v-list-tile-title>
                  </v-list-tile>
                  <v-list-tile
                    v-if="group.group"
                    @click="
                      removeDatasetFromGroup({ group: group.group, dataset })
                    "
                  >
                    <v-list-tile-title>Remove from group</v-list-tile-title>
                  </v-list-tile>
                  <v-divider />
                  <v-list-tile @click="deleteDataset(dataset)">
                    <v-list-tile-title>Delete</v-list-tile-title>
                  </v-list-tile>
                  <v-list-tile
                    :href="`${API_URL}/item/${dataset._id}/download`"
                    target="_blank"
                  >
                    <v-list-tile-title>Download</v-list-tile-title>
                  </v-list-tile>
                </v-list>
              </v-menu>
            </v-list-tile-action>
          </v-list-tile>
        </v-list-group>
      </transition-group>
    </v-list>
    <DatasetGroupDialog
      v-if="showAddToGroup"
      v-model="showAddToGroup"
      :dataset="selectedDataset"
    />
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import groupBy from "lodash-es/groupBy";
import debounce from "lodash-es/debounce";
import keyBy from "lodash-es/keyBy";

import { API_URL } from "../constants";
import DatasetGroupDialog from "./DatasetGroupDialog";
import getDatasetDriver from "../utils/getDatasetDriver";

export default {
  name: "DatasetModule",
  components: { DatasetGroupDialog },
  inject: ["girderRest"],
  props: ["filteredDatasetIds"],
  data() {
    return {
      API_URL,
      showAddToGroup: false,
      selectedDataset: null
    };
  },
  computed: {
    groupedDatasets() {
      var datasetMap = keyBy(this.datasets, "_id");
      var namedGroups = this.groups.map(group => {
        return {
          name: group.name,
          group,
          key: group._id,
          datasets: group.datasetIds
            .filter(id => datasetMap[id])
            .map(id => datasetMap[id])
        };
      });
      var typeGroups = Object.entries(
        groupBy(
          this.datasets.filter(dataset => !dataset._id.startsWith("adhoc_")),
          dataset => dataset.geometa.type_
        )
      ).map(([type, datasets]) => {
        return {
          name: type,
          key: type,
          datasets
        };
      });
      let adhocDatasets = this.datasets.filter(dataset =>
        dataset._id.startsWith("adhoc_")
      );
      if (adhocDatasets.length) {
        typeGroups.unshift({
          name: "ad-hoc",
          key: "ad-hoc",
          datasets: adhocDatasets
        });
      }
      return [...typeGroups, ...namedGroups];
    },
    ...mapState([
      "datasets",
      "groups",
      "datasetSortBy",
      "loadingDatasetIds",
      "workspaces"
    ]),
    ...mapGetters(["focusedWorkspace"])
  },
  watch: {},
  created() {
    this.debouncedSetSelectedDataset = debounce(this.setSelectedDataset, 200);
  },
  methods: {
    ...mapMutations([
      "addWorkspace",
      "setSelectedDataset",
      "removeDatasetFromWorkspace"
    ]),
    ...mapActions([
      "deleteGroup",
      "deleteDataset",
      "addDatasetToWorkspace",
      "removeDatasetFromGroup"
    ]),
    allowAddToWorkspace(dataset) {
      if (this.loadingDatasetIds[dataset._id]) {
        return false;
      }
      var workspaceType = null;
      if (
        ["GeoJSON", "GeoTIFF", "WMS", "Network Common Data Format"].includes(
          getDatasetDriver(dataset)
        )
      ) {
        workspaceType = "geojs";
      }
      if (getDatasetDriver(dataset) === "OBJ") {
        workspaceType = "vtk";
      }
      if (
        Object.keys(this.workspaces).length < 2 ||
        this.focusedWorkspace.type === workspaceType
      ) {
        return workspaceType;
      } else {
        return false;
      }
    },
    tryAddDatasetToWorkspace(dataset) {
      var workspaceType = this.allowAddToWorkspace(dataset);
      if (workspaceType !== this.focusedWorkspace.type) {
        this.addWorkspace(workspaceType);
      }
      this.addDatasetToWorkspace({
        dataset,
        workspace: this.focusedWorkspace
      });
    }
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

.dataset {
  .dataset-menu-button {
    display: none;
  }

  &:hover {
    .dataset-menu-button {
      display: initial;
    }
  }
}
</style>

<style lang="scss">
.datasets {
  .v-list__group__header .v-list__group__header__prepend-icon {
    padding: 0 0 0 6px;
    min-width: 0;
  }

  .v-list__group__items--no-action .v-list__tile {
    padding-left: 15px;
  }

  .v-list__tile__action,
  .v-list__tile__avatar {
    min-width: 40px;
    padding: 0 9px;
  }

  .v-list--dense .v-list__tile .icon.fa {
    font-size: 20px;
  }

  .add-button.theme--light.v-btn.v-btn--disabled .v-icon {
    color: rgba(199, 199, 199, 0.26) !important;
  }
}
</style>
