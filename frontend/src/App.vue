<template>
  <v-app>
    <NavBar
      :is-dark="isDark"
      :drawer-open="isDrawerOpen"
      :households="households"
      :current-household="currentHousehold"
      @toggle-drawer="drawer = !isDrawerOpen"
      @toggle-theme="toggleTheme"
      @switch-household="switchHousehold"
      @open-manage="showManageDialog = true"
    />

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
        <router-view v-if="initialized" v-slot="{ Component, route }">
          <component
            :is="Component"
            :current-household="currentHousehold"
            :currency-code="currencyCode"
            v-bind="route.name === 'settings' ? { themePreference } : {}"
            @update-currency="updateCurrency"
            @update-theme="setThemePreference"
            @open-manage="showManageDialog = true"
          />
        </router-view>

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
      @updated="handleUpdatedHousehold"
      @deleted="handleDeletedHousehold"
    />
  </v-app>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useDisplay, useTheme } from 'vuetify'
import api from '@/services/api'
import NavBar from '@/components/NavBar.vue'
import NavDrawer from '@/components/NavDrawer.vue'
import NewHouseholdDialog from '@/components/NewHouseholdDialog.vue'
import ManageHouseholdsDialog from '@/components/ManageHouseholdsDialog.vue'

const { mobile } = useDisplay()
const theme = useTheme()

const checkingStatus = ref(true)
const currencyCode = ref('GBP')
const currentHousehold = ref(null)
const drawer = ref(null)
const households = ref([])
const initialized = ref(false)
const showManageDialog = ref(false)
const showOnboarding = ref(false)
const themePreference = ref('system')

const isDark = computed(() => theme.current.value.dark)
const isDrawerOpen = computed(() => (drawer.value === null ? !mobile.value : Boolean(drawer.value)))

function getStoredTheme() {
  try {
    const val = localStorage.getItem('theme')
    return val === 'light' || val === 'dark' ? val : null
  } catch {
    return null
  }
}

function applyTheme(stored) {
  themePreference.value = stored ?? 'system'
  theme.change(stored ?? 'system')
  const meta = document.querySelector('meta[name="color-scheme"]')
  if (meta) {
    meta.content = stored ?? 'light dark'
  }
}

function setThemePreference(pref) {
  if (pref === 'system') {
    try {
      localStorage.removeItem('theme')
    } catch {
      // Ignore storage failures
    }
    applyTheme(null)
  } else if (pref === 'light' || pref === 'dark') {
    try {
      localStorage.setItem('theme', pref)
    } catch {
      // Ignore storage failures
    }
    applyTheme(pref)
  }
}

function toggleTheme() {
  const target = isDark.value ? 'light' : 'dark'
  const systemScheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'

  setThemePreference(target === systemScheme ? 'system' : target)
}

function handleStorage(event) {
  if (event.key === 'theme' || event.key === null) {
    applyTheme(getStoredTheme())
  }
  if (event.key === 'currencyCode' && event.newValue) {
    currencyCode.value = event.newValue
  }
}

function updateCurrency(newVal) {
  currencyCode.value = newVal
  try {
    localStorage.setItem('currencyCode', newVal)
  } catch {
    // Ignore storage failures
  }
}

function switchHousehold(household) {
  currentHousehold.value = household
  showManageDialog.value = false
}

function handleNewHousehold(newHousehold) {
  households.value.push(newHousehold)
  switchHousehold(newHousehold)
  showOnboarding.value = false
  showManageDialog.value = false
  initialized.value = true
}

function handleUpdatedHousehold(updatedHousehold) {
  households.value = households.value.map((household) =>
    household.id === updatedHousehold.id ? updatedHousehold : household,
  )
  if (currentHousehold.value?.id === updatedHousehold.id) {
    currentHousehold.value = updatedHousehold
  }
}

function handleDeletedHousehold(delHousehold) {
  households.value = households.value.filter((household) => household.id !== delHousehold.id)
  if (households.value.length === 0) {
    currentHousehold.value = null
    initialized.value = false
    showManageDialog.value = false
    showOnboarding.value = true
    return
  }

  if (currentHousehold.value?.id === delHousehold.id) {
    switchHousehold(households.value[0])
  }
  showOnboarding.value = false
  showManageDialog.value = false
  initialized.value = true
}

async function loadApp() {
  applyTheme(getStoredTheme())
  try {
    const savedCurrencyCode = localStorage.getItem('currencyCode')
    if (savedCurrencyCode) {
      currencyCode.value = savedCurrencyCode
    }
  } catch {
    // Ignore storage failures
  }

  try {
    const res = await api.get('/households/')
    households.value = res.data
    if (households.value.length > 0) {
      initialized.value = true
      if (!currentHousehold.value) {
        currentHousehold.value = households.value[0]
      }
      showOnboarding.value = false
    } else {
      currentHousehold.value = null
      showOnboarding.value = true
    }
  } catch (e) {
    console.error(e)
  } finally {
    checkingStatus.value = false
  }
}

onMounted(() => {
  window.addEventListener('storage', handleStorage)
  loadApp()
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', handleStorage)
})
</script>

<style>
:root {
  color-scheme: light dark;
  --v-font-heading: 'Montserrat', sans-serif;

  &:has(> head > meta[name='color-scheme'][content='dark']) {
    color-scheme: dark;
  }

  &:has(> head > meta[name='color-scheme'][content='light']) {
    color-scheme: light;
  }
}

body {
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    sans-serif;
  line-height: 1.5;
}

.v-card-title,
.v-app-bar-title {
  font-family: var(--v-font-heading);
}

.v-btn--disabled.v-btn--variant-flat,
.v-btn--disabled.v-btn--variant-elevated {
  background-color: rgba(var(--v-theme-on-surface), 0.14);
  color: rgba(var(--v-theme-on-surface), 0.5);
}

.v-btn--disabled.v-btn--variant-flat .v-btn__overlay,
.v-btn--disabled.v-btn--variant-elevated .v-btn__overlay {
  opacity: 0;
}
</style>
