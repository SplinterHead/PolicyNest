<template>
  <div v-if="currentHousehold">
    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-headline-large font-weight-thin">Policies</h1>
      </v-col>
    </v-row>

    <v-fab app color="primary" location="right bottom" size="large" icon>
      <v-icon :icon="openFab ? 'mdi-close' : 'mdi-plus'" />
      <v-speed-dial
        v-model="openFab"
        location="top left"
        transition="slide-y-reverse-transition"
        activator="parent"
      >
        <v-btn
          v-for="(config, type) in PolicyTypes"
          :key="type"
          :color="config.colour"
          :prepend-icon="config.icon"
          density="default"
          rounded="xl"
          size="large"
          @click="openPolicyDialog(type)"
        >
          {{ config.label }}
        </v-btn>
      </v-speed-dial>
    </v-fab>

    <div class="mb-6">
      <div class="d-flex align-center mb-2">
        <v-icon color="success" icon="mdi-shield-check" class="mr-2" />
        <h2 class="text-title-large font-weight-bold">Active Policies</h2>
      </div>

      <PolicyList
        :currency-code="currencyCode"
        :policies="activePolicies"
        :loading="loading"
        @edit="openEditDialog"
        @delete="handleDelete"
        @uploaded="handleDocumentUploaded"
      />
    </div>

    <div v-if="expiredPolicies.length > 0" class="mb-6">
      <v-divider class="my-6" />

      <div class="d-flex align-center mb-2 text-medium-emphasis">
        <v-icon color="grey" icon="mdi-history" class="mr-2" />
        <h2 class="text-title-large font-weight-bold">Expired Policies</h2>
      </div>

      <PolicyList
        :currency-code="currencyCode"
        :policies="expiredPolicies"
        :loading="loading"
        @edit="openEditDialog"
        @delete="handleDelete"
        @uploaded="handleDocumentUploaded"
      />
    </div>

    <PolicyForm
      v-model="policyDialog"
      :assets="assets"
      :currency-code="currencyCode"
      :household-id="currentHousehold?.id"
      :loading="submitting"
      :policy-to-edit="selectedPolicy"
      :policy-type="policyDialogType"
      @asset-created="handleAssetCreated"
      @submit="handlePolicySubmit"
    />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import api from '@/services/api'
import { parseIsoDate } from '@/utils/Formats'
import { PolicyTypes } from '@/utils/PolicyTypes'
import PolicyList from '@/components/PolicyList.vue'
import PolicyForm from '@/components/PolicyForm.vue'

const props = defineProps({
  currencyCode: String,
  currentHousehold: Object,
})

const assets = ref([])
const loading = ref(false)
const openFab = ref(false)
const policies = ref([])
const policyDialog = ref(false)
const policyDialogType = ref(null)
const selectedPolicy = ref(null)
const submitting = ref(false)

const activePolicies = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return policies.value.filter((p) => {
    if (!p.end_date) return true
    const endDate = parseIsoDate(p.end_date)
    return !endDate || endDate >= today
  })
})

const expiredPolicies = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return policies.value.filter((p) => {
    if (!p.end_date) return false
    const endDate = parseIsoDate(p.end_date)
    return endDate && endDate < today
  })
})

function openPolicyDialog(type) {
  selectedPolicy.value = null
  policyDialogType.value = type
  policyDialog.value = true
}

function openEditDialog(policy) {
  selectedPolicy.value = policy
  policyDialogType.value = policy.type
  policyDialog.value = true
}

function handleDocumentUploaded(updatedPolicy) {
  const index = policies.value.findIndex((p) => p.id === updatedPolicy.id)
  if (index !== -1) {
    policies.value[index] = updatedPolicy
  }
}

function handleAssetCreated(newAsset) {
  if (newAsset && !assets.value.some((a) => a.id === newAsset.id)) {
    assets.value.push(newAsset)
  }
}

async function loadData() {
  if (!props.currentHousehold?.id) return
  loading.value = true
  try {
    const [polRes, assetRes] = await Promise.all([
      api.get(`/policies/?household_id=${props.currentHousehold.id}`),
      api.get(`/assets/?household_id=${props.currentHousehold.id}`),
    ])
    policies.value = polRes.data
    assets.value = assetRes.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handlePolicySubmit(payload) {
  submitting.value = true
  const formData = new FormData()
  formData.append('household_id', props.currentHousehold.id)
  formData.append('provider', payload.provider)
  if (payload.policy_number) {
    formData.append('policy_number', payload.policy_number)
  }
  formData.append('type', payload.type)
  formData.append('start_date', payload.start_date)
  if (payload.end_date) {
    formData.append('end_date', payload.end_date)
  }
  formData.append('premium', payload.premium)
  formData.append('attributes', payload.attributes)
  if (payload.asset_id) formData.append('asset_id', payload.asset_id)
  if (payload.file) formData.append('file', payload.file)

  try {
    if (payload.id) {
      await api.put(`/policies/${payload.id}`, formData)
    } else {
      await api.post('/policies/', formData)
    }
    await loadData()
    policyDialog.value = false
    selectedPolicy.value = null
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id) {
  try {
    await api.delete(`/policies/${id}`)
    await loadData()
  } catch (e) {
    console.error('Delete failed', e)
  }
}

watch(
  () => props.currentHousehold?.id,
  (newId) => {
    if (newId) {
      loadData()
    }
  },
  { immediate: true },
)

watch(policyDialog, (val) => {
  if (!val) {
    selectedPolicy.value = null
  }
})
</script>
