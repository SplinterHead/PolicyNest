<template>
  <v-app-bar elevation="1">
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')"></v-app-bar-nav-icon>

    <v-app-bar-title class="font-weight-bold text-primary">
      <v-icon icon="mdi-shield-check" class="mr-2" />
      <span class="font-weight-bold">policy</span>
      <span class="font-weight-light">nest</span>
    </v-app-bar-title>

    <v-spacer />

    <v-btn icon @click="$emit('toggle-theme')" class="mr-2">
      <v-icon :icom="isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'" />
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    isDark: Boolean,
  },
  emits: ['toggle-drawer', 'toggle-theme'],
}
</script>
