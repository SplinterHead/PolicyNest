<template>
  <v-dialog
    :model-value="modelValue"
    max-width="500px"
    @update:modelValue="$emit('update:modelValue', $event)"
  >
    <v-card rounded="lg">
      <v-card-title class="pa-4 bg-surface-light">
        <v-icon :icon="getIcon" class="mr-2" color="primary" />
        Add {{ type }}
      </v-card-title>

      <v-card-text class="pt-4">
        <v-form ref="form" v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="form.name"
            :label="type === 'Pet' ? 'Pet Name' : 'Nickname (e.g. Dad\'s Car)'"
            variant="outlined"
            prepend-inner-icon="mdi-tag-text"
            :rules="[(v) => !!v || 'Name is required']"
            class="mb-2"
          />

          <div v-if="type === 'Vehicle'">
            <v-row dense>
              <v-col cols="6">
                <v-text-field
                  v-model="form.make"
                  label="Make"
                  placeholder="Toyota"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="form.model"
                  label="Model"
                  placeholder="Corolla"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.reg"
                  label="Registration Plate"
                  variant="outlined"
                  density="compact"
                  prepend-inner-icon="mdi-card-account-details"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.vin"
                  label="VIN (Optional)"
                  variant="outlined"
                  density="compact"
                  prepend-inner-icon="mdi-barcode"
                />
              </v-col>
            </v-row>
          </div>

          <div v-if="type === 'Pet'">
            <v-row dense>
              <v-col cols="12">
                <v-select
                  v-model="form.species"
                  :items="['Dog', 'Cat', 'Rabbit', 'Bird', 'Horse', 'Reptile', 'Other']"
                  label="Species"
                  variant="outlined"
                  density="compact"
                  prepend-inner-icon="mdi-paw"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="form.breed"
                  label="Breed"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="form.color"
                  label="Color/Markings"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.chip_id"
                  label="Microchip ID"
                  variant="outlined"
                  density="compact"
                  prepend-inner-icon="mdi-barcode-scan"
                />
              </v-col>
            </v-row>
          </div>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4 pt-0">
        <v-spacer />
        <v-btn variant="text" @click="$emit('update:modelValue', false)">Cancel</v-btn>
        <v-btn color="primary" variant="flat" @click="save" :loading="loading" :disabled="!valid">
          Save {{ type }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'AssetDialog',
  props: {
    modelValue: Boolean,
    type: { type: String, default: 'Vehicle' },
    householdId: Number,
  },
  emits: ['update:modelValue', 'saved'],
  data() {
    return {
      valid: false,
      loading: false,
      form: this.getResetForm(),
    }
  },
  computed: {
    getIcon() {
      return this.type === 'Pet' ? 'mdi-paw' : 'mdi-car'
    },
  },
  watch: {
    modelValue(val) {
      if (val) {
        this.form = this.getResetForm()
      }
    },
  },
  methods: {
    getResetForm() {
      return {
        name: '',
        make: '',
        model: '',
        reg: '',
        vin: '',
        species: 'Dog',
        breed: '',
        color: '',
        chip_id: '',
      }
    },
    async save() {
      if (!this.householdId) return
      this.loading = true

      let details = {}

      if (this.type === 'Vehicle') {
        details = {
          make: this.form.make,
          model: this.form.model,
          reg: this.form.reg,
          vin: this.form.vin,
        }
      } else if (this.type === 'Pet') {
        details = {
          species: this.form.species,
          breed: this.form.breed,
          color: this.form.color,
          chip_id: this.form.chip_id,
        }
      }

      let formData = new FormData()
      formData.append('household_id', this.householdId)
      formData.append('name', this.form.name)
      formData.append('type', this.type)
      formData.append('details', JSON.stringify(details))

      try {
        await api.post('/assets/', formData)
        this.$emit('saved')
        this.$emit('update:modelValue', false)
      } catch (e) {
        console.error('Failed to save asset', e)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
