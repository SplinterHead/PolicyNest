<template>
  <div v-if="currentHousehold">
    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-h4 font-weight-thin">Policies</h1>
      </v-col>
    </v-row>

    <v-fab app="true" color="primary" location="right bottom" size="large" icon>
      <v-icon :icon="openFab ? 'mdi-close' : 'mdi-plus'" />
      <v-speed-dial
        v-model="openFab"
        location="top left"
        transition="slide-y-reverse-transition"
        activator="parent"
      >
        <v-btn
          v-for="(config, type) in createOptions"
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
        <h2 class="text-h6 font-weight-bold">Active Policies</h2>
      </div>

      <PolicyList
        :currency-code="currencyCode"
        :policies="activePolicies"
        :loading="loading"
        @edit="openEditDialog"
        @delete="handleDelete"
        @upload="handleUpload"
      />
    </div>

    <div v-if="expiredPolicies.length > 0" class="mb-6">
      <v-divider class="my-6" />

      <div class="d-flex align-center mb-2 text-medium-emphasis">
        <v-icon color="grey" icon="mdi-history" class="mr-2" />
        <h2 class="text-h6 font-weight-bold">Expired Policies</h2>
      </div>

      <PolicyList
        :currency-code="currencyCode"
        :policies="expiredPolicies"
        :loading="loading"
        @edit="openEditDialog"
        @delete="handleDelete"
        @upload="handleUpload"
      />
    </div>

    <PolicyForm
      v-model="policyDialog"
      :assets="assets"
      :currency-code="currencyCode"
      :loading="submitting"
      :policy-to-edit="selectedPolicy"
      :policy-type="policyDialogType"
      @submit="handlePolicySubmit"
    />
  </div>
</template>

<script>
import api from '@/services/api'
import { POLICY_THEME } from '@/utils/PolicyStyles'
import PolicyList from '@/components/PolicyList.vue'
import PolicyForm from '@/components/PolicyForm.vue'

export default {
  name: 'PoliciesView',
  components: { PolicyList, PolicyForm },
  props: {
    currencyCode: String,
    currentHousehold: Object,
  },
  data() {
    return {
      policies: [],
      assets: [],
      loading: false,
      policyDialog: false,
      policyDialogType: null,
      submitting: false,
      selectedPolicy: null,
      openFab: false,
      policyTheme: POLICY_THEME,
    }
  },
  watch: {
    currentHousehold: {
      immediate: true,
      deep: true,
      handler(newVal) {
        if (newVal && newVal.id) {
          this.loadData()
        }
      },
    },
    policyDialog(val) {
      if (!val) this.selectedPolicy = null
    },
  },
  computed: {
    activePolicies() {
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      return this.policies.filter((p) => {
        if (!p.end_date) return true
        return new Date(p.end_date) >= today
      })
    },
    createOptions() {
      return this.policyTheme
    },
    expiredPolicies() {
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      return this.policies.filter((p) => {
        if (!p.end_date) return false
        return new Date(p.end_date) < today
      })
    },
  },
  methods: {
    openPolicyDialog(type) {
      this.policyDialogType = type
      this.policyDialog = true
    },
    openEditDialog(policy) {
      this.selectedPolicy = policy
      this.policyDialog = true
    },
    async loadData() {
      if (!this.currentHousehold) return
      this.loading = true
      try {
        const [polRes, assetRes] = await Promise.all([
          api.get(`/policies/?household_id=${this.currentHousehold.id}`),
          api.get(`/assets/?household_id=${this.currentHousehold.id}`),
        ])
        this.policies = polRes.data
        this.assets = assetRes.data
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    async handlePolicySubmit(payload) {
      this.submitting = true
      let formData = new FormData()
      formData.append('household_id', this.currentHousehold.id)
      formData.append('provider', payload.provider)
      formData.append('policy_number', payload.policy_number)
      formData.append('type', payload.type)
      formData.append('start_date', payload.start_date)
      formData.append('end_date', payload.end_date)
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
        this.loadData()
        this.policyDialog = false
        this.selectedPolicy = null
      } catch (e) {
        console.error(e)
      } finally {
        this.submitting = false
      }
    },
    async handleDelete(id) {
      try {
        await api.delete(`/policies/${id}`)
        this.loadData()
      } catch (e) {
        console.error('Delete failed', e)
      }
    },
  },
  mounted() {
    if (this.currentHousehold && this.currentHousehold.id) {
      this.loadData()
    }
  },
}
</script>
