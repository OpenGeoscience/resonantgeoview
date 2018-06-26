import Vue from 'vue'
import Router from 'vue-router'
import Explore from './views/Explore.vue'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'explore',
    component: Explore
  }]
})
