<template>
  <div class="d-flex flex-wrap ga-2">
    <v-chip
      v-for="item in items"
      :key="item.label"
      :color="item.enabled ? 'green' : 'default'"
      variant="tonal"
    >
      <v-icon start :icon="item.enabled ? 'mdi-check' : 'mdi-close'" />
      {{ item.label }}
    </v-chip>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})
</script>
