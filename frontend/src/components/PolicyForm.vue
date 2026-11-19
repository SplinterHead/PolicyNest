<template>
  <v-dialog v-model="open" max-width="600px" scrollable>
    <v-card rounded="lg">
      <v-card-title class="pa-4 bg-primary text-white">
        {{ policyToEdit ? 'Edit Policy' : 'New Policy' }}
      </v-card-title>

      <v-card-text class="pt-4" style="max-height: 80vh">
        <v-form ref="formRef" @submit.prevent="submit">
          <v-row density="compact">
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="form.provider"
                label="Provider"
                variant="outlined"
                density="comfortable"
                :rules="[(v) => !!v || 'Provider is required']"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="form.policy_number"
                label="Policy No."
                variant="outlined"
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-date-input
                v-model="form.start_date"
                label="Start Date"
                input-format="yyyy-mm-dd"
                prepend-icon=""
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                density="comfortable"
                :rules="[(v) => !!v || 'Start date is required']"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-date-input
                v-model="form.end_date"
                label="End Date"
                input-format="yyyy-mm-dd"
                prepend-icon=""
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                density="comfortable"
                clearable
                hint="Leave empty for perpetual policy"
                persistent-hint
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
                :rules="[
                  (v) => (v !== '' && v !== null && v !== undefined) || 'Premium is required',
                ]"
              >
                <template #append>
                  <v-select
                    v-model="form.frequency"
                    :items="['Annual', 'Monthly']"
                    variant="plain"
                    density="compact"
                    hide-details
                    width="120px"
                    class="font-weight-bold text-body-small"
                  />
                </template>
              </v-text-field>
            </v-col>

            <v-col cols="12">
              <BuildingsPolicyForm
                v-if="form.type === 'Buildings'"
                v-model="form.attributes"
                :currency-symbol="currencySymbol"
              />
              <CarPolicyForm
                v-else-if="form.type === 'Car'"
                v-model="form.attributes"
                v-model:asset-id="form.asset_id"
                :assets="vehicleAssets"
                :currency-symbol="currencySymbol"
              />
              <ContentsPolicyForm
                v-else-if="form.type === 'Contents'"
                v-model="form.attributes"
                :currency-symbol="currencySymbol"
              />
              <LifePolicyForm
                v-else-if="form.type === 'Life'"
                v-model="form.attributes"
                :currency-symbol="currencySymbol"
              />
              <MedicalPolicyForm
                v-else-if="form.type === 'Medical'"
                v-model="form.attributes"
                :currency-symbol="currencySymbol"
              />
              <PetPolicyForm
                v-else-if="form.type === 'Pet'"
                v-model="form.attributes"
                v-model:asset-id="form.asset_id"
                :assets="petAssets"
                :currency-symbol="currencySymbol"
              />
            </v-col>

            <v-col cols="12">
              <v-file-input
                v-model="file"
                accept=".pdf"
                label="Policy Document"
                placeholder="PDF files only"
                variant="outlined"
                density="comfortable"
                prepend-icon=""
                prepend-inner-icon="mdi-paperclip"
                clearable
                show-size
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-divider />
      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn variant="text" @click="open = false">Cancel</v-btn>
        <v-btn color="primary" variant="flat" :loading="loading" @click="submit">
          Save Policy
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, ref, useTemplateRef, watch } from 'vue'
import { parseIsoDate, toIsoDate } from '@/utils/Formats'
import BuildingsPolicyForm from '@/components/forms/BuildingsPolicyForm.vue'
import ContentsPolicyForm from '@/components/forms/ContentsPolicyForm.vue'
import CarPolicyForm from '@/components/forms/CarPolicyForm.vue'
import LifePolicyForm from '@/components/forms/LifePolicyForm.vue'
import MedicalPolicyForm from '@/components/forms/MedicalPolicyForm.vue'
import PetPolicyForm from '@/components/forms/PetPolicyForm.vue'

const open = defineModel({ type: Boolean })

const props = defineProps({
  assets: { type: Array, default: () => [] },
  currencyCode: String,
  loading: Boolean,
  policyToEdit: Object,
  policyType: String,
})

const emit = defineEmits(['submit'])

const formRef = useTemplateRef('formRef')
const file = ref(null)
const form = ref(createEmptyForm())

function createEmptyForm(type = null) {
  return {
    asset_id: null,
    type,
    provider: '',
    policy_number: '',
    start_date: null,
    end_date: null,
    premium: '',
    frequency: 'Annual',
    attributes: {},
  }
}

const currencySymbol = computed(() => {
  const symbols = { GBP: '£', USD: '$', EUR: '€', AUD: 'A$', CAD: 'C$' }
  return symbols[props.currencyCode] || '$'
})

const vehicleAssets = computed(() => props.assets.filter((a) => a.type === 'Vehicle'))
const petAssets = computed(() => props.assets.filter((a) => a.type === 'Pet'))

watch(open, (isOpen) => {
  if (!isOpen) return

  if (props.policyToEdit) {
    const clonedAttributes = JSON.parse(JSON.stringify(props.policyToEdit.attributes || {}))
    form.value = {
      ...props.policyToEdit,
      start_date: parseIsoDate(props.policyToEdit.start_date),
      end_date: parseIsoDate(props.policyToEdit.end_date),
      frequency: clonedAttributes.payment_frequency || 'Annual',
      attributes: clonedAttributes,
    }
  } else {
    form.value = createEmptyForm(props.policyType)
  }
  file.value = null
})

async function submit() {
  const validation = await formRef.value?.validate()
  if (validation && !validation.valid) return

  const startDate = toIsoDate(form.value.start_date)
  if (!form.value.provider || form.value.premium === '' || !startDate) return

  const finalAttributes = {
    ...form.value.attributes,
    payment_frequency: form.value.frequency,
  }

  emit('submit', {
    ...form.value,
    start_date: startDate,
    end_date: toIsoDate(form.value.end_date),
    attributes: JSON.stringify(finalAttributes),
    file: file.value,
    id: props.policyToEdit?.id,
  })
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
