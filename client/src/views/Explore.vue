<template>
  <FullScreenViewport>
    <AppToolbar
      title="ResonantGeoView"
      :panelButton="true"
      @click-panel="sidePanelExpanded = !sidePanelExpanded"
    >
      <template slot="right">
        <UserButton @user="girderRest.logout()" />
      </template>
    </AppToolbar>

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
        @split="addWorkspace(workspace.type)"
        @close="removeWorkspace(key)"
      >
        <template slot="actions">
          <WorkspaceAction v-if="workspace.type === 'geojs'">
            <v-icon @click="takeScreenshot(key)">camera_alt</v-icon>
          </WorkspaceAction>
          <WorkspaceAction v-if="workspace.type === 'vtk'">
            <v-menu top offset-y origin="center center">
              <v-icon slot="activator">palette</v-icon>
              <v-card width="130px">
                <Palette
                  :value="workspace.vtkBGColor"
                  @input="workspace.vtkBGColor = $event"
                />
              </v-card>
            </v-menu>
          </WorkspaceAction>
        </template>
        <GeojsMapViewport
          class="map"
          v-if="workspace.type === 'geojs'"
          :viewport="viewport"
          :ref="`geojsMapViewport${key}`"
        >
          <AdaptedColorLegendLayer
            :layers="workspace.layers"
            :datasetIdMetaMap="datasetIdMetaMap"
          />
          <GeojsTileLayer
            url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors, © CARTO"
            :zIndex="0"
          >
          </GeojsTileLayer>
          <template v-for="(layer, i) in workspace.layers">
            <GeojsGeojsonDatasetLayer
              v-if="getDatasetDriver(layer.dataset) === 'GeoJSON'"
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :geojson="datasetIdMetaMap[layer.dataset._id].geojson"
              :summary="datasetIdMetaMap[layer.dataset._id].summary"
              :zIndex="workspace.layers.length - i"
              :opacity="layer.opacity"
              @click="layerClicked(layer, $event)"
            >
            </GeojsGeojsonDatasetLayer>
            <StyledGeoTIFFLayer
              v-if="getDatasetDriver(layer.dataset) === 'GeoTIFF'"
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :tileURL="getTileURL(layer.dataset)"
              :opacity="layer.opacity"
              :keepLower="false"
              :zIndex="workspace.layers.length - i"
              @click="layerClicked(layer, $event)"
            >
            </StyledGeoTIFFLayer>
            <StyledGeoTIFFLayer
              v-if="
                getDatasetDriver(layer.dataset) === 'Network Common Data Format'
              "
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :tileURL="getTileURL(layer.dataset)"
              :opacity="layer.opacity"
              :keepLower="false"
              :zIndex="workspace.layers.length - i"
              @click="layerClicked(layer, $event)"
            >
            </StyledGeoTIFFLayer>
            <WMSLayer
              v-if="getDatasetDriver(layer.dataset) === 'WMS'"
              :key="layer.dataset._id"
              :dataset="layer.dataset"
              :opacity="layer.opacity"
              :zIndex="workspace.layers.length - i"
              @click="layerClicked(layer, $event)"
            >
            </WMSLayer>
          </template>
          <GeojsAnnotationLayer
            :drawing.sync="drawing"
            :editing.sync="editing"
            :editable="true"
            :annotations="annotations"
            @update:annotations="annotations = $event"
            :zIndex="workspace.layers.length + 1"
          >
          </GeojsAnnotationLayer>
          <GeojsGeojsonLayer
            v-if="filteringGeometry"
            :geojson="filteringGeometry"
            :featureStyle="{
              polygon: {
                strokeColor: 'grey',
                strokeWidth: 1,
                fillColor: '#1976d2',
                fillOpacity: 0.3
              }
            }"
            :zIndex="workspace.layers.length + 2"
          >
          </GeojsGeojsonLayer>
          <template v-if="selectedDatasetPoint && focusedWorkspaceKey === key">
            <GeojsGeojsonLayer
              :geojson="selectedDatasetPoint"
              :featureStyle="{
                point: { strokeColor: 'black', strokeWidth: 2, radius: 3 }
              }"
              :zIndex="workspace.layers.length + 3"
            >
            </GeojsGeojsonLayer>
            <GeojsWidgetLayer
              :position="selectedDatasetPoint.coordinates"
              :offset="{ x: 0, y: -20 }"
              :zIndex="workspace.layers.length + 4"
            >
              <v-chip small color="green" text-color="white">{{
                selectedDataset.name
              }}</v-chip>
            </GeojsWidgetLayer>
          </template>
        </GeojsMapViewport>
        <VTKViewport
          v-if="workspace.type === 'vtk'"
          :background="workspace.vtkBGColor"
        >
          <OBJMultiItemActor
            v-for="layer in workspace.layers"
            :key="layer.dataset._id"
            :item="layer.dataset"
          />
        </VTKViewport>
      </Workspace>
    </WorkspaceContainer>
    <VNavigationDrawer
      app
      clipped
      class="side-panel"
      v-model="sidePanelExpanded"
    >
      <v-toolbar flat>
        <v-btn
          icon
          class="hidden-xs-only"
          v-if="customVizDataset"
          @click="returnFromCustomViz"
        >
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <v-toolbar-title>{{
          !customVizDataset ? "Datasets" : "Customize"
        }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu lazy offset-y>
          <v-btn slot="activator" icon>
            <v-icon>more_vert</v-icon>
          </v-btn>
          <v-list>
            <v-list-tile @click="uploadDialog = true">
              <v-list-tile-content>
                <v-list-tile-title>Upload</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile @click="addWMSDialog = true">
              <v-list-tile-content>
                <v-list-tile-title>Add WMS dataset</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-divider />
            <v-list-tile @click="jobsDialog = true">
              <v-list-tile-content>
                <v-list-tile-title>Jobs</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-menu>
      </v-toolbar>
      <v-container class="action-buttons pa-0">
        <SidePanelAction
          @click="drawing = 'rectangle'"
          v-if="focusedWorkspace && focusedWorkspace.type === 'geojs'"
        >
          <v-icon>aspect_ratio</v-icon>
        </SidePanelAction>
        <SidePanelAction @click="processingDialog = true">
          <v-icon>fa-cogs</v-icon>
        </SidePanelAction>
      </v-container>
      <div class="main">
        <transition name="slide-fade" mode="out-in">
          <div
            v-if="!customVizDataset"
            class="datasets-layers-pane"
            key="datasets"
          >
            <transition name="fade">
              <div v-if="filteredDatasetIds">
                <v-switch
                  hide-details
                  label="Filtering"
                  :input-value="!!filteringGeometry"
                  @change="filteringGeometry = null"
                  class="mt-0 mx-1"
                ></v-switch>
              </div>
            </transition>
            <DatasetModule
              class="datasets"
              :filteredDatasetIds="filteredDatasetIds"
            />
            <LayerModule
              class="layers"
              v-if="focusedWorkspace && focusedWorkspace.layers.length"
              @zoomToDataset="zoomToDataset"
              @customDataset="customVizDataset = $event"
            />
          </div>
          <VectorCustomVizPane
            v-if="
              customVizDataset &&
                getDatasetDriver(customVizDataset) === 'GeoJSON'
            "
            :dataset="customVizDataset"
            :summary="datasetIdMetaMap[customVizDataset._id].summary"
            :preserve.sync="preserveCustomViz"
          />
          <GeotiffCustomVizPane
            v-if="
              customVizDataset &&
                getDatasetDriver(customVizDataset) === 'GeoTIFF'
            "
            :dataset="customVizDataset"
            :meta="datasetIdMetaMap[customVizDataset._id]"
            :preserve.sync="preserveCustomViz"
          />
          <GeotiffCustomVizPane
            v-if="
              customVizDataset &&
                getDatasetDriver(customVizDataset) ===
                  'Network Common Data Format'
            "
            :dataset="customVizDataset"
            :meta="datasetIdMetaMap[customVizDataset._id]"
            :preserve.sync="preserveCustomViz"
          />
        </transition>
      </div>
    </VNavigationDrawer>
    <v-dialog v-model="uploadDialog" scrollable max-width="400px" lazy>
      <GirderUpload
        v-if="datasetFolder"
        :dest="datasetFolder"
        @done="
          loadDatasets();
          uploadDialog = false;
        "
      />
    </v-dialog>
    <MapScreenshotDialog v-model="mapScreenshotDialog" :map="screenshotMap" />
    <ClickInfoDialog
      right="15px"
      bottom="60px"
      :datasetClickEvents="datasetClickEvents"
    />
    <AddWMSDatasetDialog
      v-model="addWMSDialog"
      @dataset="createDatasetWithGeometa"
    />
    <GaiaProcessingDialog
      v-if="datasetFolder"
      :dest="datasetFolder"
      v-model="processingDialog"
    />
    <JobsDialog v-model="jobsDialog" />
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
import UserButton from "../components/girder/UserButton";
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
import GaiaProcessingDialog from "./GaiaProcessingDialog";
import JobsDialog from "../components/girder/JobsDialog";
// import ResizableVNavigationDrawer from "../components/ResizableVNavigationDrawer";
import getDatasetDriver from "../utils/getDatasetDriver";
import VTKViewport from "../components/vtk/VTKViewport";
import OBJMultiItemActor from "../components/vtk/OBJMultiItemActor";
import Palette from "../components/vtk/Palette";

export default {
  name: "Explore",
  components: {
    UserButton,
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
    GirderUpload,
    MapScreenshotDialog,
    ClickInfoDialog,
    AddWMSDatasetDialog,
    GaiaProcessingDialog,
    JobsDialog,
    VTKViewport,
    OBJMultiItemActor,
    Palette
  },
  inject: ["girderRest", "notificationBus"],
  data() {
    return {
      getDatasetDriver,
      sidePanelExpanded: true,
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
      jobsDialog: false,
      addWMSDialog: false,
      processingDialog: false
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
    this.notificationBus.$on("message:job_status", this.jobStatusChange);
  },
  beforeDestroy() {
    this.notificationBus.$off("message:job_status", this.jobStatusChange);
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
    async createDatasetWithGeometa({ name, geometa }) {
      var { data: item } = await this.girderRest.post(
        "/item",
        stringify({
          name,
          folderId: this.datasetFolder._id
        })
      );
      await this.girderRest.put(
        `/item/${item._id}/geometa`,
        stringify({
          geometa: JSON.stringify(geometa)
        })
      );
      this.loadDatasets();
    },
    jobStatusChange(e) {
      if (e.data.status === 3) {
        this.loadDatasets();
      }
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
  overflow: visible;

  .action-buttons {
    position: fixed;
    top: 64px;
    width: 50px;
    right: -50px;
  }

  .main {
    flex: 1;
    display: flex;
    flex-direction: column;

    .datasets-layers-pane {
      flex: 1;
      display: flex;
      flex-direction: column;

      .datasets {
        overflow-y: auto;
      }

      .layers {
        flex: 1;
      }
    }
  }
}
</style>
