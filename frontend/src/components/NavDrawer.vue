<template>
  <v-navigation-drawer v-model="drawer">
    <div class="pa-2">
      <v-menu location="bottom">
        <template #activator="{ props }">
          <v-card
            v-bind="props"
            tag="button"
            type="button"
            color="primary"
            elevation="0"
            rounded="lg"
            class="w-100 text-left pa-3 cursor-pointer household-switcher-btn"
            :aria-label="
              currentHousehold
                ? `Switch household, currently ${currentHousehold.name}`
                : 'Switch household'
            "
            v-ripple
          >
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center overflow-hidden">
                <v-avatar color="white" size="36" class="mr-3 text-primary">
                  <span class="text-title-small font-weight-bold">
                    {{ currentHousehold ? currentHousehold.name.charAt(0) : 'H' }}
                  </span>
                </v-avatar>
                <div class="text-truncate">
                  <div class="text-body-small text-blue-lighten-4 font-weight-bold">HOUSEHOLD</div>
                  <div class="text-title-small font-weight-bold text-white text-truncate">
                    {{ currentHousehold ? currentHousehold.name : 'Select...' }}
                  </div>
                </div>
              </div>
              <v-icon color="white" icon="mdi-chevron-down" size="small" />
            </div>
          </v-card>
        </template>

        <v-list density="compact" nav role="menu" aria-label="Households" class="mt-2">
          <v-list-subheader>Switch Household</v-list-subheader>

          <v-list-item
            v-for="h in households"
            :key="h.id"
            role="menuitemradio"
            :aria-checked="Boolean(currentHousehold && currentHousehold.id === h.id)"
            :active="currentHousehold && currentHousehold.id === h.id"
            color="primary"
            @click="emit('switch-household', h)"
          >
            <template #prepend>
              <v-icon
                :icon="
                  currentHousehold && currentHousehold.id === h.id
                    ? 'mdi-check'
                    : 'mdi-home-outline'
                "
              />
            </template>
            <v-list-item-title>{{ h.name }}</v-list-item-title>
          </v-list-item>

          <v-divider class="my-2" />

          <v-list-item
            role="menuitem"
            prepend-icon="mdi-cog-outline"
            title="Manage Households"
            @click="emit('open-manage')"
          />
        </v-list>
      </v-menu>
    </div>

    <v-divider />

    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-file-document-multiple"
        title="Policies"
        value="policies"
        to="/policies"
        color="primary"
      />
      <v-list-item
        prepend-icon="mdi-car-multiple"
        title="Inventory"
        value="inventory"
        to="/inventory"
        color="primary"
      />
      <v-list-item
        prepend-icon="mdi-cog"
        title="Settings"
        value="settings"
        to="/settings"
        color="primary"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
const drawer = defineModel()

defineProps({
  households: Array,
  currentHousehold: Object,
})

const emit = defineEmits(['switch-household', 'open-manage'])
</script>

<style scoped>
.household-switcher-btn:focus-visible {
  outline: 2px solid rgb(var(--v-theme-on-surface));
  outline-offset: 2px;
}
</style>
