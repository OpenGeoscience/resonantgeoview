<template>
  <v-app>
    <router-view></router-view>
    <Prompt />
  </v-app>
</template>

<style lang="scss">
/* global */
html,
body,
.application,
.application--wrap {
  height: 100vh;
  overflow: hidden;
}

.v-list .selected .v-list__tile {
  background: rgba(103, 103, 103, 0.2) !important;
}

/* overwrite */
.btn {
  min-width: 0;
}

.v-toolbar {
  // This is a wierd fix needed for the login label
  button .v-btn__content {
    height: inherit;
  }
}
</style>

<script>
import Prompt from "./components/prompt/Prompt";

import "./transitions.scss";

export default {
  name: "App",
  components: { Prompt },
  inject: ["girderRest"],
  data() {
    return {};
  }
};
</script>
