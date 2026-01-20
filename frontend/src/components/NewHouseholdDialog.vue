<template>
  <v-dialog :model-value="modelValue" max-width="500px" persistent>
    <v-card class="text-center pa-6">
      <v-icon icon="mdi-home-plus" size="64" color="primary" class="mb-4" />

      <v-card-title class="text-h5 font-weight-bold">
        Welcome to PolicyNest!
      </v-card-title>

      <v-card-text>
        <p class="mb-4 text-medium-emphasis">
          To get started, please name your household (e.g., "Smith Family" or "My Apartment").
        </p>

        <v-form @submit.prevent="submit" v-model="valid">
          <v-text-field
            v-model="name"
            label="Household Name"
            variant="outlined"
            placeholder="e.g. Dream Home"
            :rules="[v => !!v || 'Name is required']"
            autofocus
            :loading="loading"
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="justify-center">
        <v-btn
          color="primary"
          size="large"
          variant="flat"
          block
          @click="submit"
          :loading="loading"
          :disabled="!valid || !name"
        >
          Get Started
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from '../services/api';

export default {
  name: 'OnboardingDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:modelValue', 'complete'],
  data() {
    return {
      name: '',
      loading: false,
      valid: false
    };
  },
  methods: {
    async submit() {
      if (!this.name) return;

      this.loading = true;
      try {
        const payload = { name: this.name };
        const res = await api.post('/households/', payload);
        this.$emit('complete', res.data);
        this.name = '';
      } catch (e) {
        console.error("Household creation failed:", e);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>