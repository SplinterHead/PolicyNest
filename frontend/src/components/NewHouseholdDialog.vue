<template>
  <v-dialog
    v-model="open"
    max-width="500px"
    :persistent="!showCancel"
    aria-labelledby="new-household-title"
  >
    <v-card rounded="lg" elevation="2" class="text-center pa-2 h-100 position-relative">
      <v-card-title id="new-household-title" class="text-headline-small font-weight-bold">
        <v-icon icon="mdi-home-plus" color="primary" class="mb-1" />
        {{ title }}
      </v-card-title>

      <v-card-text>
        <p class="mb-4 text-medium-emphasis">
          {{ subtitle }}
        </p>

        <v-form v-model="valid" @submit.prevent="submit">
          <v-text-field
            v-model="name"
            label="Household Name"
            variant="outlined"
            placeholder="e.g. Dream Home"
            :rules="[(v) => !!v || 'Name is required']"
            autofocus
            :loading="loading"
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="justify-center">
        <v-btn v-if="showCancel" variant="text" @click="open = false">Cancel</v-btn>

        <v-btn
          color="primary"
          size="large"
          variant="flat"
          :class="{ 'ml-2': showCancel, 'w-100': !showCancel }"
          :loading="loading"
          :disabled="!valid || !name"
          @click="submit"
        >
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const open = defineModel({ type: Boolean, required: true })

defineProps({
  showCancel: { type: Boolean, default: false },
  title: { type: String, default: 'Create Household' },
  subtitle: { type: String, default: 'Give your household a name.' },
})

const emit = defineEmits(['complete'])

const name = ref('')
const loading = ref(false)
const valid = ref(false)

async function submit() {
  if (!name.value) return
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('name', name.value)
    const res = await api.post('/households/', formData)
    emit('complete', res.data)
    name.value = ''
  } catch (e) {
    console.error('Household creation failed:', e)
  } finally {
    loading.value = false
  }
}
</script>
