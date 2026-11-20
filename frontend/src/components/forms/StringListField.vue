<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-2">
      <h4 class="text-body-small font-weight-bold text-medium-emphasis">
        {{ title }}
      </h4>
      <v-btn size="small" variant="text" color="primary" prepend-icon="mdi-plus" @click="addItem">
        {{ addLabel }}
      </v-btn>
    </div>

    <div v-if="normalizedItems.length > 0">
      <v-row
        v-for="(item, index) in normalizedItems"
        :key="index"
        density="compact"
        class="align-center mb-1"
      >
        <v-col cols="11">
          <v-text-field
            :model-value="item"
            :label="itemLabel"
            :placeholder="placeholder"
            variant="outlined"
            density="comfortable"
            hide-details
            bg-color="surface"
            @update:model-value="(val) => updateItem(index, val)"
          />
        </v-col>
        <v-col cols="1" class="d-flex justify-center">
          <v-icon-btn
            icon="mdi-delete"
            size="small"
            variant="text"
            color="red-lighten-2"
            :aria-label="removeAriaLabel"
            @click="removeItem(index)"
          />
        </v-col>
      </v-row>
    </div>

    <v-sheet
      v-else
      rounded="md"
      border
      class="d-flex align-center px-3 py-2 text-body-small text-medium-emphasis bg-surface-light"
    >
      <v-icon icon="mdi-information-outline" size="small" class="mr-2" aria-hidden="true" />
      {{ emptyText }}
    </v-sheet>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const model = defineModel({ default: () => [] })

defineProps({
  title: { type: String, required: true },
  addLabel: { type: String, default: 'Add' },
  itemLabel: { type: String, default: 'Name' },
  placeholder: { type: String, default: '' },
  emptyText: { type: String, default: 'No items added.' },
  removeAriaLabel: { type: String, default: 'Remove item' },
})

const normalizedItems = computed(() => {
  if (Array.isArray(model.value)) return model.value
  if (typeof model.value === 'string' && model.value.trim()) {
    return model.value
      .split(',')
      .map((entry) => entry.trim())
      .filter(Boolean)
  }
  return []
})

function addItem() {
  model.value = [...normalizedItems.value, '']
}

function updateItem(index, value) {
  const next = [...normalizedItems.value]
  next[index] = value
  model.value = next
}

function removeItem(index) {
  const next = [...normalizedItems.value]
  next.splice(index, 1)
  model.value = next
}
</script>
