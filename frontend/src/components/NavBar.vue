<template>
  <v-app-bar elevation="1">
    <v-app-bar-nav-icon
      aria-label="Toggle navigation menu"
      :aria-expanded="String(drawerOpen)"
      @click="emit('toggle-drawer')"
    />

    <v-app-bar-title>
      <router-link
        to="/policies"
        class="brand-link d-inline-flex align-center text-primary text-decoration-none rounded px-1"
        aria-label="PolicyNest Home"
      >
        <v-icon icon="mdi-shield-check" class="mr-2" aria-hidden="true" />
        <span class="font-weight-bold">policy</span>
        <span class="font-weight-light">nest</span>
      </router-link>
    </v-app-bar-title>

    <v-spacer />

    <v-menu v-if="currentHousehold && (mobile || !drawerOpen)" location="bottom end">
      <template #activator="{ props: menuProps }">
        <v-btn
          v-bind="menuProps"
          variant="tonal"
          color="primary"
          size="small"
          rounded="pill"
          prepend-icon="mdi-home-outline"
          append-icon="mdi-chevron-down"
          class="mr-2"
          :aria-label="`Switch household, currently ${currentHousehold.name}`"
        >
          <span class="text-truncate" style="max-width: 120px">{{ currentHousehold.name }}</span>
        </v-btn>
      </template>

      <v-list density="compact" nav role="menu" aria-label="Households">
        <v-list-item
          v-for="h in households"
          :key="h.id"
          :active="h.id === currentHousehold.id"
          color="primary"
          role="menuitemradio"
          :aria-checked="String(h.id === currentHousehold.id)"
          @click="emit('switch-household', h)"
        >
          <v-list-item-title>{{ h.name }}</v-list-item-title>
          <template v-if="h.id === currentHousehold.id" #append>
            <v-icon icon="mdi-check" size="small" />
          </template>
        </v-list-item>
        <v-divider class="my-1" />
        <v-list-item
          role="menuitem"
          prepend-icon="mdi-cog"
          title="Manage Households"
          @click="emit('open-manage')"
        />
      </v-list>
    </v-menu>

    <v-icon-btn
      :icon="isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'"
      variant="text"
      :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'"
      class="mr-2"
      @click="emit('toggle-theme')"
    />
  </v-app-bar>
</template>

<script setup>
import { useDisplay } from 'vuetify'

defineProps({
  currentHousehold: {
    type: Object,
    default: null,
  },
  drawerOpen: Boolean,
  households: {
    type: Array,
    default: () => [],
  },
  isDark: Boolean,
})

const emit = defineEmits(['toggle-drawer', 'toggle-theme', 'switch-household', 'open-manage'])
const { mobile } = useDisplay()
</script>

<style scoped>
.brand-link:hover {
  opacity: 0.85;
}
</style>
