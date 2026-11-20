<template>
  <v-dialog v-model="open" width="80%" scrollable aria-labelledby="policy-details-title">
    <v-card v-if="policy" rounded="lg">
      <v-toolbar :color="getPolicyColour(policy.type)">
        <template #prepend>
          <div class="ml-4">
            <v-icon :icon="getPolicyIcon(policy.type)" />
          </div>
        </template>
        <v-toolbar-title id="policy-details-title" class="font-weight-bold">
          {{ policy.provider }}
          <span v-if="policy.policy_number" class="text-title-small ml-2 opacity-80">
            Policy No. {{ policy.policy_number }}
          </span>
        </v-toolbar-title>
        <v-spacer />
        <v-icon-btn icon="mdi-close" variant="text" aria-label="Close" @click="open = false" />
      </v-toolbar>

      <v-card-text
        class="pa-0 d-flex flex-column"
        :class="isDark ? 'bg-grey-darken-4' : 'bg-grey-lighten-5'"
        style="height: 85dvh"
      >
        <div class="pa-6 d-flex flex-column ga-4 policy-details-body">
          <div class="flex-shrink-0">
            <v-row density="compact">
              <v-col cols="12" md="4">
                <v-card variant="flat" class="pa-4 border bg-surface h-100">
                  <div class="text-body-small text-medium-emphasis mb-1">Premium</div>
                  <div class="text-headline-small font-weight-bold text-primary">
                    {{ currencyFormat(policy.premium, currencyCode) }}
                  </div>
                  <div class="text-body-small mt-1">
                    {{
                      policy.attributes?.payment_frequency === 'Monthly' ? 'Per Month' : 'Per Year'
                    }}
                  </div>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card variant="flat" class="pa-4 border bg-surface h-100">
                  <div class="text-body-small text-medium-emphasis mb-1">Policy Start</div>
                  <div class="text-title-large">{{ formatDate(policy.start_date, 'N/A') }}</div>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card variant="flat" class="pa-4 border bg-surface h-100">
                  <div class="text-body-small text-medium-emphasis mb-1">Policy Renewal</div>
                  <div class="text-title-large" :class="getRenewalColor(policy.end_date)">
                    {{ formatDate(policy.end_date, 'Perpetual') }}
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </div>

          <v-card class="pa-4 bg-surface flex-shrink-0" border variant="flat">
            <div class="text-title-medium font-weight-bold mb-3 d-flex align-center">
              <v-icon icon="mdi-list-box-outline" class="mr-2" color="primary" />
              Policy Details
            </div>

            <div>
              <v-row density="compact">
                <BuildingsPolicyDetails
                  v-if="policy.type === 'Buildings'"
                  :attributes="policy.attributes"
                  :currency-code="currencyCode"
                />
                <CarPolicyDetails
                  v-if="policy.type === 'Car'"
                  :asset="linkedAsset"
                  :attributes="policy.attributes"
                  :currency-code="currencyCode"
                />
                <ContentsPolicyDetails
                  v-if="policy.type === 'Contents'"
                  :attributes="policy.attributes"
                  :currency-code="currencyCode"
                />
                <LifePolicyDetails
                  v-if="policy.type === 'Life'"
                  :attributes="policy.attributes"
                  :currency-code="currencyCode"
                />
                <MedicalPolicyDetails
                  v-if="policy.type === 'Medical'"
                  :attributes="policy.attributes"
                  :currency-code="currencyCode"
                />
                <PetPolicyDetails
                  v-if="policy.type === 'Pet'"
                  :attributes="policy.attributes"
                  :currency-code="currencyCode"
                />
              </v-row>
            </div>
          </v-card>

          <section class="d-flex flex-column policy-doc-section">
            <div class="text-title-medium font-weight-bold mb-2 flex-shrink-0">Policy Document</div>

            <v-alert
              v-if="uploadError"
              type="error"
              variant="tonal"
              density="compact"
              closable
              class="mb-3 flex-shrink-0"
              @click:close="uploadError = ''"
            >
              {{ uploadError }}
            </v-alert>

            <v-card
              v-if="policy.document_path"
              border
              class="d-flex flex-column overflow-hidden bg-white policy-pdf-card"
            >
              <object
                :data="getFileUrl(policy.document_path)"
                type="application/pdf"
                class="policy-pdf-object"
              >
                <div
                  class="d-flex flex-column align-center justify-center text-center text-black flex-grow-1 pa-4"
                >
                  <v-icon icon="mdi-file-pdf-box" size="64" color="grey" />
                  <div class="mt-2">Preview not supported.</div>
                  <v-btn
                    color="primary"
                    class="mt-4"
                    :href="getFileUrl(policy.document_path)"
                    target="_blank"
                  >
                    Download PDF
                  </v-btn>
                </div>
              </object>
            </v-card>

            <v-file-upload
              v-else
              :model-value="selectedUpload"
              accept=".pdf"
              filter-by-type=".pdf,application/pdf"
              icon="mdi-cloud-upload"
              title="No Document Uploaded"
              subtitle="Drag & Drop a PDF here, or click to browse"
              :loading="isUploading"
              :disabled="isUploading"
              clearable
              hide-details
              class="policy-upload"
              @update:model-value="handleFileUpload"
              @rejected="handleFileRejected"
            />
          </section>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useTheme } from 'vuetify'
import api, { getFileUrl } from '@/services/api'
import { currencyFormat, formatDate, parseIsoDate } from '@/utils/Formats'
import { getPolicyColour, getPolicyIcon } from '@/utils/PolicyTypes'

import BuildingsPolicyDetails from '@/components/details/BuildingsPolicyDetails.vue'
import CarPolicyDetails from '@/components/details/CarPolicyDetails.vue'
import ContentsPolicyDetails from '@/components/details/ContentsPolicyDetails.vue'
import LifePolicyDetails from '@/components/details/LifePolicyDetails.vue'
import MedicalPolicyDetails from '@/components/details/MedicalPolicyDetails.vue'
import PetPolicyDetails from '@/components/details/PetPolicyDetails.vue'

const open = defineModel({ type: Boolean })

const props = defineProps({
  assets: { type: Array, default: () => [] },
  currencyCode: String,
  policy: Object,
})

const emit = defineEmits(['edit', 'uploaded'])

const theme = useTheme()
const isDark = computed(() => theme.current.value.dark)
const linkedAsset = computed(
  () => props.assets.find((asset) => asset.id === props.policy?.asset_id) || null,
)

const isUploading = ref(false)
const selectedUpload = ref(null)
const uploadError = ref('')

watch(open, (val) => {
  if (!val) {
    selectedUpload.value = null
    uploadError.value = ''
  }
})

function getRenewalColor(dateStr) {
  const endDate = parseIsoDate(dateStr)
  if (!endDate) return 'text-grey'

  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const daysLeft = (endDate - today) / (1000 * 60 * 60 * 24)
  if (daysLeft < 0) return 'text-red font-weight-bold'
  if (daysLeft < 30) return 'text-orange font-weight-bold'
  return 'text-success'
}

function handleFileRejected() {
  uploadError.value = 'Please upload a PDF file.'
}

function handleFileUpload(fileOrFiles) {
  const file = Array.isArray(fileOrFiles) ? fileOrFiles[0] : fileOrFiles
  if (file) {
    uploadError.value = ''
    uploadDocument(file)
  }
}

async function uploadDocument(file) {
  if (!props.policy?.id) return
  isUploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await api.put(`/policies/${props.policy.id}/document`, formData)
    emit('uploaded', res.data)
    selectedUpload.value = null
  } catch (e) {
    console.error('Upload failed', e)
    uploadError.value = 'Failed to upload document.'
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
.policy-details-body {
  flex: 1 0 auto;
}

.policy-doc-section {
  flex: 1 0 auto;
}

.policy-pdf-card {
  flex: 1 0 auto;
  min-height: 280px;
}

.policy-pdf-object {
  flex: 1 1 0;
  inline-size: 100%;
  min-block-size: 280px;
  display: block;
}

.policy-upload {
  flex: 1 0 auto;
}

.policy-upload :deep(.v-file-upload-dropzone) {
  flex: 1 1 auto;
  min-block-size: 220px;
  padding-block: 32px;
}
</style>
