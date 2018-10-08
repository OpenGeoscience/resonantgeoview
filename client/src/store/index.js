import Vue from 'vue';
import Vuex from 'vuex';
import pointOnFeature from '@turf/point-on-feature';
import bbox from "@turf/bbox";
import bboxPolygon from "@turf/bbox-polygon";

import girder from '../girder';
import { remove } from '../utils/array';
import prompt from '../components/prompt/module';
import loadDatasets from '../utils/loadDataset';
import loadDatasetData from "../utils/loadDatasetData";
import { summarize, normalize } from "../utils/geojsonUtil";
import { getDefaultGeojsonVizProperties } from "../utils/getDefaultGeojsonVizProperties";
import getLargeImageMeta from "../utils/getLargeImageMeta";

Vue.use(Vuex);

export default new Vuex.Store({
  strict: false,
  state: {
    sidePanelExpanded: true,
    datasets: [],
    datasetIdMetaMap: {},
    datasetSortBy: 'type',
    groups: [],
    selectedDataset: null,
    workspaces: {
      '0': {
        layers: []
      }
    },
    focusedWorkspaceKey: '0',
    datasetFolder: null
  },
  mutations: {
    toggleSidePanel(state) {
      state.sidePanelExpanded = !state.sidePanelExpanded;
    },
    setDatasets(state, datasets) {
      datasets.forEach((dataset) => {
        switch (dataset.geometa.driver) {
          case "GeoJSON":
            if (!dataset.meta || !dataset.meta.vizProperties) {
              Object.assign(dataset, { meta: { vizProperties: getDefaultGeojsonVizProperties() } });
            }
            break;
          case "GeoTIFF":
            if (!dataset.meta) {
              dataset.meta = {};
            }
            break;
        }
      });
      state.datasets = datasets;
    },
    addAdhocGeojsonDataset(state, { name, geojson }) {
      var dataset = {
        _id: 'adhoc_' + Math.random().toString(36).substring(7),
        name,
        geometa: {
          type_: 'vector',
          driver: 'GeoJSON',
          bounds: bboxPolygon(bbox(geojson)).geometry
        },
        meta: {
          vizProperties: getDefaultGeojsonVizProperties()
        }
      };
      geojson = normalize(geojson);
      var summary = summarize(geojson);
      Vue.set(state.datasetIdMetaMap, dataset._id, { geojson, summary });
      state.datasets.push(dataset);
    },
    setSelectedDataset(state, dataset) {
      state.selectedDataset = dataset;
    },
    addWorkspace(state) {
      Vue.set(state.workspaces, Math.random().toString(36).substring(7), {
        layers: []
      })
    },
    removeWorkspace(state, key) {
      Vue.delete(state.workspaces, key);
    },
    setFocusedWorkspaceKey(state, key) {
      state.focusedWorkspaceKey = key;
    },
    _addDatasetToWorkspace(state, { dataset, workspace }) {
      workspace.layers.push({ dataset, opacity: 1 });
    },
    removeDatasetFromWorkspace(state, { dataset, workspace }) {
      workspace.layers.splice(workspace.layers.map(layers => layers.dataset).indexOf(dataset), 1);
    },
    setWorkspaceLayers(state, { workspace, layers }) {
      workspace.layers = layers;
    },
    setWorkspaceLayerOpacity(state, { layer, opacity }) {
      layer.opacity = opacity;
    },
    setGroup(state, groups) {
      state.groups = groups;
    },
    addGroup(state, group) {
      state.groups.push(group);
    },
    removeGroup(state, group) {
      remove(state.groups, group);
    },
    addDatasetToGroup(state, { group, dataset }) {
      remove(group.datasetIds, dataset._id);
      group.datasetIds.push(dataset._id);
    },
    removeDatasetFromGroup(state, { group, dataset }) {
      remove(group.datasetIds, dataset._id);
    }
  },
  actions: {
    async loadDatasets({ commit }) {
      commit('setDatasets', await loadDatasets());
    },
    async loadGroups({ commit }) {
      commit('setGroup', (await girder.rest.get('dataset_group')).data);
    },
    async createGroup({ commit }, name) {
      commit('addGroup', (await girder.rest.post('dataset_group', { name, datasetIds: [] })).data);
    },
    async deleteGroup({ commit }, group) {
      await girder.rest.delete(`dataset_group/${group._id}`);
      commit('removeGroup', group);
    },
    async addDatasetToGroup({ state, commit }, { group, dataset }) {
      commit('addDatasetToGroup', { group, dataset });
      return girder.rest.put(`dataset_group/${group._id}`, group);
    },
    async removeDatasetFromGroup({ state, commit }, { group, dataset }) {
      commit('removeDatasetFromGroup', { group, dataset });
      return girder.rest.put(`dataset_group/${group._id}`, group);
    },
    async addDatasetToWorkspace({ state, commit }, { dataset, workspace }) {
      if (!(dataset._id in state.datasetIdMetaMap)) {
        Vue.set(state.datasetIdMetaMap, dataset._id, await getDatasetMeta(dataset, state.datasetIdMetaMap));
      }
      workspace.layers.push({ dataset, opacity: 1 });
    },
    async setDatasetFolder({ state, commit }) {
      var { data: folder } = await girder.rest.get('dataset/folder');
      state.datasetFolder = folder;
    },
    async deleteDataset({ state }, dataset) {
      await girder.rest.delete(`item/${dataset._id}`);
      remove(state.datasets, dataset);
    },
  },
  getters: {
    focusedWorkspace(state) {
      return state.workspaces[state.focusedWorkspaceKey];
    },
    selectedDatasetPoint(state) {
      if (!state.selectedDataset) {
        return null;
      }
      return pointOnFeature(state.selectedDataset.geometa.bounds).geometry;
    }
  },
  modules: {
    prompt
  }
});


async function getDatasetMeta(dataset) {
  switch (dataset.geometa.driver) {
    case "GeoJSON":
      var geojson = normalize(await loadDatasetData(dataset));
      var summary = summarize(geojson);
      return { geojson, summary };
      break;
    case "GeoTIFF":
      return await getLargeImageMeta(dataset);
      break;
    default:
      return null;
  }
}
