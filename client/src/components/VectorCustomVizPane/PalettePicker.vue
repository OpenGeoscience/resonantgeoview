<template>
  <v-select
    :disabled="disabled"
    :items="items"
    hide-details
    placeholder=" "
    dense
    label="Color"
    :value="palette"
    @input="$emit('update:palette', $event)">
    <template slot="item" slot-scope="{item}">
      <div class="d-flex palette item">
        <div class="flex1 color" v-for="color of item" :key='color' :style="{background:color}">
        </div>
      </div>
    </template>
    <template slot="selection" slot-scope="{item}">
      <div class="d-flex palette" :class="{disabled}">
        <div class="flex1 color" v-for="color of item" :key='color' :style="{background:color}">
        </div>
      </div>
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

  .color {
    max-width: 22%;
    border-top: 1px solid #c3c3c3;
    border-bottom: 1px solid #c3c3c3;

    &:first-child {
      border-left: 1px solid #c3c3c3;
    }

    &:last-child {
      border-right: 1px solid #c3c3c3;
    }
  }

  &.disabled {
    filter: grayscale(100%);
  }

  &.item {
    min-width: 140px;
  }
}
</style>
