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
        <router-view
          v-if="initialized"
          :current-household="currentHousehold"
          :currency-code="currencyCode"
          @update-currency="updateCurrency"
        />

        <div
          v-else-if="checkingStatus"
          class="d-flex justify-center align-center"
          style="height: 70vh"
        >
          <v-progress-circular indeterminate color="primary" size="64" />
        </div>
      </v-container>
    </v-main>

    <v-dialog v-model="showOnboarding" persistent max-width="450px">
      <v-card class="text-center pa-6 rounded-xl">
        <h2 class="text-h5 font-weight-bold mb-2">Welcome</h2>
        <v-text-field
          v-model="newHouseholdName"
          label="Household Name"
          variant="outlined"
          @keyup.enter="createHousehold(true)"
        />
        <v-btn
          block
          color="primary"
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
        <v-card-text class="pa-4">
          <v-list lines="one" border class="rounded-lg mb-4">
            <v-list-item v-for="h in households" :key="h.id" :title="h.name">
              <template v-slot:subtitle v-if="currentHousehold?.id === h.id">
                <span class="text-success font-weight-bold text-caption">Currently Active</span>
              </template>

              <template v-slot:append>
                <v-btn
                  v-if="currentHousehold?.id !== h.id"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="switchHousehold(h)"
                  >Switch</v-btn
                >

                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="grey"
                  class="ml-2"
                  @click="confirmDeleteHousehold(h)"
                ></v-btn>
              </template>
            </v-list-item>
          </v-list>

          <div class="d-flex">
            <v-text-field
              v-model="newHouseholdName"
              label="New Household Name"
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

    <v-dialog v-model="deleteHouseholdDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5 text-red">Delete Household?</v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ householdToDelete?.name }}</strong
          >? <br /><br />
          <v-alert type="warning" variant="tonal" density="compact" border="start">
            This will permanently delete all
            <strong>Policies, Assets, and Documents</strong> associated with this household.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="deleteHouseholdDialog = false">Cancel</v-btn>
          <v-btn
            color="red"
            variant="flat"
            @click="executeDeleteHousehold"
            :loading="deletingHousehold"
            >Delete Forever</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios'
import NavBar from './components/NavBar.vue'
import NavDrawer from './components/NavDrawer.vue'

export default {
  components: { NavBar, NavDrawer },
  data() {
    return {
      checkingStatus: true,
      creatingHousehold: false,
      currencyCode: 'GBP',
      currentHousehold: null,
      deleteHouseholdDialog: false,
      deletingHousehold: false,
      drawer: null,
      households: [],
      householdToDelete: null,
      initialized: false,
      manageDialog: false,
      newHouseholdName: '',
      showOnboarding: false,
    }
  },
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  methods: {
    toggleTheme() {
      const newTheme = this.isDark ? 'light' : 'dark'
      this.$vuetify.theme.global.name = newTheme
      localStorage.setItem('theme', newTheme)
    },
    updateCurrency(newVal) {
      this.currencyCode = newVal
      localStorage.setItem('currencyCode', newVal)
    },
    async loadApp() {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) this.$vuetify.theme.global.name = savedTheme
      const savedCurrencyCode = localStorage.getItem('currencyCode')
      if (savedCurrencyCode) this.updateCurrency(savedCurrencyCode)

      try {
        const res = await axios.get('http://localhost:8000/households/')
        this.households = res.data
        if (this.households.length > 0) {
          this.initialized = true
          if (!this.currentHousehold) this.currentHousehold = this.households[0]
        } else {
          this.showOnboarding = true
        }
      } catch (e) {
        console.error(e)
      } finally {
        this.checkingStatus = false
      }
    },
    switchHousehold(household) {
      this.currentHousehold = household
      this.manageDialog = false
    },
    confirmDeleteHousehold(household) {
      this.householdToDelete = household
      this.deleteHouseholdDialog = true
    },
    async executeDeleteHousehold() {
      if (!this.householdToDelete) return
      this.deletingHousehold = true
      try {
        await axios.delete(`http://localhost:8000/households/${this.householdToDelete.id}`)
        this.households = this.households.filter((h) => h.id !== this.householdToDelete.id)
        if (this.currentHousehold && this.currentHousehold.id === this.householdToDelete.id) {
          if (this.households.length > 0) {
            this.switchHousehold(this.households[0])
          } else {
            this.currentHousehold = null
            this.showOnboarding = true
            this.manageDialog = false
          }
        }

        this.deleteHouseholdDialog = false
        this.householdToDelete = null
      } catch (e) {
        console.error('Failed to delete household', e)
        alert('Could not delete household. Ensure all policies are removed or try again.')
      } finally {
        this.deletingHousehold = false
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
  },
  mounted() {
    this.loadApp()
  },
}
</script>

<style>
:root {
  --title-font: 'Montserrat', sans-serif;
}

.v-application .text-h1,
.v-application .text-h2,
.v-application .text-h3,
.v-application .text-h4,
.v-application .text-h5,
.v-application .text-h6,
.v-card-title,
.v-app-bar-title {
  font-family: var(--title-font) !important;
}
</style>
