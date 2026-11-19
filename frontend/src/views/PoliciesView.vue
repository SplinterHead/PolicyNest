<template>
  <div v-if="currentHousehold">
    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-headline-large font-weight-light">Policies</h1>
      </v-col>
    </v-row>

    <v-fab app color="primary" location="right bottom" size="large" style="z-index: 900" icon>
      <v-icon :icon="openFab ? 'mdi-close' : 'mdi-plus'" />
      <v-speed-dial
        v-model="openFab"
        location="top left"
        transition="slide-y-reverse-transition"
        activator="parent"
        scrim
        :activator-props="{ 'aria-label': openFab ? 'Close new policy menu' : 'Add policy' }"
      >
        <v-btn
          v-for="(config, type) in PolicyTypes"
          :key="type"
          :color="config.colour"
          :prepend-icon="config.icon"
          density="default"
          rounded="xl"
          size="large"
          width="160"
          class="justify-start px-4"
          @click="openPolicyDialog(type)"
        >
          {{ config.label }}
        </v-btn>
      </v-speed-dial>
    </v-fab>

    <div v-if="!loading && policies.length === 0" class="text-center mt-12 text-medium-emphasis">
      <v-icon icon="mdi-shield-off-outline" size="64" class="mb-4" />
      <div class="text-title-large">No policies yet</div>
      <div class="mb-4">Add your first policy to track renewals, cover details, and documents.</div>
      <v-menu>
        <template #activator="{ props: menuProps }">
          <v-btn
            v-bind="menuProps"
            color="primary"
            variant="flat"
            prepend-icon="mdi-plus"
            append-icon="mdi-chevron-down"
          >
            Add Policy
          </v-btn>
        </template>

        <v-list density="compact" role="menu" aria-label="Policy types">
          <v-list-item
            v-for="(config, type) in PolicyTypes"
            :key="type"
            role="menuitem"
            :prepend-icon="config.icon"
            :title="config.label"
            @click="openPolicyDialog(type)"
          />
        </v-list>
      </v-menu>
    </div>

    <template v-else>
      <div class="mb-6">
        <div class="d-flex align-center mb-3">
          <v-icon color="success" icon="mdi-shield-check" class="mr-2 flex-shrink-0" />
          <h2 class="text-headline-small font-weight-light text-no-wrap flex-shrink-0">
            Active Policies
          </h2>
          <v-divider class="ml-4" />
        </div>

        <v-card
          v-if="!loading && activePolicies.length === 0"
          elevation="2"
          rounded="lg"
          class="pa-6 text-center text-medium-emphasis"
        >
          <div class="mb-4">No active policies</div>
          <v-menu>
            <template #activator="{ props: menuProps }">
              <v-btn
                v-bind="menuProps"
                color="primary"
                variant="flat"
                prepend-icon="mdi-plus"
                append-icon="mdi-chevron-down"
              >
                Add Policy
              </v-btn>
            </template>

            <v-list density="compact" role="menu" aria-label="Policy types">
              <v-list-item
                v-for="(config, type) in PolicyTypes"
                :key="type"
                role="menuitem"
                :prepend-icon="config.icon"
                :title="config.label"
                @click="openPolicyDialog(type)"
              />
            </v-list>
          </v-menu>
        </v-card>

        <PolicyList
          v-else
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

        <div class="d-flex align-center mb-3 text-medium-emphasis">
          <v-icon color="grey" icon="mdi-history" class="mr-2 flex-shrink-0" />
          <h2 class="text-headline-small font-weight-light text-no-wrap flex-shrink-0">
            Expired Policies
          </h2>
          <v-divider class="ml-4" />
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
    </template>

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
  assets: { type: Array, default: () => [] },
  currencyCode: String,
  currentHousehold: Object,
})

const emit = defineEmits(['asset-created'])

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
  openFab.value = false
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
  emit('asset-created', newAsset)
}

async function loadData() {
  if (!props.currentHousehold?.id) return
  loading.value = true
  try {
    const polRes = await api.get(`/policies/?household_id=${props.currentHousehold.id}`)
    policies.value = polRes.data
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
