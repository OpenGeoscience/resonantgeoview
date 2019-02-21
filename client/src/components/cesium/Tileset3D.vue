<script>
// import Cesium from "cesium/Cesium";

export default {
  name: "Tileset3D",
  inject: ["$viewer"],
  props: {
    dataset: {
      required: true
    }
  },
  created() {
    var tileset = this.$viewer.scene.primitives.add(
      new Cesium.Cesium3DTileset({
        url: Cesium.IonResource.fromAssetId(this.dataset.geometa.assetId)
      })
    );
    this.$viewer.zoomTo(tileset);
  },
  render() {
    return null;
  }
};
</script>
