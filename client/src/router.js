import Vue from "vue";
import Router from "vue-router";

import Explore from "./views/Explore.vue";
import girder from "./girder";
import Login from "./views/Login.vue";

Vue.use(Router);

function beforeEnter(to, from, next) {
  if (!girder.rest.user) {
    next("/login");
  } else {
    next();
  }
}

export default new Router({
  routes: [
    {
      path: "/",
      name: "explore",
      component: Explore,
      beforeEnter
    },
    {
      path: "/login",
      name: "login",
      component: Login
    },
    {
      path: "*",
      redirect: "/"
    }
  ]
});
