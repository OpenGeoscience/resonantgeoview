<template>
<v-app>
  <AppToolbar
  title='ResonantGeoView'
  :panelButton="true"
  @click-panel="toggleSidePanel">
    <template slot="right">
      <UserButton
        @user="girderRest.logout()" />
    </template>
  </AppToolbar>

  <transition name="fade" mode='out-in'>
    <router-view></router-view>
  </transition>
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
import { mapMutations } from "vuex";

import UserButton from "./components/girder/UserButton";
import "./transitions.scss";

export default {
  name: "App",
  components: { Prompt, UserButton },
  inject: ["girderRest"],
  data() {
    return {};
  },
  methods: {
    ...mapMutations(["toggleSidePanel"])
  }
};
</script>
