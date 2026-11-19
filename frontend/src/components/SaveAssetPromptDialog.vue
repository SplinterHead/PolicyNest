<template>
  <v-dialog v-model="open" max-width="480px" aria-labelledby="save-asset-prompt-title">
    <v-card rounded="lg">
      <v-card-title id="save-asset-prompt-title" class="pa-4 bg-surface-light d-flex align-center">
        <v-icon :icon="iconName" class="mr-2" color="primary" />
        Save {{ type }} to Inventory?
      </v-card-title>

      <v-card-text class="pt-4">
        <p class="text-body-medium mb-3">
          Saving this {{ type.toLowerCase() }} to your household inventory will make it quick to
          select on future policies and renewals without re-entering its details.
        </p>

        <v-sheet border rounded="md" class="pa-3 mb-4 bg-surface-light text-body-small">
          <template v-if="type === 'Vehicle'">
            <div v-if="details?.reg_number" class="d-flex justify-space-between">
              <span class="text-medium-emphasis">Registration</span>
              <span class="font-weight-bold">{{ details.reg_number }}</span>
            </div>
            <div v-if="details?.make_model" class="d-flex justify-space-between mt-1">
              <span class="text-medium-emphasis">Make / Model</span>
              <span class="font-weight-medium">{{ details.make_model }}</span>
            </div>
          </template>
          <template v-else>
            <div class="d-flex justify-space-between">
              <span class="text-medium-emphasis">Pet Name</span>
              <span class="font-weight-bold">{{ details?.pet_name }}</span>
            </div>
          </template>
        </v-sheet>

        <v-alert v-if="errorMessage" type="error" variant="tonal" density="compact" class="mb-3">
          {{ errorMessage }}
        </v-alert>

        <v-form v-model="valid" @submit.prevent="handleSave">
          <v-text-field
            v-model="entityName"
            :label="type === 'Pet' ? 'Pet Name' : 'Vehicle Nickname'"
            :placeholder="type === 'Pet' ? 'e.g. Bella' : 'e.g. Family Car'"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-tag-text"
            :rules="[(v) => !!(v && v.trim()) || 'Name is required to save to inventory']"
            autofocus
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4 pt-0">
        <v-btn variant="text" :disabled="saving" @click="handleSkip">
          Skip &amp; Save Policy Only
        </v-btn>
        <v-spacer />
        <v-btn
          color="primary"
          variant="flat"
          :loading="saving"
          :disabled="!valid || !entityName.trim()"
          @click="handleSave"
        >
          Save to Inventory
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
  type: { type: String, required: true },
  householdId: Number,
  details: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['saved', 'skip'])

const entityName = ref('')
const valid = ref(false)
const saving = ref(false)
const errorMessage = ref('')

const iconName = computed(() => (props.type === 'Pet' ? 'mdi-paw' : 'mdi-car'))

watch(open, (isOpen) => {
  if (!isOpen) return
  errorMessage.value = ''
  if (props.type === 'Pet') {
    entityName.value = (props.details?.pet_name || '').trim()
  } else {
    entityName.value = (props.details?.make_model || props.details?.reg_number || '').trim()
  }
})

function handleSkip() {
  open.value = false
  emit('skip')
}

async function handleSave() {
  if (!entityName.value.trim() || !props.householdId) return
  saving.value = true
  errorMessage.value = ''

  const makeModel = (props.details?.make_model || '').trim()
  const parts = makeModel ? makeModel.split(/\s+/) : []
  const assetDetails =
    props.type === 'Vehicle'
      ? {
          make: parts[0] || '',
          model: parts.slice(1).join(' '),
          reg: (props.details?.reg_number || '').trim(),
          vin: '',
        }
      : {
          species: '',
          breed: '',
          color: '',
          chip_id: '',
        }

  const formData = new FormData()
  formData.append('household_id', props.householdId)
  formData.append('name', entityName.value.trim())
  formData.append('type', props.type)
  formData.append('details', JSON.stringify(assetDetails))

  try {
    const res = await api.post('/assets/', formData)
    open.value = false
    emit('saved', res.data)
  } catch (e) {
    console.error('Failed to save asset to inventory', e)
    errorMessage.value = 'Could not save to inventory. Please try again or skip.'
  } finally {
    saving.value = false
  }
}
</script>
