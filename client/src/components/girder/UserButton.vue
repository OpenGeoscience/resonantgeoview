<script>
export default {
  name: "UserButton",
  inject: ["girderRest"],
  computed: {
    initials() {
      const first = this.girderRest.user.firstName;
      const last = this.girderRest.user.lastName;
      return (
        first.charAt(0).toLocaleUpperCase() + last.charAt(0).toLocaleUpperCase()
      );
    }
  }
};
</script>

<template>
  <span>
    <v-btn
      v-if="girderRest.user"
      icon
      color="grey lighten-1"
      class="avatar-btn"
      @click="$emit('user', girderRest.user)"
    >
      <v-avatar>
        {{ initials }}
      </v-avatar>
    </v-btn>
    <v-btn v-else flat @click="$emit('login')">
      Login
    </v-btn>
  </span>
</template>

<style lang="scss" scoped>
</style>
