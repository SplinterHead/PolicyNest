<template>
  <v-dialog id="asset-dialog" v-model="open" max-width="500px" aria-labelledby="asset-dialog-title">
    <v-defaults-provider :defaults="{ VMenu: { attach: '#asset-dialog' } }">
      <v-card rounded="lg">
        <v-card-title id="asset-dialog-title" class="pa-4 bg-surface-light">
          <v-icon :icon="iconName" class="mr-2" color="primary" />
          {{ isEditing ? `Edit ${effectiveType}` : `Add ${effectiveType}` }}
        </v-card-title>

        <v-card-text class="pt-4">
          <v-form v-model="valid" @submit.prevent="save">
            <v-text-field
              v-model="form.name"
              :label="effectiveType === 'Pet' ? 'Pet Name' : 'Nickname (e.g. Dad\'s Car)'"
              variant="outlined"
              prepend-inner-icon="mdi-tag-text"
              :rules="[(v) => !!(v && v.trim()) || 'Name is required']"
              class="mb-2"
            />

            <div v-if="effectiveType === 'Vehicle'">
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

            <div v-if="effectiveType === 'Pet'">
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
            {{ isEditing ? 'Save Changes' : `Save ${effectiveType}` }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-defaults-provider>
  </v-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import api from '@/services/api'

const open = defineModel({ type: Boolean })

const props = defineProps({
  type: { type: String, default: 'Vehicle' },
  householdId: Number,
  assetToEdit: { type: Object, default: null },
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

const effectiveType = computed(() => props.assetToEdit?.type || props.type)
const isEditing = computed(() => Boolean(props.assetToEdit))
const iconName = computed(() => (effectiveType.value === 'Pet' ? 'mdi-paw' : 'mdi-car'))

watch(open, (val) => {
  if (!val) return
  if (props.assetToEdit) {
    const details = props.assetToEdit.details || {}
    form.value = {
      name: props.assetToEdit.name || '',
      make: details.make || '',
      model: details.model || '',
      reg: details.reg || '',
      vin: details.vin || '',
      species: details.species || 'Dog',
      breed: details.breed || '',
      color: details.color || '',
      chip_id: details.chip_id || '',
    }
  } else {
    form.value = getResetForm()
  }
})

async function save() {
  if ((!isEditing.value && !props.householdId) || !form.value.name.trim()) return
  loading.value = true

  let details = {}

  if (effectiveType.value === 'Vehicle') {
    details = {
      make: form.value.make,
      model: form.value.model,
      reg: form.value.reg,
      vin: form.value.vin,
    }
  } else if (effectiveType.value === 'Pet') {
    details = {
      species: form.value.species,
      breed: form.value.breed,
      color: form.value.color,
      chip_id: form.value.chip_id,
    }
  }

  const targetHouseholdId = isEditing.value
    ? props.assetToEdit.household_id || props.householdId
    : props.householdId

  const formData = new FormData()
  formData.append('household_id', targetHouseholdId)
  formData.append('name', form.value.name.trim())
  formData.append('type', effectiveType.value)
  formData.append('details', JSON.stringify(details))

  try {
    const res = isEditing.value
      ? await api.put(`/assets/${props.assetToEdit.id}`, formData)
      : await api.post('/assets/', formData)
    emit('saved', res.data)
    open.value = false
  } catch (e) {
    console.error('Failed to save asset', e)
  } finally {
    loading.value = false
  }
}
</script>
