<template>
  <div v-if="currentHousehold">
    <v-row class="mb-4" align="center">
      <v-col>
        <div class="text-caption text-medium-emphasis">DASHBOARD</div>
        <h1 class="text-h4 font-weight-thin">{{ currentHousehold.name }}</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" size="large" @click="policyDialog = true">
          Add Policy
        </v-btn>
      </v-col>
    </v-row>

    <PolicyList
      :currency-code="currencyCode"
      :loading="loading"
      :policies="policies"
      @edit="openEditDialog"
      @delete="handleDelete"
    />

    <PolicyForm
      v-model="policyDialog"
      :assets="assets"
      :currency-code="currencyCode"
      :loading="submitting"
      :policy-to-edit="selectedPolicy"
      @submit="handlePolicySubmit"
    />
  </div>
</template>

<script>
import api from '../services/api'
import PolicyList from '../components/PolicyList.vue'
import PolicyForm from '../components/PolicyForm.vue'

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
      submitting: false,
      selectedPolicy: null,
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
  methods: {
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
