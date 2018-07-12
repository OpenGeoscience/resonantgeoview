<template>
<v-app>
    <AppToolbar
    title='Minerva'
    :userIcon='userIcon'
    @click-user='loginDialog = true' />

    <transition name="fade" mode='out-in'>
      <router-view></router-view>
    </transition>

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
import "danesfield-client/src/transitions.scss";

import Prompt from "./components/prompt/Prompt";

export default {
  name: "App",
  components: { Prompt },
  data() {
    return {
      title: "Minerva",
      tabs: [
        {
          title: "Explore",
          route: "/",
          icon: "explore"
        }
      ],
      userIcon: "account_circle",
      loginDialog: false,
      login: {
        email: "",
        password: "",
        rules: [v => !!v || "Field is required"]
      }
    };
  },
  methods: {
    submitLogin() {
      if (this.$refs.login.validate()) {
        console.log(`logged in as ${this.login.email}`);
        this.loginDialog = false;
      }
    }
  }
};
</script>
