<template>
  <v-app>
    <v-navigation-drawer v-if="initialized" v-model="drawer" color="grey-lighten-5">
      <div class="pa-4">
        <v-card color="primary" elevation="0" rounded="lg" class="pa-3">
          <div class="d-flex align-center">
            <v-avatar color="white" size="40" class="mr-3">
              <v-icon color="primary">mdi-home-variant</v-icon>
            </v-avatar>
            <div class="text-truncate">
              <div class="text-caption text-blue-lighten-4 font-weight-bold">HOUSEHOLD</div>
              <div class="text-subtitle-2 font-weight-bold text-white">
                {{ currentHousehold ? currentHousehold.name : '...' }}
              </div>
            </div>
          </div>
        </v-card>
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
          prepend-icon="mdi-cog"
          title="Settings"
          value="settings"
          disabled
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2 text-center text-caption text-grey">v0.1.0 Self-Hosted</div>
      </template>
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
        <div v-if="initialized">
          <v-row class="mb-4" align="center">
            <v-col>
              <h1 class="text-h4 font-weight-thin">Dashboard</h1>
            </v-col>
            <v-col cols="auto">
              <v-btn color="primary" prepend-icon="mdi-plus" size="large" @click="dialog = true">
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
        <h2 class="text-h5 font-weight-bold mb-2">Welcome Home</h2>
        <p class="text-body-2 text-grey mb-6">
          Let's set up your household to start tracking your policies safely.
        </p>

        <v-text-field
          v-model="householdName"
          label="Household Name"
          placeholder="e.g. The Smith Residence"
          variant="outlined"
          density="comfortable"
          bg-color="grey-lighten-5"
          @keyup.enter="createHousehold"
        ></v-text-field>

        <v-btn
          block
          color="black"
          size="large"
          class="mt-2"
          rounded="lg"
          @click="createHousehold"
          :loading="creatingHousehold"
        >
          Get Started
        </v-btn>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-primary text-white">
          <span class="text-h6">New Policy</span>
        </v-card-title>
        <v-card-text class="pt-4">
          <v-form ref="form" @submit.prevent="submitPolicy">
            <v-row dense>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.provider"
                  label="Provider"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="form.type"
                  :items="['Car', 'Home', 'Life', 'Medical', 'Pet']"
                  label="Type"
                  variant="outlined"
                  density="comfortable"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  type="date"
                  v-model="form.start_date"
                  label="Start Date"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  type="date"
                  v-model="form.end_date"
                  label="End Date"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  type="number"
                  step="0.01"
                  v-model="form.premium"
                  label="Premium Cost"
                  variant="outlined"
                  density="comfortable"
                  prefix="$"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-file-input
                  @change="handleFileUpload"
                  label="Policy Document (PDF)"
                  variant="outlined"
                  density="comfortable"
                  prepend-icon=""
                  prepend-inner-icon="mdi-paperclip"
                  accept=".pdf"
                ></v-file-input>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
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
      // App State
      drawer: null, // Null allows Vuetify to automatically handle mobile/desktop states
      checkingStatus: true,
      initialized: false,
      showOnboarding: false,
      currentHousehold: null,

      // Onboarding State
      householdName: '',
      creatingHousehold: false,

      // Dashboard State
      dialog: false,
      loading: false,
      submitting: false,
      policies: [],
      headers: [
        { title: 'Provider', key: 'provider', align: 'start' },
        { title: 'Type', key: 'type' },
        { title: 'Start Date', key: 'start_date' },
        { title: 'End Date', key: 'end_date' },
        { title: 'Premium', key: 'premium' },
        { title: 'Document', key: 'document_path', sortable: false },
      ],
      form: {
        provider: '',
        type: null,
        start_date: '',
        end_date: '',
        premium: '',
      },
      file: null,
    }
  },
  methods: {
    async checkSystemStatus() {
      try {
        const res = await axios.get('http://localhost:8000/system/status')
        if (res.data.initialized) {
          this.initialized = true
          this.currentHousehold = res.data.household
          this.fetchPolicies()
        } else {
          this.showOnboarding = true
        }
      } catch (e) {
        console.error('Connection error', e)
      } finally {
        this.checkingStatus = false
      }
    },
    async createHousehold() {
      if (!this.householdName) return
      this.creatingHousehold = true
      try {
        let formData = new FormData()
        formData.append('name', this.householdName)
        const res = await axios.post('http://localhost:8000/households/', formData)

        this.currentHousehold = res.data
        this.initialized = true
        this.showOnboarding = false
        this.fetchPolicies()
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
      if (this.file) {
        formData.append('file', this.file)
      }

      try {
        await axios.post('http://localhost:8000/policies/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        this.fetchPolicies()
        this.dialog = false
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
    this.checkSystemStatus()
  },
}
</script>
