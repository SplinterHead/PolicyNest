<template>
  <v-app>
    <v-navigation-drawer v-if="initialized" v-model="drawer" color="grey-lighten-5">
      <div class="pa-2">
        <v-menu location="bottom">
          <template v-slot:activator="{ props }">
            <v-card
              v-bind="props"
              color="primary"
              elevation="0"
              rounded="lg"
              class="pa-3 cursor-pointer"
              v-ripple
            >
              <div class="d-flex align-center justify-space-between">
                <div class="d-flex align-center overflow-hidden">
                  <v-avatar color="white" size="36" class="mr-3 text-primary">
                    <span class="text-subtitle-2 font-weight-bold">
                      {{ currentHousehold ? currentHousehold.name.charAt(0) : 'H' }}
                    </span>
                  </v-avatar>
                  <div class="text-truncate">
                    <div class="text-caption text-blue-lighten-4 font-weight-bold">HOUSEHOLD</div>
                    <div class="text-subtitle-2 font-weight-bold text-white text-truncate">
                      {{ currentHousehold ? currentHousehold.name : 'Select...' }}
                    </div>
                  </div>
                </div>
                <v-icon color="white" icon="mdi-chevron-down" size="small"></v-icon>
              </div>
            </v-card>
          </template>

          <v-list density="compact" nav class="mt-2">
            <v-list-subheader>Switch Household</v-list-subheader>

            <v-list-item
              v-for="h in households"
              :key="h.id"
              :value="h.id"
              @click="switchHousehold(h)"
              :active="currentHousehold && currentHousehold.id === h.id"
              color="primary"
            >
              <template v-slot:prepend>
                <v-icon
                  :icon="
                    currentHousehold && currentHousehold.id === h.id
                      ? 'mdi-check'
                      : 'mdi-home-outline'
                  "
                ></v-icon>
              </template>
              <v-list-item-title>{{ h.name }}</v-list-item-title>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item
              prepend-icon="mdi-cog-outline"
              title="Manage Households"
              @click="manageDialog = true"
            ></v-list-item>
          </v-list>
        </v-menu>
      </div>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-file-document-multiple"
          title="Policies"
          value="policies"
          active
          color="primary"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-chart-pie"
          title="Reports"
          value="reports"
          disabled
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="white" elevation="1">
      <v-app-bar-nav-icon v-if="initialized" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title class="text-primary font-weight-bold">
        <v-icon icon="mdi-shield-check" class="mr-2"></v-icon>
        PolicyNest
      </v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container fluid class="pa-6">
        <div v-if="initialized && currentHousehold">
          <v-row class="mb-4" align="center">
            <v-col>
              <div class="text-caption text-grey">DASHBOARD</div>
              <h1 class="text-h4 font-weight-thin">{{ currentHousehold.name }}</h1>
            </v-col>
            <v-col cols="auto">
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                size="large"
                @click="policyDialog = true"
              >
                Add Policy
              </v-btn>
            </v-col>
          </v-row>

          <v-card elevation="2" rounded="lg">
            <v-data-table :headers="headers" :items="policies" :loading="loading" hover>
              <template v-slot:item.type="{ item }">
                <v-chip
                  :color="getTypeColor(item.type)"
                  size="small"
                  variant="flat"
                  class="font-weight-bold"
                >
                  {{ item.type }}
                </v-chip>
              </template>
              <template v-slot:item.premium="{ item }">
                <strong>${{ item.premium.toFixed(2) }}</strong>
              </template>
              <template v-slot:item.document_path="{ item }">
                <v-btn
                  v-if="item.document_path"
                  size="small"
                  variant="tonal"
                  color="primary"
                  prepend-icon="mdi-file-pdf-box"
                  :href="getDocumentUrl(item.document_path)"
                  target="_blank"
                >
                  View
                </v-btn>
                <span v-else class="text-caption text-grey">No Doc</span>
              </template>
            </v-data-table>
          </v-card>
        </div>

        <div
          v-else-if="checkingStatus"
          class="d-flex justify-center align-center"
          style="height: 70vh"
        >
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </div>
      </v-container>
    </v-main>

    <v-dialog v-model="showOnboarding" persistent max-width="450px">
      <v-card class="text-center pa-6 rounded-xl">
        <div class="mb-4">
          <v-avatar color="primary" size="80">
            <v-icon icon="mdi-home-plus" size="40" color="white"></v-icon>
          </v-avatar>
        </div>
        <h2 class="text-h5 font-weight-bold mb-2">Welcome</h2>
        <p class="text-body-2 text-grey mb-6">Create your first household to get started.</p>
        <v-text-field
          v-model="newHouseholdName"
          label="Household Name"
          variant="outlined"
          @keyup.enter="createHousehold(true)"
        ></v-text-field>
        <v-btn
          block
          color="black"
          size="large"
          class="mt-2"
          rounded="lg"
          @click="createHousehold(true)"
          :loading="creatingHousehold"
        >
          Get Started
        </v-btn>
      </v-card>
    </v-dialog>

    <v-dialog v-model="manageDialog" max-width="500px">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Manage Households</v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-list lines="one" class="bg-grey-lighten-5 rounded-lg mb-4" border>
            <v-list-item v-for="h in households" :key="h.id" :title="h.name">
              <template v-slot:prepend>
                <v-icon icon="mdi-home" color="grey"></v-icon>
              </template>
              <template v-slot:append>
                <v-chip
                  v-if="currentHousehold && h.id === currentHousehold.id"
                  size="x-small"
                  color="success"
                  >Active</v-chip
                >
              </template>
            </v-list-item>
          </v-list>

          <div class="text-subtitle-2 mb-2">Create New Household</div>
          <div class="d-flex">
            <v-text-field
              v-model="newHouseholdName"
              label="Name"
              variant="outlined"
              density="compact"
              hide-details
              class="mr-2"
            ></v-text-field>
            <v-btn
              color="primary"
              height="40"
              @click="createHousehold(false)"
              :loading="creatingHousehold"
              >Add</v-btn
            >
          </div>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="manageDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="policyDialog" max-width="600px">
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-primary text-white">New Policy</v-card-title>
        <v-card-text class="pt-4">
          <v-form ref="form" @submit.prevent="submitPolicy">
            <v-row dense>
              <v-col cols="12" sm="6"
                ><v-text-field
                  v-model="form.provider"
                  label="Provider"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field
              ></v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="form.type"
                  :items="['Car', 'Home', 'Life', 'Medical', 'Pet']"
                  label="Type"
                  variant="outlined"
                  density="comfortable"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6"
                ><v-text-field
                  type="date"
                  v-model="form.start_date"
                  label="Start Date"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field
              ></v-col>
              <v-col cols="12" sm="6"
                ><v-text-field
                  type="date"
                  v-model="form.end_date"
                  label="End Date"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field
              ></v-col>
              <v-col cols="12"
                ><v-text-field
                  type="number"
                  step="0.01"
                  v-model="form.premium"
                  label="Premium Cost"
                  variant="outlined"
                  density="comfortable"
                  prefix="$"
                ></v-text-field
              ></v-col>
              <v-col cols="12">
                <v-file-input
                  @change="handleFileUpload"
                  label="Policy Document (PDF)"
                  variant="outlined"
                  density="comfortable"
                  accept=".pdf"
                  prepend-icon=""
                  prepend-inner-icon="mdi-paperclip"
                ></v-file-input>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="policyDialog = false">Cancel</v-btn>
          <v-btn color="primary" variant="flat" @click="submitPolicy" :loading="submitting"
            >Save Policy</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      // UI State
      drawer: null,
      checkingStatus: true,
      initialized: false,
      showOnboarding: false,
      manageDialog: false,
      policyDialog: false,

      // Data State
      households: [], // List of all households
      currentHousehold: null, // Currently selected
      policies: [],

      // Forms
      newHouseholdName: '',
      creatingHousehold: false,
      loading: false,
      submitting: false,

      // Table Config
      headers: [
        { title: 'Provider', key: 'provider', align: 'start' },
        { title: 'Type', key: 'type' },
        { title: 'Start Date', key: 'start_date' },
        { title: 'End Date', key: 'end_date' },
        { title: 'Premium', key: 'premium' },
        { title: 'Document', key: 'document_path', sortable: false },
      ],
      form: { provider: '', type: null, start_date: '', end_date: '', premium: '' },
      file: null,
    }
  },
  methods: {
    async loadApp() {
      // 1. Fetch all households
      try {
        const res = await axios.get('http://localhost:8000/households/')
        this.households = res.data

        if (this.households.length > 0) {
          this.initialized = true
          // Default to the first one, or stay on current if valid
          if (!this.currentHousehold) {
            this.switchHousehold(this.households[0])
          }
        } else {
          // No households exist, trigger onboarding
          this.showOnboarding = true
        }
      } catch (e) {
        console.error('Connection error', e)
      } finally {
        this.checkingStatus = false
      }
    },

    async switchHousehold(household) {
      this.currentHousehold = household
      this.fetchPolicies()
    },

    async createHousehold(isOnboarding) {
      if (!this.newHouseholdName) return
      this.creatingHousehold = true
      try {
        let formData = new FormData()
        formData.append('name', this.newHouseholdName)
        const res = await axios.post('http://localhost:8000/households/', formData)

        // Add to list and select it
        this.households.push(res.data)
        this.switchHousehold(res.data)

        this.newHouseholdName = '' // Reset form
        this.initialized = true

        if (isOnboarding) this.showOnboarding = false
        // Keep manage dialog open if used from there, but clear input
      } catch (e) {
        console.error(e)
      } finally {
        this.creatingHousehold = false
      }
    },

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

    async submitPolicy() {
      if (!this.form.provider || !this.form.premium) return
      this.submitting = true
      let formData = new FormData()
      formData.append('household_id', this.currentHousehold.id)
      formData.append('provider', this.form.provider)
      formData.append('type', this.form.type)
      formData.append('start_date', this.form.start_date)
      formData.append('end_date', this.form.end_date)
      formData.append('premium', this.form.premium)
      if (this.file) formData.append('file', this.file)

      try {
        await axios.post('http://localhost:8000/policies/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        this.fetchPolicies()
        this.policyDialog = false
        this.form = { provider: '', type: null, start_date: '', end_date: '', premium: '' }
        this.file = null
      } catch (e) {
        console.error('Error upload', e)
      } finally {
        this.submitting = false
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0]
    },
    getTypeColor(type) {
      const colors = { Car: 'blue', Home: 'orange', Life: 'green', Medical: 'red', Pet: 'purple' }
      return colors[type] || 'grey'
    },
    getDocumentUrl(path) {
      if (!path) return '#'
      const filename = path.split('/').pop()
      return `http://localhost:8000/uploads/${filename}`
    },
  },
  mounted() {
    this.loadApp()
  },
}
</script>
