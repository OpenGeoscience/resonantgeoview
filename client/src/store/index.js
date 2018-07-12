import Vue from 'vue';
import Vuex from 'vuex';
import pointOnFeature from '@turf/point-on-feature';

import girder from '../girder';
import { remove } from '../utils/array';
import prompt from '../components/prompt/module';
import loadDatasets from '../utils/loadDataset';

Vue.use(Vuex);

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  state: {
    datasets: [],
    datasetSortBy: 'type',
    groups: [],
    selectedDataset: null,
    workspaces: {
      '0': {
        layers: []
      }
    },
    focusedWorkspaceKey: '0'
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
        layers: []
      })
    },
    removeWorkspace(state, key) {
      Vue.delete(state.workspaces, key);
    },
    setFocusedWorkspaceKey(state, key) {
      state.focusedWorkspaceKey = key;
    },
    addDatasetToWorkspace(state, { dataset, workspace }) {
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
    },
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
      return pointOnFeature(state.selectedDataset.geometa.bounds).geometry;
    }
  },
  modules: {
    prompt
  }
});
