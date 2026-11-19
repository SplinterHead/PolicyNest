<template>
  <v-app-bar elevation="1">
    <v-app-bar-nav-icon @click="emit('toggle-drawer')" />

    <v-app-bar-title class="font-weight-bold text-primary" @click="router.push('/policies')">
      <v-icon icon="mdi-shield-check" class="mr-2" />
      <span class="font-weight-bold">policy</span>
      <span class="font-weight-light">nest</span>
    </v-app-bar-title>

    <v-spacer />

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
import { useRouter } from 'vue-router'

defineProps({
  isDark: Boolean,
})

const emit = defineEmits(['toggle-drawer', 'toggle-theme'])
const router = useRouter()
</script>

<style scoped>
/* Ensure the title behaves like a button on hover */
.v-app-bar-title:hover {
  cursor: pointer;
  opacity: 0.8;
}
</style>
