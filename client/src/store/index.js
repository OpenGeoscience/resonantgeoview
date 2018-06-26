import Vue from 'vue';
import Vuex from 'vuex';
import pointOnFeature from '@turf/point-on-feature';

import prompt from "../components/prompt/module";
import loadDatasets from '../utils/loadDataset';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    datasets: [],
    datasetSortBy: 'type',
    selectedDataset: null,
    workspaces: {
      "0": {
        datasets: []
      }
    },
    focusedWorkspaceKey: "0"
  },
  mutations: {
    setDatasets(state, datasets) {
      state.datasets = datasets;
    },
    setSelectedDataset(state, dataset) {
      state.selectedDataset = dataset;
    },
    addWorkspace(state) {
      Vue.set(state.workspaces, Math.random().toString(36).substring(7), {
        datasets: []
      })
    },
    removeWorkspace(state, key) {
      Vue.delete(state.workspaces, key);
    },
    setFocusedWorkspaceKey(state, key) {
      state.focusedWorkspaceKey = key;
    },
    addDatasetToWorkspace(state, { dataset, workspace }) {
      workspace.datasets.push(dataset);
    },
    removeDatasetFromWorkspace(state, { dataset, workspace }) {
      workspace.datasets.splice(workspace.datasets.indexOf(dataset), 1);
    }
  },
  actions: {
    async loadDatasets({ commit }) {
      commit('setDatasets', await loadDatasets());
    }
  },
  getters: {
    focusedWorkspace(state) {
      return state.workspaces[state.focusedWorkspaceKey];
    },
    selectedDatasetPoint(state) {
      if (!state.selectedDataset) {
        return null;
      }
      var point = pointOnFeature(state.selectedDataset.geometa.bounds);
      return {
        _id: state.selectedDataset._id,
        name: state.selectedDataset.name,
        x: point.geometry.coordinates[0],
        y: point.geometry.coordinates[1]
      }
    }
  },
  modules: {
    prompt
  }
});
