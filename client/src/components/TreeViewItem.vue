<template>
  <li class="my-1 mx-3">
    <div class="list-item-title subheading" @click="toggle">
      <span>{{ model.name }}</span>
      <v-spacer></v-spacer>
      <v-icon v-if="isFolder">{{
        open ? "expand_less" : "expand_more"
      }}</v-icon>
    </div>
    <v-slide-y-transition>
      <ul class="sub-items ml-2" v-show="open" v-if="isFolder">
        <TreeViewItem
          class="item"
          v-for="(model, index) of model.children"
          :key="index"
          :model="model"
        />
      </ul>
    </v-slide-y-transition>
  </li>
</template>

<script>
export default {
  name: "TreeViewItem",
  props: {
    model: Object
  },
  data: function() {
    return {
      open: false
    };
  },
  computed: {
    isFolder: function() {
      return this.model.children && this.model.children.length;
    }
  },
  methods: {
    toggle: function() {
      if (this.isFolder) {
        this.open = !this.open;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
li {
  cursor: pointer;

  .list-item-title {
    display: flex;
  }

  ul {
    list-style: none;
  }
}
</style>
