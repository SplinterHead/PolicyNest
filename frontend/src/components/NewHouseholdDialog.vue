<template>
  <v-dialog :model-value="modelValue" max-width="500px" :persistent="!showCancel">
    <v-card class="text-center pa-6">
      <v-icon icon="mdi-home-plus" size="64" color="primary" class="mb-4" />

      <v-card-title class="text-h5 font-weight-bold">
        {{ title }}
      </v-card-title>

      <v-card-text>
        <p class="mb-4 text-medium-emphasis">
          {{ subtitle }}
        </p>

        <v-form @submit.prevent="submit" v-model="valid">
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
        <v-btn v-if="showCancel" variant="text" @click="$emit('update:modelValue', false)">
          Cancel
        </v-btn>

        <v-btn
          color="primary"
          size="large"
          variant="flat"
          :class="{ 'ml-2': showCancel, 'w-100': !showCancel }"
          @click="submit"
          :loading="loading"
          :disabled="!valid || !name"
        >
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'NewHouseholdDialog',
  props: {
    modelValue: { type: Boolean, required: true },
    showCancel: { type: Boolean, default: false },
    title: { type: String, default: 'Create Household' },
    subtitle: { type: String, default: 'Give your household a name.' },
  },
  emits: ['update:modelValue', 'complete'],
  data() {
    return {
      name: '',
      loading: false,
      valid: false,
    }
  },
  methods: {
    async submit() {
      if (!this.name) return
      this.loading = true
      try {
        const res = await api.post('/households/', { name: this.name })
        this.$emit('complete', res.data)
        this.name = ''
      } catch (e) {
        console.error('Household creation failed:', e)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
