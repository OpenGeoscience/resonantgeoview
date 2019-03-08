<script>
// import Cesium from "cesium/Cesium";
import { API_URL } from "../../constants";

export default {
  name: "Model",
  inject: ["$viewer", "girderRest"],
  props: {
    dataset: {
      required: true
    }
  },
  created() {
    var position = Cesium.Cartesian3.fromDegrees(
      -75.62898254394531,
      40.02804946899414
    );
    var heading = Cesium.Math.toRadians(0.0);
    var pitch = Cesium.Math.toRadians(0.0);
    var roll = Cesium.Math.toRadians(0.0);
    var orientation = Cesium.Transforms.headingPitchRollQuaternion(
      position,
      new Cesium.HeadingPitchRoll(heading, pitch, roll)
    );

    var entity = this.$viewer.entities.add({
      position,
      orientation,
      model: {
        uri: `${API_URL}/item/${this.dataset._id}/download`
      }
    });

    this.$viewer.zoomTo(entity);

    // var modelMatrix = Cesium.Transforms.eastNorthUpToFixedFrame(
    //   Cesium.Cartesian3.fromDegrees(-75.62898254394531, 40.02804946899414, 0.0)
    // );
    // var model = this.$viewer.scene.primitives.add(
    //   Cesium.Model.fromGltf({
    //     url: `https://zouyaoji.top/vue-cesium/statics/SampleData/models/GroundVehicle/GroundVehicle.glb`,
    //     modelMatrix: modelMatrix,
    //     scale: 300
    //   })
    // );
    // this.$viewer.zoomTo(model);
  },
  render() {
    return null;
  }
};
</script>
