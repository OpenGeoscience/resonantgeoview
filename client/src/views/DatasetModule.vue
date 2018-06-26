<template>
  <div class='datasets'>
    <v-list dense>
      <v-list-group
        v-for="(datasets, key) in groupedDatasets"
        :key="key"
        prepend-icon="folder"
        no-action
      >
        <v-list-tile slot="activator">
          <v-list-tile-content>
            <v-list-tile-title>{{ key }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          v-for="dataset in datasets"
          :key="dataset.name"
          @click="123"
          @mouseenter.native="debouncedSetSelectedDataset(dataset)"
          @mouseleave.native="debouncedSetSelectedDataset.cancel(),setSelectedDataset(null)">
          <v-list-tile-action>
            <v-btn flat icon key="add" v-if="focusedWorkspace && focusedWorkspace.datasets.indexOf(dataset)===-1" color="grey lighten-2" @click="addDatasetToWorkspace({dataset,workspace:focusedWorkspace})">
              <v-icon>fa-globe-americas</v-icon>
            </v-btn>
            <v-btn flat icon key="remove" v-else color="grey darken-2" @click="removeDatasetFromWorkspace({dataset,workspace:focusedWorkspace})">
              <v-icon>fa-globe-americas</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ dataset.name }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list-group>
    </v-list>
  </div>
</template>

<style lang="scss" scoped>
</style>

<script>
import { mapState, mapMutations, mapGetters } from "vuex";
import groupBy from "lodash-es/groupBy";
import debounce from "lodash-es/debounce";

import TreeViewItem from "../components/TreeViewItem";

export default {
  name: "DatasetModule",
  components: { TreeViewItem },
  data() {
    return {};
  },
  computed: {
    groupedDatasets() {
      return groupBy(this.datasets, dataset => dataset.geometa.type_);
      // var a = Object.entries(
      //   groupBy(this.datasets, dataset => dataset.geometa.type_)
      // ).map(([key, value]) => {
      //   return {
      //     name: key,
      //     children: value.map(dataset => {
      //       return {
      //         name: dataset.name,
      //         data: dataset
      //       };
      //     })
      //   };
      // });
      // if (a[1]) {
      //   let children = a[1].children.slice();
      //   a[1].children.push({ name: "children", children });
      // }
      // return a;
    },
    ...mapState(["datasets", "datasetSortBy"]),
    ...mapGetters(["focusedWorkspace"])
  },
  watch: {},
  created() {
    this.$store.dispatch("loadDatasets");
    this.debouncedSetSelectedDataset = debounce(this.setSelectedDataset, 200);
  },
  methods: {
    ...mapMutations([
      "setSelectedDataset",
      "addDatasetToWorkspace",
      "removeDatasetFromWorkspace"
    ])
  }
};
</script>

<style lang="scss">
.datasets {
  .list__group__header .list__group__header__prepend-icon {
    padding: 0 0 0 6px;
    min-width: 0;
  }

  .list__group__items--no-action .list__tile {
    padding-left: 12px;
  }

  .list__tile__action,
  .list__tile__avatar {
    min-width: 40px;
    padding: 0 9px;
  }

  .list--dense .list__tile .icon.fa {
    font-size: 20px;
  }
}
</style>
