

<template>
  <FullScreenViewport>
    <WorkspaceContainer
      :focused="focusedWorkspace"
      @update:focused="setFocusedWorkspaceKey($event)"
      :autoResize="true"
      :max="2"
      :flex-grow-first="5/4"
    >
      <Workspace
        v-for="(workspace, key) in workspaces"
        :key="key"
        :identifier="key"
        @split="addWorkspace()"
        @close="removeWorkspace(key)">
        <GeojsMapViewport
          class='map'
          :viewport.sync='viewport'
        >
          <GeojsTileLayer
            url='https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png'
            attribution='© OpenStreetMap contributors, © CARTO'
            :zIndex='0'>
          </GeojsTileLayer>
          <template v-for="(dataset,i) in workspace.datasets">
            <GeojsGeojsonDatasetLayer
              v-if="dataset.geometa.driver==='GeoJSON'"
              :key="dataset._id"
              :dataset="dataset"
              :zIndex="i+1">
            </GeojsGeojsonDatasetLayer>
            <GeojsTileLayer
              v-if="dataset.geometa.driver==='GeoTIFF'"
              :key="dataset._id"
              :url='getTileURL(dataset)'
              :keepLower="false"
              :zIndex='i+1'>
            </GeojsTileLayer>
          </template>
          <template v-if="selectedDatasetPoint && focusedWorkspaceKey===key">
            <GeojsGeojsonLayer
              :geojson="{type:'Point',coordinates:[selectedDatasetPoint.x, selectedDatasetPoint.y]}"
              :featureStyle="{point:{strokeColor:'black',strokeWidth:2,radius:3}}"
              :zIndex="workspace.datasets.length+1">
            </GeojsGeojsonLayer>
            <GeojsWidgetLayer
              :position="selectedDatasetPoint"
              :offset="{x:0,y:-20}"
              :zIndex="workspace.datasets.length+2">
              <v-chip small color="green" text-color="white">{{selectedDataset.name}}</v-chip>
            </GeojsWidgetLayer>
          </template>
        </GeojsMapViewport>
      </Workspace>
    </WorkspaceContainer>

    <SidePanel
    class="side-panel"
    :top="64"
    :toolbar="{title:'Datasets'}"
    :expanded="true"
    :footer="false"
    >
      <template slot="actions">
        <SidePanelAction
        v-for="action in actions" 
        :key="action.name"
        @click.stop="clickAction(action.name)">
        <v-icon>{{action.icon}}</v-icon>
        </SidePanelAction>
      </template>
      <div class="main">
        <DatasetModule />
      </div>
    </SidePanel>
  </FullScreenViewport>
</template>

<style lang="scss" scoped>
.map {
  z-index: 0;
}

.side-panel {
  display: flex;
  flex-direction: column;

  .main {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
  }
}
</style>
<script>
import { mapState, mapGetters, mapMutations } from "vuex";

import { API_URL } from "../constants";
// import WorkspaceContainer from "./Workspace/Container";
// import Workspace from "./Workspace/Workspace";
// import WorkspaceAction from "./Workspace/Action";
import WorkspaceContainer from "danesfield-client/src/views/Workspace/Container";
import Workspace from  "danesfield-client/src/views/Workspace/Workspace";
import WorkspaceAction from  "danesfield-client/src/views/Workspace/Action";
import DatasetModule from "./DatasetModule";
import GeojsGeojsonDatasetLayer from "./GeojsGeojsonDatasetLayer";

export default {
  name: "Explore",
  components: {
    DatasetModule,
    WorkspaceContainer,
    Workspace,
    WorkspaceAction,
    GeojsGeojsonDatasetLayer
  },
  data() {
    return {
      viewport: {
        center: [-100, 30],
        zoom: 4
      },
      drawing: false,
      editing: false
    };
  },
  computed: {
    actions() {
      return [];
    },
    ...mapState([
      "selectedDataset",
      "workspaces",
      "focusedWorkspace",
      "focusedWorkspaceKey"
    ]),
    ...mapGetters(["selectedDatasetPoint"])
    // ...mapState("workingSet", ["editingWorkingSet"]),
    // ...mapState("filter", [
    // "editingFilter",
    // "annotations",
    // "selectedCondition"
    // ]),
    // ...mapGetters("workingSet", ["datasetBoundsFeature"]),
    // ...mapGetters("filter", ["editingConditionsGeojson", "heatmapData"])
  },
  created() {},
  methods: {
    // createNewWorkspace(type) {
    //   this.workspaces.push({
    //     type,
    //     id: Math.random()
    //       .toString(36)
    //       .substring(7)
    //   });
    // },
    // close(workspace) {
    //   var index = this.workspaces.indexOf(workspace);
    //   this.workspaces.splice(index, 1);
    // }
    getTileURL(dataset) {
      var url = `${API_URL}/item/${
        dataset._id
      }/tiles/zxy/{z}/{x}/{y}?${encodeURI(
        "encoding=PNG&projection=EPSG:3857"
      )}`;
      return url;
    },
    ...mapMutations([
      "addWorkspace",
      "removeWorkspace",
      "setFocusedWorkspaceKey"
    ])
  }
};
</script>
