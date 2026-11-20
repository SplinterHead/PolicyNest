<template>
  <div>
    <v-row>
      <v-col>
        <h1 class="text-headline-large font-weight-light">Settings</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2" rounded="lg" class="pa-4 h-100">
          <h2 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
            <v-icon icon="mdi-earth" class="mr-2" />
            Localization
          </h2>

          <v-select
            :model-value="currencyCode"
            :items="currencies"
            item-title="label"
            item-value="code"
            label="Application Currency"
            variant="outlined"
            density="comfortable"
            class="mb-4"
            hint="Display format only (no exchange-rate conversion). Saved locally in this browser."
            persistent-hint
            @update:model-value="emit('update-currency', $event)"
          >
            <template #selection="{ item }">
              <span class="font-weight-bold mr-2">{{ item.symbol }}</span>
              <span>{{ item.label }}</span>
              <span class="text-medium-emphasis ml-1">({{ item.code }})</span>
            </template>
            <template #item="{ props: itemProps, item }">
              <v-list-item v-bind="itemProps" :subtitle="item.code">
                <template #prepend>
                  <span class="currency-symbol font-weight-bold text-center mr-3">
                    {{ item.symbol }}
                  </span>
                </template>
              </v-list-item>
            </template>
          </v-select>

          <v-select
            :model-value="localePreference"
            :items="localeOptions"
            item-title="label"
            item-value="code"
            label="Date & Number Format"
            variant="outlined"
            density="comfortable"
            :hint="localeSampleHint"
            persistent-hint
            @update:model-value="emit('update-locale', $event)"
          >
            <template #selection="{ item }">
              <span>{{ item.label }}</span>
              <span v-if="item.dateHint" class="text-medium-emphasis ml-1">
                ({{ item.dateHint }})
              </span>
            </template>
            <template #item="{ props: itemProps, item }">
              <v-list-item v-bind="itemProps" :subtitle="item.subtitle" />
            </template>
          </v-select>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="2" rounded="lg" class="pa-4 h-100">
          <h2
            id="appearance-heading"
            class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4"
          >
            <v-icon icon="mdi-theme-light-dark" class="mr-2" />
            Appearance
          </h2>

          <v-radio-group
            :model-value="themePreference"
            color="primary"
            hide-details
            aria-labelledby="appearance-heading"
            aria-describedby="appearance-hint"
            @update:model-value="emit('update-theme', $event)"
          >
            <v-radio
              value="system"
              :label="`System (Currently ${systemIsDark ? 'Dark' : 'Light'})`"
            />
            <v-radio value="light" label="Light" />
            <v-radio value="dark" label="Dark" />
          </v-radio-group>

          <p id="appearance-hint" class="text-body-small text-medium-emphasis mt-3 mb-0">
            Follows your device theme by default. Overrides are saved locally in this browser.
          </p>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="2" rounded="lg" class="pa-4 h-100">
          <h2 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
            <v-icon icon="mdi-home-group" class="mr-2" />
            Household
          </h2>

          <p class="text-body-medium mb-4">
            Currently active: <strong>{{ currentHousehold?.name }}</strong>
          </p>

          <v-btn
            color="primary"
            variant="tonal"
            prepend-icon="mdi-cog-outline"
            @click="emit('open-manage')"
          >
            Manage Households
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { SUPPORTED_LOCALES, currencyFormat, formatDate, getBrowserLocale } from '@/utils/Formats'

const props = defineProps({
  currencyCode: String,
  currentHousehold: Object,
  localePreference: {
    type: String,
    default: 'auto',
  },
  themePreference: {
    type: String,
    default: 'system',
  },
})

const emit = defineEmits(['update-currency', 'update-locale', 'update-theme', 'open-manage'])

const currencies = [
  { code: 'GBP', label: 'British Pound', symbol: '£' },
  { code: 'EUR', label: 'Euro', symbol: '€' },
  { code: 'USD', label: 'US Dollar', symbol: '$' },
  { code: 'AUD', label: 'Australian Dollar', symbol: 'A$' },
  { code: 'CAD', label: 'Canadian Dollar', symbol: 'C$' },
]

const SAMPLE_DATE = new Date(2026, 10, 20)
const SAMPLE_AMOUNT = 1234.5
const browserLocale = getBrowserLocale()

function formatSampleDate(loc) {
  if (loc === 'iso') return '2026-11-20'
  return new Intl.DateTimeFormat(loc, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(SAMPLE_DATE)
}

function formatSampleCurrency(loc) {
  return new Intl.NumberFormat(loc, {
    style: 'currency',
    currency: props.currencyCode || 'GBP',
    currencyDisplay: 'narrowSymbol',
  }).format(SAMPLE_AMOUNT)
}

const localeOptions = computed(() => [
  {
    code: 'auto',
    label: `Browser Default (${browserLocale})`,
    dateHint: '',
    subtitle: `${formatSampleDate(browserLocale)} · ${formatSampleCurrency(browserLocale)}`,
  },
  ...SUPPORTED_LOCALES.map((item) => ({
    ...item,
    subtitle: `${item.dateHint} · ${formatSampleDate(item.code)} · ${formatSampleCurrency(
      item.code === 'iso' ? browserLocale : item.code,
    )}`,
  })),
])

const localeSampleHint = computed(
  () =>
    `Preview: ${formatDate('2026-11-20')} · ${currencyFormat(SAMPLE_AMOUNT, props.currencyCode)}. Saved locally in this browser.`,
)

const systemIsDark = ref(
  typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-color-scheme: dark)').matches,
)
let colorSchemeQuery = null

function handleColorSchemeChange(event) {
  systemIsDark.value = event.matches
}

onMounted(() => {
  if (typeof window.matchMedia !== 'function') return
  colorSchemeQuery = window.matchMedia('(prefers-color-scheme: dark)')
  systemIsDark.value = colorSchemeQuery.matches
  colorSchemeQuery.addEventListener('change', handleColorSchemeChange)
})

onBeforeUnmount(() => {
  colorSchemeQuery?.removeEventListener('change', handleColorSchemeChange)
})
</script>

<style scoped>
.currency-symbol {
  display: inline-block;
  inline-size: 2rem;
}
</style>
