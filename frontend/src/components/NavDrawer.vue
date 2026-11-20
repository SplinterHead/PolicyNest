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
                <v-avatar color="surface" size="36" class="mr-3 text-primary">
                  <span class="text-title-small font-weight-bold">
                    {{ currentHousehold ? currentHousehold.name.charAt(0) : 'H' }}
                  </span>
                </v-avatar>
                <div class="text-truncate">
                  <div class="text-body-small font-weight-bold opacity-90">HOUSEHOLD</div>
                  <div class="text-title-small font-weight-bold text-truncate">
                    {{ currentHousehold ? currentHousehold.name : 'Select...' }}
                  </div>
                </div>
              </div>
              <v-icon icon="mdi-chevron-down" size="small" />
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

    <template #append>
      <v-divider />
      <div class="d-flex flex-column align-center pa-3 ga-1 text-medium-emphasis">
        <span class="text-body-small">{{ formattedVersion }}</span>
        <v-btn
          icon="mdi-github"
          variant="text"
          density="comfortable"
          color="default"
          href="https://github.com/SplinterHead/PolicyNest"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="View PolicyNest on GitHub (opens in a new tab)"
        />
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
const drawer = defineModel()

defineProps({
  households: Array,
  currentHousehold: Object,
})

const emit = defineEmits(['switch-household', 'open-manage'])

const rawVersion = (import.meta.env.VITE_APP_VERSION || 'dev').trim()
const formattedVersion =
  rawVersion === 'dev' || rawVersion.startsWith('v') ? rawVersion : `v${rawVersion}`
</script>

<style scoped>
.household-switcher-btn:focus-visible {
  outline: 2px solid rgb(var(--v-theme-on-surface));
  outline-offset: 2px;
}
</style>
