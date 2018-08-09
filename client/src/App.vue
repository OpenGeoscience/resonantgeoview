<template>
<v-app>
    <AppToolbar
    title='Minerva'>
      <template slot="right">
        <GirderUserButton 
          @login="userForm='login';userDialog=true;"
          @user="userForm='logout';userDialog=true;" />
      </template>
    </AppToolbar>

    <transition name="fade" mode='out-in'>
      <router-view></router-view>
    </transition>

    <GirderUserDialog
      :form.sync='userForm'
      v-model='userDialog'
      />

    <Prompt />
</v-app>
</template>

<style>
/* global */
html,
body,
.application,
.application--wrap {
  height: 100vh;
  overflow: hidden;
}

/* overwrite */
.btn {
  min-width: 0;
}
</style>

<script>
import "./transitions.scss";

import Prompt from "./components/prompt/Prompt";

export default {
  name: "App",
  components: { Prompt },
  data() {
    return {
      title: "Minerva",
      userForm: "login",
      userDialog: false
    };
  },
  methods: {}
};
</script>
