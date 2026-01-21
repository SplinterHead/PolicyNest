<template>
  <v-app>
    <NavBar :is-dark="isDark" @toggle-drawer="drawer = !drawer" @toggle-theme="toggleTheme" />

    <NavDrawer
      v-if="initialized"
      v-model="drawer"
      :households="households"
      :current-household="currentHousehold"
      @switch-household="switchHousehold"
      @open-manage="showManageDialog = true"
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

    <NewHouseholdDialog
      v-model="showOnboarding"
      :show-cancel="false"
      @complete="handleNewHousehold"
    />

    <ManageHouseholdsDialog
      v-model="showManageDialog"
      :households="households"
      :current-id="currentHousehold?.id"
      @select="switchHousehold"
      @created="handleNewHousehold"
      @deleted="handleDeletedHousehold"
    />
  </v-app>
</template>

<script>
import api from '@/services/api'
import NavBar from '@/components/NavBar.vue'
import NavDrawer from '@/components/NavDrawer.vue'
import NewHouseholdDialog from '@/components/NewHouseholdDialog.vue'
import ManageHouseholdsDialog from '@/components/ManageHouseholdsDialog.vue'

export default {
  components: {
    ManageHouseholdsDialog,
    NavBar,
    NavDrawer,
    NewHouseholdDialog,
  },
  data() {
    return {
      checkingStatus: true,
      currencyCode: 'GBP',
      currentHousehold: null,
      drawer: null,
      households: [],
      initialized: false,
      showManageDialog: false,
      showOnboarding: false,
    }
  },
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  methods: {
    handleNewHousehold(newHousehold) {
      this.households.push(newHousehold)
      this.switchHousehold(newHousehold)
      this.showOnboarding = false
      this.showManageDialog = false
      this.initialized = true
    },
    handleDeletedHousehold(delHousehold) {
      this.households = this.households.filter((household) => household.id !== delHousehold.id)
      if (this.currentHousehold.id === delHousehold.id) {
        this.switchHousehold(this.households[0])
      }
      this.showOnboarding = false
      this.showManageDialog = false
      this.initialized = true
    },
    switchHousehold(household) {
      this.currentHousehold = household
      this.showManageDialog = false
    },
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
      this.loading = true
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) this.$vuetify.theme.global.name = savedTheme
      const savedCurrencyCode = localStorage.getItem('currencyCode')
      if (savedCurrencyCode) this.updateCurrency(savedCurrencyCode)

      try {
        const res = await api.get('/households/')
        this.households = res.data
        if (this.households.length > 0) {
          this.initialized = true
          if (!this.currentHousehold) this.currentHousehold = this.households[0]
          this.showOnboarding = false
        } else {
          this.currentHousehold = null
          this.showOnboarding = true
        }
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
        this.checkingStatus = false
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
