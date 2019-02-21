<script>
import CesiumViewport from "../components/cesium/CesiumViewport";

export default {
  name: "CesiumContainer",
  components: {
    CesiumViewport
  }
};
</script>

<template>
  <FullScreenViewport>
    <CesiumViewport />
  </FullScreenViewport>
</template>
