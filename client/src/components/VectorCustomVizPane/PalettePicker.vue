<template>
  <v-select
    :disabled="disabled"
    :items="items"
    hide-details
    placeholder=" "
    dense
    label="Color"
    :value="palette"
    menu-props="lazy"
    @input="$emit('update:palette', $event)"
  >
    <template slot="item" slot-scope="{ item }">
      <div v-if="!continuous" class="d-flex palette item">
        <div
          class="flex1 color"
          v-for="color of item"
          :key="color"
          :style="{ background: color }"
        ></div>
      </div>
      <div
        v-else
        class="palette item"
        :style="{ background: `linear-gradient(to right,${item.join(',')})` }"
      ></div>
    </template>
    <template slot="selection" slot-scope="{ item }">
      <div v-if="!continuous" class="d-flex palette" :class="{ disabled }">
        <div
          class="flex1 color"
          v-for="color of item"
          :key="color"
          :style="{ background: color }"
        ></div>
      </div>
      <div
        v-else
        class="palette"
        :style="{ background: `linear-gradient(to right,${item.join(',')})` }"
      ></div>
    </template>
  </v-select>
</template>

<script>
import {
  colorbrewerCategories,
  toPaletteColors
} from "../../utils/palettableColorbrewerMapper";

export default {
  name: "PalettePicker",
  props: {
    palette: {
      type: Array
    },
    disabled: {
      type: Boolean,
      default: false
    },
    continuous: {
      type: Boolean,
      defualt: false
    },
    extras: {
      type: Object,
      default() {
        return this.palettePickerExtras;
      }
    }
  },
  inject: {
    palettePickerExtras: { default: null }
  },
  data() {
    return {};
  },
  computed: {
    items() {
      var items = [];
      if (this.palette) {
        items = [this.palette, { divider: true }];
      }
      if (this.extras) {
        for (let [category, palette] of Object.entries(this.extras)) {
          items.push({ header: category });
          items = [...items, ...palette];
        }
      }
      for (let category of Object.keys(colorbrewerCategories)) {
        items.push({ header: category });
        items = [
          ...items,
          ...colorbrewerCategories[category].map(ramp => toPaletteColors(ramp))
        ];
      }
      return items;
    }
  }
};
</script>

<style lang="scss" scoped>
.palette {
  height: 20px;
  width: 100%;
  border: 1px solid #c3c3c3;

  .color {
    max-width: 22%;
  }

  &.disabled {
    filter: grayscale(100%);
  }

  &.item {
    min-width: 140px;
  }
}
</style>
