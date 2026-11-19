<template>
  <v-dialog v-model="open" max-width="500px">
    <v-card rounded="lg">
      <v-card-title class="pa-4 bg-surface-light">
        <v-icon :icon="iconName" class="mr-2" color="primary" />
        Add {{ type }}
      </v-card-title>

      <v-card-text class="pt-4">
        <v-form v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="form.name"
            :label="type === 'Pet' ? 'Pet Name' : 'Nickname (e.g. Dad\'s Car)'"
            variant="outlined"
            prepend-inner-icon="mdi-tag-text"
            :rules="[(v) => !!v || 'Name is required']"
            class="mb-2"
          />

          <div v-if="type === 'Vehicle'">
            <v-row density="compact">
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
            <v-row density="compact">
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
        <v-btn variant="text" @click="open = false">Cancel</v-btn>
        <v-btn color="primary" variant="flat" :loading="loading" :disabled="!valid" @click="save">
          Save {{ type }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import api from '@/services/api'

const open = defineModel({ type: Boolean })

const props = defineProps({
  type: { type: String, default: 'Vehicle' },
  householdId: Number,
})

const emit = defineEmits(['saved'])

function getResetForm() {
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
}

const valid = ref(false)
const loading = ref(false)
const form = ref(getResetForm())

const iconName = computed(() => (props.type === 'Pet' ? 'mdi-paw' : 'mdi-car'))

watch(open, (val) => {
  if (val) {
    form.value = getResetForm()
  }
})

async function save() {
  if (!props.householdId) return
  loading.value = true

  let details = {}

  if (props.type === 'Vehicle') {
    details = {
      make: form.value.make,
      model: form.value.model,
      reg: form.value.reg,
      vin: form.value.vin,
    }
  } else if (props.type === 'Pet') {
    details = {
      species: form.value.species,
      breed: form.value.breed,
      color: form.value.color,
      chip_id: form.value.chip_id,
    }
  }

  const formData = new FormData()
  formData.append('household_id', props.householdId)
  formData.append('name', form.value.name)
  formData.append('type', props.type)
  formData.append('details', JSON.stringify(details))

  try {
    await api.post('/assets/', formData)
    emit('saved')
    open.value = false
  } catch (e) {
    console.error('Failed to save asset', e)
  } finally {
    loading.value = false
  }
}
</script>
