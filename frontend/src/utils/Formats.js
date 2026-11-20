import { computed, ref } from 'vue'

export const LOCALE_STORAGE_KEY = 'locale'

export const SUPPORTED_LOCALES = [
  { code: 'en-GB', label: 'English (UK)', dateHint: 'DD/MM/YYYY' },
  { code: 'en-US', label: 'English (US)', dateHint: 'MM/DD/YYYY' },
  { code: 'en-AU', label: 'English (Australia)', dateHint: 'DD/MM/YYYY' },
  { code: 'en-CA', label: 'English (Canada)', dateHint: 'YYYY-MM-DD' },
  { code: 'iso', label: 'ISO 8601 Date', dateHint: 'YYYY-MM-DD' },
  { code: 'de-DE', label: 'German (Germany)', dateHint: 'DD.MM.YYYY' },
  { code: 'fr-FR', label: 'French (France)', dateHint: 'DD/MM/YYYY' },
]

const VALID_LOCALE_CODES = new Set(SUPPORTED_LOCALES.map((item) => item.code))

export const getBrowserLocale = () => {
  if (typeof navigator !== 'undefined' && navigator.language) {
    return navigator.language
  }

  try {
    return Intl.DateTimeFormat().resolvedOptions().locale || 'en-GB'
  } catch {
    return 'en-GB'
  }
}

export const getStoredLocalePreference = () => {
  try {
    const val = localStorage.getItem(LOCALE_STORAGE_KEY)
    return val && VALID_LOCALE_CODES.has(val) ? val : 'auto'
  } catch {
    return 'auto'
  }
}

export const localePreference = ref(getStoredLocalePreference())

export const setLocalePreference = (pref) => {
  const next = pref && VALID_LOCALE_CODES.has(pref) ? pref : 'auto'
  localePreference.value = next

  try {
    if (next === 'auto') {
      localStorage.removeItem(LOCALE_STORAGE_KEY)
    } else {
      localStorage.setItem(LOCALE_STORAGE_KEY, next)
    }
  } catch {
    // Ignore storage failures
  }
}

export const syncLocalePreferenceFromStorage = () => {
  localePreference.value = getStoredLocalePreference()
}

export const resolvedNumberLocale = computed(() =>
  localePreference.value === 'auto' || localePreference.value === 'iso'
    ? getBrowserLocale()
    : localePreference.value,
)

export const resolvedDateLocale = computed(() =>
  localePreference.value === 'auto' ? getBrowserLocale() : localePreference.value,
)

export const vuetifyLocale = computed(() =>
  localePreference.value === 'iso' ? 'en-GB' : resolvedDateLocale.value,
)

export const isIsoDateLocale = computed(() => localePreference.value === 'iso')

export const currencyFormat = (value, code) => {
  if (value === undefined || value === null || value === '') return 'N/A'

  let currencyCode = code
  if (!currencyCode) {
    try {
      currencyCode = localStorage.getItem('currencyCode')
    } catch {
      currencyCode = null
    }
  }

  return new Intl.NumberFormat(resolvedNumberLocale.value, {
    style: 'currency',
    currency: currencyCode || 'GBP',
    currencyDisplay: 'narrowSymbol',
  }).format(value)
}

export const parseIsoDate = (isoStr) => {
  if (!isoStr) return null
  if (isoStr instanceof Date) return isoStr

  const match = String(isoStr).match(/^(\d{4})-(\d{2})-(\d{2})/)
  if (match) {
    const [, year, month, day] = match
    return new Date(Number(year), Number(month) - 1, Number(day))
  }

  const parsed = new Date(isoStr)
  return Number.isNaN(parsed.getTime()) ? null : parsed
}

export const toIsoDate = (value) => {
  if (!value) return null
  if (typeof value === 'string') {
    const match = value.match(/^(\d{4}-\d{2}-\d{2})/)
    if (match) return match[1]
  }

  const date = value instanceof Date ? value : parseIsoDate(value)
  if (!date || Number.isNaN(date.getTime())) return null

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export const formatDate = (isoStr, emptyLabel = '') => {
  if (localePreference.value === 'iso') {
    return toIsoDate(isoStr) || emptyLabel
  }

  const date = parseIsoDate(isoStr)
  if (!date) return emptyLabel

  return new Intl.DateTimeFormat(resolvedDateLocale.value, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date)
}
