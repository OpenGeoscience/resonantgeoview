import Vue from 'vue';
import ResonantGeo from 'resonantgeo/src';
import { Session } from 'resonantgeo/src/rest';
import { API_URL } from './constants';
import eventstream from './utils/eventstream';
import AsyncComputed from 'vue-async-computed';
import '@fortawesome/fontawesome-free/css/all.css';

import App from './App.vue';
import router from './router';
import store from './store';
import girder from './girder';


Vue.use(AsyncComputed);

eventstream.open();
girder.rest = new Session({ apiRoot: API_URL });
Vue.use(ResonantGeo, {
  girder: girder.rest,
});
girder.rest.$refresh().then(() => {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app');
});
