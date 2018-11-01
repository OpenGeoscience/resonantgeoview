import Vue from 'vue';
import ResonantGeo from 'resonantgeo/src';
import Girder, { RestClient } from '@girder/components/src';
import NotificationBus from '@girder/components/src/utils/notifications';
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
var notificationBus = new NotificationBus(girder.rest, { useEventSource: true });
notificationBus.connect();
// A hack when transitioning from resonantgeo to girder_web_component
girder.rest.sse = notificationBus;
Vue.use(ResonantGeo, {
  girder: girder.rest,
});
girder.rest.fetchUser().then(() => {
  new Vue({
    router,
    store,
    render: h => h(App),
    provide: { girderRest: girder.rest, notificationBus },
  }).$mount('#app');
});
