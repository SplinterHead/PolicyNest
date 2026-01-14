<template>
  <v-navigation-drawer
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="pa-2">
      <v-menu location="bottom">
        <template v-slot:activator="{ props }">
          <v-card
            v-bind="props"
            color="primary"
            elevation="0"
            rounded="lg"
            class="pa-3 cursor-pointer"
            v-ripple
          >
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center overflow-hidden">
                <v-avatar color="white" size="36" class="mr-3 text-primary">
                  <span class="text-subtitle-2 font-weight-bold">
                    {{ currentHousehold ? currentHousehold.name.charAt(0) : 'H' }}
                  </span>
                </v-avatar>
                <div class="text-truncate">
                  <div class="text-caption text-blue-lighten-4 font-weight-bold">HOUSEHOLD</div>
                  <div class="text-subtitle-2 font-weight-bold text-white text-truncate">
                    {{ currentHousehold ? currentHousehold.name : 'Select...' }}
                  </div>
                </div>
              </div>
              <v-icon color="white" icon="mdi-chevron-down" size="small"></v-icon>
            </div>
          </v-card>
        </template>

        <v-list density="compact" nav class="mt-2">
          <v-list-subheader>Switch Household</v-list-subheader>

          <v-list-item
            v-for="h in households"
            :key="h.id"
            :value="h.id"
            @click="$emit('switch-household', h)"
            :active="currentHousehold && currentHousehold.id === h.id"
            color="primary"
          >
            <template v-slot:prepend>
              <v-icon
                :icon="
                  currentHousehold && currentHousehold.id === h.id
                    ? 'mdi-check'
                    : 'mdi-home-outline'
                "
              ></v-icon>
            </template>
            <v-list-item-title>{{ h.name }}</v-list-item-title>
          </v-list-item>

          <v-divider class="my-2"></v-divider>

          <v-list-item
            prepend-icon="mdi-cog-outline"
            title="Manage Households"
            @click="$emit('open-manage')"
          ></v-list-item>
        </v-list>
      </v-menu>
    </div>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-file-document-multiple"
        title="Policies"
        value="policies"
        active
        color="primary"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    modelValue: Boolean, // Standard Vue 3 prop for v-model
    households: Array,
    currentHousehold: Object,
  },
  emits: ['update:modelValue', 'switch-household', 'open-manage'],
}
</script>
