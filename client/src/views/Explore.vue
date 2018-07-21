

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
          <template v-for="(layer,i) in workspace.layers">
            <GeojsGeojsonDatasetLayer
              v-if="layer.dataset.geometa.driver==='GeoJSON'"
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :zIndex="workspace.layers.length-i"
              :opacity='layer.opacity'>
            </GeojsGeojsonDatasetLayer>
            <GeojsTileLayer
              v-if="layer.dataset.geometa.driver==='GeoTIFF'"
              :key="layer.dataset._id"
              :url='getTileURL(layer.dataset)'
              :keepLower="false"
              :zIndex='workspace.layers.length-i'
              :opacity='layer.opacity'>
            </GeojsTileLayer>
          </template>
          <template v-if="selectedDatasetPoint && focusedWorkspaceKey===key">
            <GeojsGeojsonLayer
              :geojson="selectedDatasetPoint"
              :featureStyle="{point:{strokeColor:'black',strokeWidth:2,radius:3}}"
              :zIndex="workspace.layers.length+1">
            </GeojsGeojsonLayer>
            <GeojsWidgetLayer
              :position="selectedDatasetPoint.coordinates"
              :offset="{x:0,y:-20}"
              :zIndex="workspace.layers.length+2">
              <v-chip small color="green" text-color="white">{{selectedDataset.name}}</v-chip>
            </GeojsWidgetLayer>
          </template>
        </GeojsMapViewport>
      </Workspace>
    </WorkspaceContainer>

    <SidePanel
    class="side-panel"
    :top="64"
    :floating="false"
    :bottom="0"
    :toolbar="{title:'Datasets'}"
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
        <DatasetModule class="datasets" />
        <LayerModule class="layers" v-if="focusedWorkspace &&focusedWorkspace.layers.length"/>
      </div>
    </SidePanel>
  </FullScreenViewport>
</template>

<script>
import { mapState, mapGetters, mapMutations } from "vuex";

import { API_URL } from "../constants";
import WorkspaceContainer from "danesfield-client/src/components/Workspace/Container";
import Workspace from "danesfield-client/src/components/Workspace/Workspace";
import WorkspaceAction from "danesfield-client/src/components/Workspace/Action";
import DatasetModule from "./DatasetModule";
import LayerModule from "./LayerModule";
import GeojsGeojsonDatasetLayer from "./GeojsGeojsonDatasetLayer";

export default {
  name: "Explore",
  components: {
    DatasetModule,
    LayerModule,
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
    ...mapState(["selectedDataset", "workspaces", "focusedWorkspaceKey"]),
    ...mapGetters(["selectedDatasetPoint", , "focusedWorkspace"])
  },
  created() {},
  methods: {
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


<style lang="scss" scoped>
.map {
  z-index: 0;
}

.side-panel {
  display: flex;
  flex-direction: column;

  .main {
    flex: 1;
    display: flex;
    flex-direction: column;

    .datasets {
      overflow-y: auto;
    }
  }
}
</style>
