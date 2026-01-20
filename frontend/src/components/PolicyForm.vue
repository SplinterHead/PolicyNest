<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="600px"
    scrollable
  >
    <v-card rounded="lg">
      <v-card-title class="pa-4 bg-primary text-white">
        {{ policyToEdit ? 'Edit Policy' : 'New Policy' }}
      </v-card-title>

      <v-card-text class="pt-4" style="max-height: 80vh">
        <v-form ref="form" @submit.prevent="submit">
          <v-row dense>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="form.provider"
                label="Provider"
                variant="outlined"
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                v-model="form.type"
                :items="policyTypes"
                label="Type"
                variant="outlined"
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                type="date"
                v-model="form.start_date"
                label="Start Date"
                variant="outlined"
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                type="date"
                v-model="form.end_date"
                label="End Date"
                variant="outlined"
                density="comfortable"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="form.premium"
                label="Premium Cost"
                variant="outlined"
                density="comfortable"
                :prefix="currencySymbol"
                type="number"
                step="0.01"
              >
                <template v-slot:append>
                  <v-select
                    v-model="form.frequency"
                    :items="['Annual', 'Monthly']"
                    variant="plain"
                    density="compact"
                    hide-details
                    width="120px"
                    class="font-weight-bold text-caption"
                  />
                </template>
              </v-text-field>
            </v-col>

            <v-col cols="12">
              <BuildingsPolicyForm
                v-if="form.type === 'Buildings'"
                v-model="form.attributes"
                :currencySymbol="currencySymbol"
              />
              <CarPolicyForm
                v-else-if="form.type === 'Car'"
                v-model="form.attributes"
                :assets="assets"
                :currencySymbol="currencySymbol"
                @update:assetId="form.asset_id = $event"
              />
              <ContentsPolicyForm
                v-else-if="form.type === 'Contents'"
                v-model="form.attributes"
                :currencySymbol="currencySymbol"
              />
              <LifePolicyForm
                v-else-if="form.type === 'Life'"
                v-model="form.attributes"
                :currencySymbol="currencySymbol"
              />
            </v-col>

            <v-col cols="12">
              <div class="d-flex align-center">
                <v-btn
                  color="primary"
                  variant="tonal"
                  prepend-icon="mdi-paperclip"
                  @click="$refs.fileUpload.click()"
                >
                  {{ file ? 'Change Document' : 'Upload Document' }}
                </v-btn>

                <div v-if="file" class="ml-3 text-body-2 font-weight-bold text-primary">
                  {{ file.name }}
                </div>
                <div v-else class="ml-3 text-caption text-medium-emphasis">PDF files only</div>

                <v-file-input
                  ref="fileUpload"
                  class="d-none"
                  accept=".pdf"
                  @update:modelValue="handleFileUpload"
                />
              </div>
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
import BuildingsPolicyForm from './forms/BuildingsPolicyForm.vue'
import ContentsPolicyForm from './forms/ContentsPolicyForm.vue'
import CarPolicyForm from './forms/CarPolicyForm.vue'
import LifePolicyForm from './forms/LifePolicyForm.vue'

export default {
  components: { BuildingsPolicyForm, ContentsPolicyForm, CarPolicyForm, LifePolicyForm },
  props: {
    modelValue: Boolean,
    loading: Boolean,
    assets: Array,
    policyToEdit: Object,
    currencyCode: String,
  },
  emits: ['update:modelValue', 'submit'],
  data() {
    return {
      form: {
        asset_id: null,
        provider: '',
        type: null,
        start_date: '',
        end_date: null,
        premium: '',
        frequency: 'Annual',
        attributes: {},
      },
      file: null,
      policyTypes: ['Buildings', 'Car', 'Contents', 'Life', 'Medical', 'Pet'],
    }
  },
  computed: {
    currencySymbol() {
      const symbols = { GBP: '£', USD: '$', EUR: '€', AUD: '$', CAD: '$' }
      return symbols[this.currencyCode] || '$'
    },
  },
  watch: {
    modelValue(isOpen) {
      if (isOpen) {
        if (this.policyToEdit) {
          this.form = { ...this.policyToEdit }
          this.form.frequency = this.policyToEdit.attributes.payment_frequency || 'Annual'
        } else {
          this.form = {
            asset_id: null,
            provider: '',
            type: null,
            start_date: '',
            end_date: '',
            premium: '',
            frequency: 'Annual',
            attributes: {},
          }
        }
        this.file = null
      }
    },
  },
  methods: {
    handleFileUpload(fileOrArray) {
      if (Array.isArray(fileOrArray) && fileOrArray.length > 0) {
        this.file = fileOrArray[0]
      } else {
        this.file = fileOrArray
      }
    },
    submit() {
      if (!this.form.provider || !this.form.premium) return
      const finalAttributes = {
        ...this.form.attributes,
        payment_frequency: this.form.frequency,
      }
      this.$emit('submit', {
        ...this.form,
        attributes: JSON.stringify(finalAttributes),
        file: this.file,
        id: this.policyToEdit?.id,
      })
    },
  },
}
</script>

<style scoped>
/* Chrome, Safari, Edge, Opera */
:deep(input::-webkit-outer-spin-button),
:deep(input::-webkit-inner-spin-button) {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
:deep(input[type='number']) {
  -moz-appearance: textfield;
}
</style>
