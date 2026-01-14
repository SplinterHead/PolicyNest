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

    <PolicyList :policies="policies" :loading="loading" />

    <PolicyForm v-model="policyDialog" :loading="submitting" @submit="handlePolicySubmit" />
  </div>
</template>

<script>
import axios from 'axios'
import PolicyList from '../components/PolicyList.vue'
import PolicyForm from '../components/PolicyForm.vue'

export default {
  name: 'PoliciesView',
  components: { PolicyList, PolicyForm },
  props: {
    currentHousehold: Object, // Received from App.vue
  },
  data() {
    return {
      policies: [],
      loading: false,
      policyDialog: false,
      submitting: false,
    }
  },
  watch: {
    // Re-fetch if the user switches household in the parent App.vue
    currentHousehold: {
      immediate: true, // Run on load
      handler(newVal) {
        if (newVal) this.fetchPolicies()
      },
    },
  },
  methods: {
    async fetchPolicies() {
      if (!this.currentHousehold) return
      this.loading = true
      try {
        const res = await axios.get(
          `http://localhost:8000/policies/?household_id=${this.currentHousehold.id}`,
        )
        this.policies = res.data
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
      if (payload.file) formData.append('file', payload.file)

      try {
        await axios.post('http://localhost:8000/policies/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        this.fetchPolicies()
        this.policyDialog = false
      } catch (e) {
        console.error(e)
      } finally {
        this.submitting = false
      }
    },
  },
}
</script>
