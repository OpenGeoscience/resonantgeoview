<script>
import debounce from "lodash-es/debounce";
import { VNavigationDrawer } from "vuetify/es5/components/VNavigationDrawer";

export default {
  extends: VNavigationDrawer,
  name: "ResizableVNavigationDrawer",
  data: () => ({
    additionalWidth: 0,
    initialAdditionalWidth: 0,
    initialClientX: null,
    dragging: false
  }),
  computed: {
    calculatedWidth() {
      return this.miniVariant
        ? this.miniVariantWidth
        : this.width + this.additionalWidth;
    }
  },
  created() {
    this.onResizing = debounce(this.onResizing, 30);
  },
  methods: {
    onResizing(e) {
      if (this.dragging) {
        this.additionalWidth = Math.max(
          0,
          this.initialAdditionalWidth + (e.clientX - this.initialClientX)
        );
        if (this.$vuetify.application.left) {
          this.$vuetify.application.left = this.calculatedWidth;
        }
      }
    },
    stopResize() {
      window.removeEventListener("mousemove", this.onResizing);
      window.removeEventListener("mouseup", this.stopResize);
    }
  },
  render(h) {
    var baseRender = VNavigationDrawer.render.call(this, h);
    baseRender.children.slice(-1)[0].data.on = {
      mousedown: e => {
        this.initialClientX = e.clientX;
        this.initialAdditionalWidth = this.additionalWidth;
        this.dragging = true;
        window.addEventListener("mousemove", this.onResizing);
        window.addEventListener("mouseup", this.stopResize);
      }
    };
    return baseRender;
  }
};
</script>

<style scoped>
.v-navigation-drawer__border {
  width: 2.5px;
  cursor: ew-resize;
  user-select: none;
  touch-action: none;
}
</style>
