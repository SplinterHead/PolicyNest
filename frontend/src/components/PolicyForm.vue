<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="600px"
    scrollable
  >
    <v-card rounded="lg">
      <v-card-title class="pa-4 bg-primary text-white">New Policy</v-card-title>

      <v-card-text class="pt-4" style="max-height: 80vh">
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

            <v-col cols="12" v-if="form.type === 'Car'">
              <CarPolicyForm
                v-model="form.attributes"
                :assets="assets"
                @update:assetId="form.asset_id = $event"
              />
            </v-col>
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
import CarPolicyForm from './forms/CarPolicyForm.vue'

export default {
  components: { CarPolicyForm },
  props: {
    modelValue: Boolean,
    loading: Boolean,
    assets: Array,
  },
  emits: ['update:modelValue', 'submit'],
  data() {
    return {
      form: {
        asset_id: null,
        provider: '',
        type: null,
        start_date: '',
        end_date: '',
        premium: '',
        attributes: {}, // <-- New object for dynamic data
      },
      file: null,
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0]
    },
    submit() {
      if (!this.form.provider || !this.form.premium) return
      this.$emit('submit', {
        ...this.form,
        attributes: JSON.stringify(this.form.attributes),
        file: this.file,
      })
    },
  },
  watch: {
    modelValue(val) {
      if (!val) {
        // Reset form
        this.form = {
          provider: '',
          type: null,
          start_date: '',
          end_date: '',
          premium: '',
          attributes: {},
        }
        this.file = null
      }
    },
  },
}
</script>
