<template>
<StyleSection title="Stroke" :enabled="enabled" @update:enabled="$emit('update:enabled',$event)">
  <v-container fluid grid-list-xl class="px-3">
    <v-layout align-center>
      <v-flex>
        <v-slider class=""
          :disabled="!enabled"
          hide-details
          thumb-label
          :min="0"
          :max="4"
          :step="0.05"
          label="Width"
          :value='width'
          @input="$emit('update:width',$event)"></v-slider>
      </v-flex>
    </v-layout>
    <v-layout align-center>
      <v-flex xs6>
        <v-select
          :disabled="!enabled"
          :items="propertyItems"
          item-text="name"
          item-value="value"
          hide-details
          label="Property"
          placeholder=" "
          :value="property"
          menu-props="lazy"
          @input="$emit('update:property', $event)">
        </v-select>
      </v-flex>
      <v-flex xs6>
        <BasicColorPicker
          v-if="!property"
          :disabled="!enabled"
          :color="color"
          @update:color="$emit('update:color', $event)" />
        <PalettePicker
          v-else
          :disabled="!enabled"
          :palette="palette"
          @update:palette="$emit('update:palette', $event)" />
      </v-flex>
    </v-layout>
    <v-layout align-center>
      <v-flex>
        <v-slider
          :disabled="!enabled"
          hide-details
          thumb-label
          :min="0"
          :max="1"
          label="Opacity"
          :value='opacity'
          @input="$emit('update:opacity',$event)"
          :step="0.01"></v-slider>
      </v-flex>
    </v-layout>
  </v-container>
</StyleSection>
</template>

<script>
import PalettePicker from "./PalettePicker";
import BasicColorPicker from "./BasicColorPicker";
import StyleSection from "./StyleSection";
import {
  colorbrewerCategories,
  toPaletteColors
} from "../../utils/palettableColorbrewerMapper";

export default {
  name: "Stroke",
  components: { StyleSection, BasicColorPicker, PalettePicker },
  props: {
    enabled: {
      type: Boolean,
      required: true
    },
    color: {
      type: String,
      required: true
    },
    property: {
      type: String
    },
    properties: {
      type: Object,
      required: true
    },
    palette: {
      type: Array
    },
    width: {
      type: Number,
      required: true
    },
    opacity: {
      type: Number,
      required: true
    }
  },
  computed: {
    propertyItems() {
      return [
        { name: "Constant", value: null },
        { divider: true },
        ...Object.keys(this.properties).map(property => ({
          name: property,
          value: property
        }))
      ];
    }
  },
  watch: {
    property(newValue) {
      if (newValue) {
        if (!this.palette) {
          this.$emit(
            "update:palette",
            toPaletteColors(
              colorbrewerCategories[Object.keys(colorbrewerCategories)[0]][0]
            )
          );
        }
      } else {
        this.$emit("update:palette", null);
      }
    }
  }
};
</script>

<style>
</style>
