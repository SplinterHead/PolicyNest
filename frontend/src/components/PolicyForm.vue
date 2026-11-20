<template>
  <v-dialog
    id="policy-form-dialog"
    v-model="open"
    max-width="600px"
    scrollable
    aria-labelledby="policy-form-title"
  >
    <v-defaults-provider
      :defaults="{
        VMenu: { attach: '#policy-form-dialog' },
        VTooltip: { attach: '#policy-form-dialog' },
      }"
    >
      <v-card rounded="lg">
        <v-card-title id="policy-form-title" class="pa-4 bg-primary d-flex align-center">
          <v-icon v-if="policyIcon" :icon="policyIcon" class="mr-2" />
          {{
            policyToEdit
              ? policyLabel
                ? `Edit ${policyLabel} Policy`
                : 'Edit Policy'
              : policyLabel
                ? `New ${policyLabel} Policy`
                : 'New Policy'
          }}
          <v-spacer />
          <v-icon-btn icon="mdi-close" variant="text" aria-label="Close" @click="open = false" />
        </v-card-title>

        <v-card-text class="pt-4 policy-form-scroll" style="max-height: 80vh">
          <v-form ref="formRef" validate-on="submit lazy" @submit.prevent="submit">
            <v-row density="compact">
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.provider"
                  label="Provider *"
                  variant="outlined"
                  density="comfortable"
                  required
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
                  v-model:menu="startDateMenu"
                  label="Start Date *"
                  :input-format="isIsoDateLocale ? 'yyyy-mm-dd' : undefined"
                  prepend-icon=""
                  prepend-inner-icon="mdi-calendar"
                  variant="outlined"
                  density="comfortable"
                  required
                  :rules="[(v) => !!v || 'Start date is required']"
                  @keydown.enter="startDateMenu = false"
                />
              </v-col>
              <v-col cols="12" sm="6">
                <v-date-input
                  v-model="form.end_date"
                  v-model:menu="endDateMenu"
                  label="End Date"
                  :input-format="isIsoDateLocale ? 'yyyy-mm-dd' : undefined"
                  prepend-icon=""
                  prepend-inner-icon="mdi-calendar"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  @keydown.enter="endDateMenu = false"
                >
                  <template #append-inner>
                    <v-tooltip text="Leave empty for perpetual policy" location="top" open-on-click>
                      <template #activator="{ props: tooltipProps }">
                        <v-icon-btn
                          v-bind="tooltipProps"
                          icon="mdi-information-outline"
                          size="small"
                          variant="text"
                          aria-label="End date information"
                          @mousedown.stop
                          @click.stop
                        />
                      </template>
                    </v-tooltip>
                  </template>
                </v-date-input>
              </v-col>
              <v-col cols="12" sm="8">
                <v-text-field
                  v-model="form.premium"
                  label="Premium Cost *"
                  variant="outlined"
                  density="comfortable"
                  :prefix="currencySymbol"
                  persistent-placeholder
                  type="number"
                  min="0"
                  step="0.01"
                  required
                  :rules="[
                    (v) => (v !== '' && v !== null && v !== undefined) || 'Premium is required',
                    (v) => Number(v) >= 0 || 'Premium cannot be negative',
                  ]"
                />
              </v-col>
              <v-col cols="12" sm="4">
                <v-select
                  v-model="form.frequency"
                  :items="['Annual', 'Monthly']"
                  label="Frequency"
                  variant="outlined"
                  density="comfortable"
                />
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
                  @add-asset="openInlineAssetDialog('Vehicle')"
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
                  @add-asset="openInlineAssetDialog('Pet')"
                />
              </v-col>

              <v-col cols="12">
                <v-file-input
                  v-model="file"
                  accept=".pdf"
                  label="Policy Document"
                  placeholder="PDF files only"
                  hint="Accepted format: PDF (.pdf)"
                  persistent-hint
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
          <v-btn
            color="primary"
            variant="flat"
            :disabled="loading"
            :loading="loading"
            @click="submit"
          >
            Save Policy
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-defaults-provider>

    <AssetDialog
      v-model="showInlineAssetDialog"
      :type="inlineAssetType"
      :household-id="householdId"
      @saved="handleInlineAssetCreated"
    />

    <SaveAssetPromptDialog
      v-model="showSaveAssetPrompt"
      :type="pendingAssetType"
      :household-id="householdId"
      :details="form.attributes"
      @saved="handlePromptAssetSaved"
      @skip="handlePromptAssetSkipped"
    />
  </v-dialog>
</template>

<script setup>
import { computed, nextTick, ref, useTemplateRef, watch } from 'vue'
import { isIsoDateLocale, parseIsoDate, toIsoDate } from '@/utils/Formats'
import { PolicyTypes, getPolicyIcon } from '@/utils/PolicyTypes'
import AssetDialog from '@/components/AssetDialog.vue'
import SaveAssetPromptDialog from '@/components/SaveAssetPromptDialog.vue'
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
  householdId: Number,
  loading: Boolean,
  policyToEdit: Object,
  policyType: String,
})

const emit = defineEmits(['submit', 'asset-created'])

const formRef = useTemplateRef('formRef')
const file = ref(null)
const form = ref(createEmptyForm())
const startDateMenu = ref(false)
const endDateMenu = ref(false)
const showInlineAssetDialog = ref(false)
const inlineAssetType = ref('Vehicle')
const showSaveAssetPrompt = ref(false)
const pendingAssetType = ref('Vehicle')
const pendingSubmitStartDate = ref(null)

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

const policyIcon = computed(() => getPolicyIcon(form.value.type))
const policyLabel = computed(() => PolicyTypes[form.value.type]?.label || form.value.type || '')

const vehicleAssets = computed(() => props.assets.filter((a) => a.type === 'Vehicle'))
const petAssets = computed(() => props.assets.filter((a) => a.type === 'Pet'))

watch(open, (isOpen) => {
  startDateMenu.value = false
  endDateMenu.value = false
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
  nextTick(() => formRef.value?.resetValidation())
})

function openInlineAssetDialog(type) {
  inlineAssetType.value = type
  showInlineAssetDialog.value = true
}

function handleInlineAssetCreated(newAsset) {
  if (!newAsset) return
  emit('asset-created', newAsset)
  form.value.asset_id = newAsset.id
  if (newAsset.type === 'Vehicle') {
    form.value.attributes.reg_number = newAsset.details?.reg || ''
    form.value.attributes.make_model = [newAsset.details?.make, newAsset.details?.model]
      .filter(Boolean)
      .join(' ')
  } else if (newAsset.type === 'Pet') {
    form.value.attributes.pet_name = newAsset.name || ''
  }
}

function emitPolicySubmit(startDate) {
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

function handlePromptAssetSaved(newAsset) {
  if (newAsset) {
    emit('asset-created', newAsset)
    form.value.asset_id = newAsset.id
    if (newAsset.type === 'Pet') {
      form.value.attributes.pet_name = newAsset.name
    }
  }
  emitPolicySubmit(pendingSubmitStartDate.value)
}

function handlePromptAssetSkipped() {
  emitPolicySubmit(pendingSubmitStartDate.value)
}

async function submit() {
  const validation = await formRef.value?.validate()
  if (validation && !validation.valid) {
    const firstErrorId = validation.errors?.[0]?.id
    if (firstErrorId) {
      document.getElementById(firstErrorId)?.focus()
    }
    return
  }

  const startDate = toIsoDate(form.value.start_date)
  if (!form.value.provider || form.value.premium === '' || !startDate) return

  const isCarFreeText =
    form.value.type === 'Car' &&
    !form.value.asset_id &&
    Boolean(form.value.attributes?.reg_number?.trim() || form.value.attributes?.make_model?.trim())
  const isPetFreeText =
    form.value.type === 'Pet' &&
    !form.value.asset_id &&
    Boolean(form.value.attributes?.pet_name?.trim())

  if ((isCarFreeText || isPetFreeText) && props.householdId) {
    pendingSubmitStartDate.value = startDate
    pendingAssetType.value = form.value.type === 'Car' ? 'Vehicle' : 'Pet'
    showSaveAssetPrompt.value = true
    return
  }

  emitPolicySubmit(startDate)
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

.policy-form-scroll {
  overflow-y: auto;
  scrollbar-gutter: stable;
  container-type: scroll-state;
}

.policy-form-scroll::before,
.policy-form-scroll::after {
  content: '';
  display: block;
  position: sticky;
  block-size: 0.75rem;
  z-index: 2;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.policy-form-scroll::before {
  inset-block-start: 0;
  margin-block-end: -0.75rem;
  background: radial-gradient(farthest-side at 50% 0, rgb(0 0 0 / 0.16), transparent);
}

.policy-form-scroll::after {
  inset-block-end: 0;
  margin-block-start: -0.75rem;
  background: radial-gradient(farthest-side at 50% 100%, rgb(0 0 0 / 0.16), transparent);
}

@container scroll-state(scrollable: block-start) {
  .policy-form-scroll::before {
    opacity: 1;
  }
}

@container scroll-state(scrollable: block-end) {
  .policy-form-scroll::after {
    opacity: 1;
  }
}

@supports not (container-type: scroll-state) {
  .policy-form-scroll::before,
  .policy-form-scroll::after {
    animation: show-scroll-shadow linear both;
    animation-timeline: scroll();
  }

  .policy-form-scroll::before {
    animation-range: 0 2rem;
  }

  .policy-form-scroll::after {
    animation-direction: reverse;
    animation-range: calc(100% - 2rem) 100%;
  }
}

@supports not ((container-type: scroll-state) or (animation-timeline: scroll())) {
  .policy-form-scroll {
    background:
      linear-gradient(rgb(var(--v-theme-surface)) 30%, transparent) top / 100% 2.5rem no-repeat
        local,
      linear-gradient(transparent, rgb(var(--v-theme-surface)) 70%) bottom / 100% 2.5rem no-repeat
        local,
      radial-gradient(farthest-side at 50% 0, rgb(0 0 0 / 0.16), transparent) top / 100% 0.75rem
        no-repeat,
      radial-gradient(farthest-side at 50% 100%, rgb(0 0 0 / 0.16), transparent) bottom / 100%
        0.75rem no-repeat,
      rgb(var(--v-theme-surface));
  }
}

@keyframes show-scroll-shadow {
  to {
    opacity: 1;
  }
}
</style>
