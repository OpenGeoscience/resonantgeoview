<template>
  <FullScreenViewport>
    <WorkspaceContainer
      :focused="focusedWorkspace"
      @update:focused="setFocusedWorkspaceKey($event)"
      :autoResize="true"
      :max="2">
      <Workspace
        v-for="(workspace, key) in workspaces"
        :key="key"
        :identifier="key"
        @split="addWorkspace()"
        @close="removeWorkspace(key)">
        <template slot='actions'>
          <WorkspaceAction>
            <v-icon @click="takeScreenshot(key)">camera_alt</v-icon>
          </WorkspaceAction>
        </template>
        <GeojsMapViewport
          class='map'
          :viewport='viewport'
          :ref='`geojsMapViewport${key}`'>
          <AdaptedColorLegendLayer
            :layers="workspace.layers"
            :datasetIdMetaMap="datasetIdMetaMap" />
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
              :geojson="datasetIdMetaMap[layer.dataset._id].geojson"
              :summary="datasetIdMetaMap[layer.dataset._id].summary"
              :zIndex="workspace.layers.length-i"
              :opacity='layer.opacity'
              @click='layerClicked(layer, $event)'>
            </GeojsGeojsonDatasetLayer>
            <StyledGeoTIFFLayer
              v-if="layer.dataset.geometa.driver==='GeoTIFF'"
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :tileURL="getTileURL(layer.dataset)"
              :opacity="layer.opacity"
              :keepLower="false"
              :zIndex="workspace.layers.length-i"
              @click='layerClicked(layer, $event)'>
            </StyledGeoTIFFLayer>
            <WMSLayer
              v-if="layer.dataset.geometa.driver==='WMS'"
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :opacity="layer.opacity"
              :zIndex="workspace.layers.length-i"
              @click='layerClicked(layer, $event)'>
            </WMSLayer>
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
    :expanded="sidePanelExpanded"
    :bottom="0"
    :footer="false">
      <template slot="toolbar">
        <v-toolbar flat>
          <v-btn icon class="hidden-xs-only" v-if="customVizDataset" @click="returnFromCustomViz">
            <v-icon>arrow_back</v-icon>
          </v-btn>
          <v-toolbar-title>{{!customVizDataset?"Datasets":"Customize"}}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu offset-y>
            <v-btn
              slot="activator"
              icon>
              <v-icon>more_vert</v-icon>
            </v-btn>
            <v-list>
              <v-list-tile
                @click="uploadDialog=true">
                <v-list-tile-content>
                  <v-list-tile-title>Upload</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-divider />
              <v-list-tile
                @click="addWMSDialog=true">
                <v-list-tile-content>
                  <v-list-tile-title>Add WMS dataset</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-toolbar>
      </template>
      <template slot="actions">
        <SidePanelAction @click="drawing = 'rectangle'">
          <v-icon>aspect_ratio</v-icon>
        </SidePanelAction>
      </template>
      <div class="main">
        <transition name="slide-fade" mode="out-in">
          <div v-if="!customVizDataset" class="datasets-layers-pane" key="datasets">
            <transition name="fade">
              <div v-if="filteredDatasetIds">
                <v-switch hide-details label="Filtering" :input-value="!!filteringGeometry" @change="filteringGeometry=null" class="mt-0 mx-1"></v-switch>
              </div>
            </transition>
            <DatasetModule class="datasets"
              :filteredDatasetIds="filteredDatasetIds" />
            <LayerModule class="layers" 
              v-if="focusedWorkspace &&focusedWorkspace.layers.length"
              @zoomToDataset="zoomToDataset"
              @customDataset="customVizDataset=$event" />
          </div>
          <VectorCustomVizPane
            v-if="customVizDataset && customVizDataset.geometa.driver === 'GeoJSON'"
            :dataset="customVizDataset"
            :summary="datasetIdMetaMap[customVizDataset._id].summary"
            :preserve.sync="preserveCustomViz"
            />
          <GeotiffCustomVizPane
            v-if="customVizDataset && customVizDataset.geometa.driver === 'GeoTIFF'"
            :dataset="customVizDataset"
            :meta="datasetIdMetaMap[customVizDataset._id]"
            :preserve.sync="preserveCustomViz"
            />
        </transition>
      </div>
    </SidePanel>
    <MapScreenshotDialog
      v-model="mapScreenshotDialog"
      :map="screenshotMap" />
    <ClickInfoDialog
      right="15px"
      bottom="60px"
      :datasetClickEvents="datasetClickEvents" />
    <v-dialog v-model="uploadDialog" scrollable max-width="250px">
      <GirderUpload v-if="datasetFolder"
      :dest="datasetFolder"
      @done="loadDatasets();uploadDialog=false;" />
    </v-dialog>
    <AddWMSDatasetDialog v-model="addWMSDialog" @dataset="createWMSdataset" />
  </FullScreenViewport>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import { stringify } from "qs";
import { point } from "@turf/helpers";
import bbox from "@turf/bbox";
import bboxPolygon from "@turf/bbox-polygon";
import buffer from "@turf/buffer";
import distance from "@turf/distance";
import debounce from "lodash-es/debounce";
import { Upload as GirderUpload } from "@girder/components/src/components";

import { API_URL } from "../constants";
import WorkspaceContainer from "../components/Workspace/Container";
import Workspace from "../components/Workspace/Workspace";
import WorkspaceAction from "../components/Workspace/Action";
import DatasetModule from "./DatasetModule";
import LayerModule from "./LayerModule";
import GeojsGeojsonDatasetLayer from "../components/geojs/GeojsGeojsonDatasetLayer";
import StyledGeoTIFFLayer from "../components/geojs/StyledGeoTIFFLayer";
import AdaptedColorLegendLayer from "../components/geojs/AdaptedColorLegendLayer";
import WMSLayer from "../components/geojs/WMSLayer";
import VectorCustomVizPane from "../components/VectorCustomVizPane/VectorCustomVizPane";
import GeotiffCustomVizPane from "../components/GeotiffCustomVizPane";
import saveDatasetMetadata from "../utils/saveDatasetMetadata";
import MapScreenshotDialog from "./MapScreenshotDialog";
import ClickInfoDialog from "./ClickInfoDialog";
import AddWMSDatasetDialog from "../components/AddWMSDatasetDialog";

export default {
  name: "Explore",
  components: {
    DatasetModule,
    LayerModule,
    WorkspaceContainer,
    Workspace,
    WorkspaceAction,
    GeojsGeojsonDatasetLayer,
    StyledGeoTIFFLayer,
    AdaptedColorLegendLayer,
    WMSLayer,
    VectorCustomVizPane,
    GeotiffCustomVizPane,
    MapScreenshotDialog,
    ClickInfoDialog,
    AddWMSDatasetDialog,
    GirderUpload
  },
  inject: ["girderRest"],
  data() {
    return {
      viewport: {
        center: [-100, 30],
        zoom: 4
      },
      drawing: false,
      editing: false,
      annotations: [],
      filteringGeometry: null,
      customVizDataset: null,
      preserveCustomViz: false,
      screenshotMap: null,
      datasetClickEvents: [],
      uploadDialog: false,
      addWMSDialog: false
    };
  },
  computed: {
    mapScreenshotDialog: {
      get() {
        return !!this.screenshotMap;
      },
      set(value) {
        if (!value) {
          this.screenshotMap = null;
        }
      }
    },
    ...mapState([
      "sidePanelExpanded",
      "datasetIdMetaMap",
      "selectedDataset",
      "workspaces",
      "focusedWorkspaceKey",
      "datasetFolder"
    ]),
    ...mapGetters(["selectedDatasetPoint", "focusedWorkspace"])
  },
  asyncComputed: {
    async filteredDatasetIds() {
      if (this.filteringGeometry) {
        var { data: datasets } = await this.girderRest.get("item/geometa", {
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
    },
    "girderRest.user"(user) {
      if (!user) {
        this.$router.push("/login");
      }
    }
  },
  created() {
    this.debounceSetdatasetClickEvents = debounce(() => {
      this.datasetClickEvents = this.datasetClickEventsAggregator;
      this.datasetClickEventsAggregator = [];
    }, 0);
    this.datasetClickEventsAggregator = [];
    this.loadDatasets();
    this.loadGroups();
    this.setDatasetFolder();
  },
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
      var map = this.$refs[`geojsMapViewport${this.focusedWorkspaceKey}`][0]
        .$geojsMap;
      if (!map) {
        return;
      }
      var datasetBBox = bbox(dataset.geometa.bounds);
      var dist = distance(
        point([datasetBBox[0], datasetBBox[1]]),
        point([datasetBBox[2], datasetBBox[3]])
      );
      var bufferedBbox = bbox(buffer(bboxPolygon(datasetBBox), dist / 4));

      var zoomAndCenter = map.zoomAndCenterFromBounds({
        left: bufferedBbox[0],
        right: bufferedBbox[2],
        top: bufferedBbox[3],
        bottom: bufferedBbox[1]
      });
      this.viewport.center = zoomAndCenter.center;
      this.viewport.zoom = zoomAndCenter.zoom;
    },
    returnFromCustomViz() {
      if (this.preserveCustomViz) {
        this.preserveCustomViz = false;
        saveDatasetMetadata(this.customVizDataset);
      }
      this.customVizDataset = null;
    },
    takeScreenshot(key) {
      var map = this.$refs[`geojsMapViewport${key}`][0].$geojsMap;
      this.screenshotMap = map;
      this.mapScreenshotDialog = true;
    },
    layerClicked(layer, clickEvent) {
      if (layer.opacity) {
        this.datasetClickEventsAggregator.push({
          dataset: layer.dataset,
          clickEvent: clickEvent
        });
        this.debounceSetdatasetClickEvents();
      }
    },
    async createWMSdataset({ name, geometa }) {
      var { data: item } = await this.girderRest.post(
        "/item",
        stringify({
          name,
          folderId: this.datasetFolder._id
        })
      );
      console.log(geometa);
      var { data: item } = await this.girderRest.put(
        `/item/${item._id}/geometa`,
        stringify({
          geometa: JSON.stringify(geometa)
        })
      );
      this.loadDatasets();
    },
    ...mapMutations([
      "addWorkspace",
      "removeWorkspace",
      "setFocusedWorkspaceKey"
    ]),
    ...mapActions(["loadDatasets", "loadGroups", "setDatasetFolder"])
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

    .datasets-layers-pane {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
  }
}
</style>
