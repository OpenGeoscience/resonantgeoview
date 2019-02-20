<template>
  <v-dialog
    :value="value"
    @input="$emit('input', $event)"
    scrollable
    max-width="250px"
  >
    <v-card>
      <v-card-title class="title">
        <span>Move to</span>
      </v-card-title>
      <v-card-text style="max-height: 300px;">
        <v-list dense>
          <v-list-tile
            v-for="group in groups"
            :key="group._id"
            :class="{ selected: selectedGroup === group }"
            @click="selectedGroup = group"
          >
            <v-list-tile-content>
              <v-list-tile-title
                class="body-2"
                v-text="group.name"
              ></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <NewWithName name="group" default="group-1" @confirm="createGroup" />
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          flat
          @click="
            addDatasetToGroup({ group: selectedGroup, dataset });
            $emit('input', false);
          "
          :disabled="!selectedGroup"
          >Ok</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions } from "vuex";

import NewWithName from "../components/NewWithName";

export default {
  name: "DatasetGroupDialog",
  components: { NewWithName },
  props: {
    value: {
      type: Boolean,
      required: true
    },
    dataset: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedGroup: null
    };
  },
  computed: {
    ...mapState(["groups"])
  },
  methods: {
    ...mapActions(["createGroup", "addDatasetToGroup"])
  }
};
</script>
