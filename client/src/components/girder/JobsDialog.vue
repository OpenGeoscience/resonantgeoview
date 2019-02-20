<script>
export default {
  name: "JobsDialog",
  components: {},
  props: {
    value: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    emitWMSDataset() {
      this.close();
    },
    close() {
      this.$emit("input", false);
    }
  }
};
</script>

<template>
  <v-dialog
    class="jobs-dialog"
    content-class="jobs-dialog-content"
    :value="value"
    @input="$emit('input', $event)"
    scrollable
    lazy
  >
    <GirderJobList />
  </v-dialog>
</template>

<style lang="scss">
.jobs-dialog-content {
  background: #fafafa;
  display: block;
  transition: height 4s;
}
</style>
