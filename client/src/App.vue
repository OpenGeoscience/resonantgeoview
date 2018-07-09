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

/* transtion */

/* fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* slide */
.slide-fade-enter-active {
  transition: all 0.15s ease;
}
.slide-fade-leave-active {
  transition: all 0.15s ease;
}
.slide-fade-enter {
  transform: translateX(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}

/* fade-group */
.fade-group-enter,
.fade-group-leave-to {
  opacity: 0;
}

.fade-group-enter-active,
.fade-group-leave-active {
  transition: opacity 0.15s;
}

.fade-group-leave-active {
  position: absolute;
}
.fade-group-move {
  transition: transform 0.15s;
}

/* overwrite */
.btn {
  min-width: 0;
}
</style>

<script>
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
