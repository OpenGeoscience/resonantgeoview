

<template>
  <FullScreenViewport>
    <WorkspaceContainer
      :focused="focusedWorkspace"
      @update:focused="setFocusedWorkspaceKey($event)"
      :autoResize="true"
      :max="2"
    >
      <Workspace
        v-for="(workspace, key) in workspaces"
        :key="key"
        :identifier="key"
        @split="addWorkspace()"
        @close="removeWorkspace(key)">
        <GeojsMapViewport
          class='map'
          :viewport='viewport'
          ref='geojsMapViewport'
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
          <GeojsAnnotationLayer
            :drawing.sync="drawing"
            :editing.sync="editing"
            :editable="true"
            :annotations="annotations"
            @update:annotations="annotations=$event"
            :zIndex="workspace.layers.length+1">
          </GeojsAnnotationLayer>
          <GeojsGeojsonLayer
            v-if="filteringGeometry"
            :geojson="filteringGeometry"
            :featureStyle="{polygon:{strokeColor:'grey',strokeWidth:1,fillColor:'#1976d2',fillOpacity:0.3}}"
            :zIndex="workspace.layers.length+2">
          </GeojsGeojsonLayer>
          <template v-if="selectedDatasetPoint && focusedWorkspaceKey===key">
            <GeojsGeojsonLayer
              :geojson="selectedDatasetPoint"
              :featureStyle="{point:{strokeColor:'black',strokeWidth:2,radius:3}}"
              :zIndex="workspace.layers.length+3">
            </GeojsGeojsonLayer>
            <GeojsWidgetLayer
              :position="selectedDatasetPoint.coordinates"
              :offset="{x:0,y:-20}"
              :zIndex="workspace.layers.length+4">
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
    :footer="false">
      <template slot="actions">
        <SidePanelAction @click="drawing = 'rectangle'">
          <v-icon>aspect_ratio</v-icon>
        </SidePanelAction>
      </template>
      <div class="main">
        <transition name="fade">
          <div v-if="filteredDatasetIds">
            <v-switch hide-details label="Filtering" :input-value="!!filteringGeometry" @change="filteringGeometry=null" class="mt-0 mx-1"></v-switch>
          </div>
        </transition>
        <DatasetModule class="datasets"
          :filteredDatasetIds="filteredDatasetIds" />
        <LayerModule class="layers" 
          v-if="focusedWorkspace &&focusedWorkspace.layers.length"
          @zoomToDataset="zoomToDataset"/>
      </div>
    </SidePanel>
  </FullScreenViewport>
</template>

<script>
import { mapState, mapGetters, mapMutations } from "vuex";
import { point } from "@turf/helpers";
import bbox from "@turf/bbox";
import bboxPolygon from "@turf/bbox-polygon";
import buffer from "@turf/buffer";
import distance from "@turf/distance";

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
      editing: false,
      annotations: [],
      filteringGeometry: null
    };
  },
  computed: {
    ...mapState(["selectedDataset", "workspaces", "focusedWorkspaceKey"]),
    ...mapGetters(["selectedDatasetPoint", "focusedWorkspace"])
  },
  asyncComputed: {
    async filteredDatasetIds() {
      if (this.filteringGeometry) {
        var { data: datasets } = await this.$girder.get("item/geometa", {
          params: {
            geojson: this.filteringGeometry,
            relation: "within"
          }
        });
        return datasets.map(dataset => dataset._id);
      } else {
        return null;
      }
    }
  },
  watch: {
    annotations([annotation]) {
      if (annotation && annotation.geojson()) {
        this.filteringGeometry = annotation.geojson().geometry;
        this.annotations = [];
      }
    }
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
    zoomToDataset(dataset) {
      var geojsViewport = this.$refs.geojsMapViewport
        ? this.$refs.geojsMapViewport[0]
        : null;
      if (!geojsViewport) {
        return;
      }
      var datasetBBox = bbox(dataset.geometa.bounds);
      var dist = distance(
        point([datasetBBox[0], datasetBBox[1]]),
        point([datasetBBox[2], datasetBBox[3]])
      );
      var bufferedBbox = bbox(buffer(bboxPolygon(datasetBBox), dist / 4));

      var zoomAndCenter = geojsViewport.$geojsMap.zoomAndCenterFromBounds({
        left: bufferedBbox[0],
        right: bufferedBbox[2],
        top: bufferedBbox[3],
        bottom: bufferedBbox[1]
      });
      this.viewport.center = zoomAndCenter.center;
      this.viewport.zoom = zoomAndCenter.zoom;
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
