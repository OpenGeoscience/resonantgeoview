import Vue from 'vue';
import ResonantGeo from 'resonantgeo/src';
import Girder, { RestClient } from '@girder/components/src';
import { API_URL } from './constants';
import AsyncComputed from 'vue-async-computed';
import '@fortawesome/fontawesome-free/css/all.css';

import App from './App.vue';
import router from './router';
import store from './store';
import girder from './girder';

Vue.use(AsyncComputed);
Vue.use(Girder);

girder.rest = new RestClient({ apiRoot: API_URL });
Vue.use(ResonantGeo, {
  girder: girder.rest,
});
girder.rest.fetchUser().then(() => {
  new Vue({
    router,
    store,
    render: h => h(App),
    provide: { girderRest: girder.rest },
  }).$mount('#app');
});
