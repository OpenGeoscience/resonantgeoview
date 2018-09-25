<script>
import { VDialog } from "vuetify/es5/components/VDialog";

export default {
  extends: VDialog,
  props: {
    transition: {
      type: [String, Boolean],
      default: "slide-x-reverse-transition"
    },
    left: String,
    right: String,
    top: String,
    bottom: String
  },
  computed: {
    contentClasses() {
      var baseContentClasses = VDialog.computed.contentClasses.call(this);
      baseContentClasses["positioned"] = true;
      return baseContentClasses;
    }
  },
  render(h) {
    var baseRender = VDialog.render.call(this, h);
    var dialogStyle =
      baseRender.children[0].children[0].componentOptions.children[0]
        .componentOptions.children[0].data.style;
    if (this.left) {
      dialogStyle.left = this.left;
    }
    if (this.right) {
      dialogStyle.right = this.right;
    }
    if (this.top) {
      dialogStyle.top = this.top;
    }
    if (this.bottom) {
      dialogStyle.bottom = this.bottom;
    }
    return baseRender;
  }
};
</script>

<style>
.v-dialog__content.positioned {
  display: block;
}

.v-dialog__content.positioned .v-dialog {
  position: absolute;
  margin: 0;
}
</style>
