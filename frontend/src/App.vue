<template>
  <v-app>
    <NavBar :is-dark="isDark" @toggle-drawer="drawer = !drawer" @toggle-theme="toggleTheme" />

    <NavDrawer
      v-if="initialized"
      v-model="drawer"
      :households="households"
      :current-household="currentHousehold"
      @switch-household="switchHousehold"
      @open-manage="manageDialog = true"
    />

    <v-main :class="isDark ? '' : 'bg-grey-lighten-4'">
      <v-container fluid class="pa-6">
        <div v-if="initialized && currentHousehold">
          <v-row class="mb-4" align="center">
            <v-col>
              <div class="text-caption text-medium-emphasis">DASHBOARD</div>
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

          <PolicyList :policies="policies" :loading="loadingPolicies" />
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

    <PolicyForm v-model="policyDialog" :loading="submittingPolicy" @submit="handlePolicySubmit" />

    <v-dialog v-model="showOnboarding" persistent max-width="450px">
      <v-card class="text-center pa-6 rounded-xl">
        <h2 class="text-h5 font-weight-bold mb-2">Welcome</h2>
        <v-text-field
          v-model="newHouseholdName"
          label="Household Name"
          variant="outlined"
          @keyup.enter="createHousehold(true)"
        ></v-text-field>
        <v-btn
          block
          color="primary"
          size="large"
          class="mt-2"
          rounded="lg"
          @click="createHousehold(true)"
          :loading="creatingHousehold"
          >Get Started</v-btn
        >
      </v-card>
    </v-dialog>

    <v-dialog v-model="manageDialog" max-width="500px">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Manage Households</v-card-title>
        <v-card-text class="pa-4">
          <v-list lines="one" border class="rounded-lg mb-4">
            <v-list-item v-for="h in households" :key="h.id" :title="h.name">
              <template v-slot:append
                ><v-chip v-if="currentHousehold?.id === h.id" size="x-small" color="success"
                  >Active</v-chip
                ></template
              >
            </v-list-item>
          </v-list>
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
        <v-card-actions
          ><v-spacer></v-spacer
          ><v-btn variant="text" @click="manageDialog = false">Close</v-btn></v-card-actions
        >
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios'
import NavBar from './components/NavBar.vue'
import NavDrawer from './components/NavDrawer.vue'
import PolicyList from './components/PolicyList.vue'
import PolicyForm from './components/PolicyForm.vue'

export default {
  components: { NavBar, NavDrawer, PolicyList, PolicyForm },
  data() {
    return {
      drawer: null,
      checkingStatus: true,
      initialized: false,
      showOnboarding: false,
      manageDialog: false,
      policyDialog: false,

      households: [],
      currentHousehold: null,
      policies: [],

      newHouseholdName: '',
      creatingHousehold: false,
      loadingPolicies: false,
      submittingPolicy: false,
    }
  },
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  methods: {
    toggleTheme() {
      this.$vuetify.theme.global.name = this.isDark ? 'light' : 'dark'
    },
    async loadApp() {
      try {
        const res = await axios.get('http://localhost:8000/households/')
        this.households = res.data
        if (this.households.length > 0) {
          this.initialized = true
          if (!this.currentHousehold) this.switchHousehold(this.households[0])
        } else {
          this.showOnboarding = true
        }
      } catch (e) {
        console.error(e)
      } finally {
        this.checkingStatus = false
      }
    },
    async switchHousehold(household) {
      this.currentHousehold = household
      this.loadingPolicies = true
      try {
        const res = await axios.get(
          `http://localhost:8000/policies/?household_id=${this.currentHousehold.id}`,
        )
        this.policies = res.data
      } catch (e) {
        console.error(e)
      } finally {
        this.loadingPolicies = false
      }
    },
    async createHousehold(isOnboarding) {
      if (!this.newHouseholdName) return
      this.creatingHousehold = true
      try {
        let formData = new FormData()
        formData.append('name', this.newHouseholdName)
        const res = await axios.post('http://localhost:8000/households/', formData)
        this.households.push(res.data)
        this.switchHousehold(res.data)
        this.newHouseholdName = ''
        this.initialized = true
        if (isOnboarding) this.showOnboarding = false
      } catch (e) {
        console.error(e)
      } finally {
        this.creatingHousehold = false
      }
    },
    async handlePolicySubmit(payload) {
      this.submittingPolicy = true
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
        this.switchHousehold(this.currentHousehold) // Refresh list
        this.policyDialog = false
      } catch (e) {
        console.error(e)
      } finally {
        this.submittingPolicy = false
      }
    },
  },
  mounted() {
    this.loadApp()
  },
}
</script>
