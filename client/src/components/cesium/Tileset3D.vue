<script>
import { API_URL } from "../../constants";

export default {
  name: "Tileset3D",
  inject: ["$viewer", "girderRest"],
  props: {
    dataset: {
      required: true
    }
  },
  created() {
    this.tileset = new Cesium.Cesium3DTileset({
      url: this.getUrl()
    });
    this.$viewer.scene.primitives.add(this.tileset);
    this.$viewer.zoomTo(this.tileset);
  },
  beforeDestroy() {
    this.$viewer.scene.primitives.remove(this.tileset);
  },
  render() {
    return null;
  },
  methods: {
    getUrl() {
      return this.girderRest
        .get(`resource/${this.dataset._id}/path`, {
          params: {
            type: "item"
          }
        })
        .then(({ data: path }) => {
          return new Cesium.Resource({
            url: API_URL + "/resource/path/download" + path,
            headers: {
              "Girder-Token": this.girderRest.token
            }
          });
        });
    }
  }
};
</script>
