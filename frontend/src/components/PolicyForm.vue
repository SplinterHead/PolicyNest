<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="600px"
  >
    <v-card rounded="lg">
      <v-card-title class="pa-4 bg-primary text-white">New Policy</v-card-title>
      <v-card-text class="pt-4">
        <v-form ref="form" @submit.prevent="submit">
          <v-row dense>
            <v-col cols="12" sm="6"
              ><v-text-field
                v-model="form.provider"
                label="Provider"
                variant="outlined"
                density="comfortable"
              ></v-text-field
            ></v-col>
            <v-col cols="12" sm="6">
              <v-select
                v-model="form.type"
                :items="['Car', 'Home', 'Life', 'Medical', 'Pet']"
                label="Type"
                variant="outlined"
                density="comfortable"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6"
              ><v-text-field
                type="date"
                v-model="form.start_date"
                label="Start Date"
                variant="outlined"
                density="comfortable"
              ></v-text-field
            ></v-col>
            <v-col cols="12" sm="6"
              ><v-text-field
                type="date"
                v-model="form.end_date"
                label="End Date"
                variant="outlined"
                density="comfortable"
              ></v-text-field
            ></v-col>
            <v-col cols="12"
              ><v-text-field
                type="number"
                step="0.01"
                v-model="form.premium"
                label="Premium Cost"
                variant="outlined"
                density="comfortable"
                prefix="$"
              ></v-text-field
            ></v-col>
            <v-col cols="12">
              <v-file-input
                @change="handleFileUpload"
                label="Policy Document (PDF)"
                variant="outlined"
                density="comfortable"
                accept=".pdf"
                prepend-inner-icon="mdi-paperclip"
              ></v-file-input>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="$emit('update:modelValue', false)">Cancel</v-btn>
        <v-btn color="primary" variant="flat" @click="submit" :loading="loading">Save Policy</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    modelValue: Boolean,
    loading: Boolean,
  },
  emits: ['update:modelValue', 'submit'],
  data() {
    return {
      form: { provider: '', type: null, start_date: '', end_date: '', premium: '' },
      file: null,
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0]
    },
    submit() {
      // Validate
      if (!this.form.provider || !this.form.premium) return

      // Emit data up to parent
      this.$emit('submit', { ...this.form, file: this.file })

      // Reset logic is better handled here after success,
      // but for simplicity we can reset on close or via a watcher.
    },
  },
  watch: {
    // Reset form when dialog closes
    modelValue(val) {
      if (!val) {
        this.form = { provider: '', type: null, start_date: '', end_date: '', premium: '' }
        this.file = null
      }
    },
  },
}
</script>
