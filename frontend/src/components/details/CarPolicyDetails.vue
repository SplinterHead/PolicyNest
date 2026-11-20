<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-car" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Vehicle</v-list-item-title>
        <template #append>
          <div class="d-flex align-center ga-2">
            <span v-if="vehicleMake" class="font-weight-medium">{{ vehicleMake }}</span>
            <v-chip
              label
              size="small"
              variant="outlined"
              class="reg-plate text-uppercase font-weight-bold"
            >
              {{ attributes.reg_number || 'N/A' }}
            </v-chip>
          </div>
        </template>
      </v-list-item>
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-shield-half-full" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Cover Level</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">{{ attributes.cover_level }}</span>
        </template>
      </v-list-item>
      <v-list-item v-if="attributes.class_of_use">
        <template #prepend>
          <v-icon icon="mdi-road-variant" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Class of Use</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">{{ attributes.class_of_use }}</span>
        </template>
      </v-list-item>
      <v-list-item
        v-if="
          attributes.annual_mileage !== undefined &&
          attributes.annual_mileage !== null &&
          attributes.annual_mileage !== ''
        "
      >
        <template #prepend>
          <v-icon icon="mdi-speedometer" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Annual Mileage</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">{{ formattedMileage }}</span>
        </template>
      </v-list-item>
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Total Excess</v-list-item-title>
        <template #append>
          <div class="text-right">
            <div class="font-weight-bold text-red">
              {{
                currencyFormat(
                  (attributes.excess_voluntary || 0) + (attributes.excess_compulsory || 0),
                  currencyCode,
                )
              }}
            </div>
            <div class="text-body-small text-medium-emphasis">
              {{ currencyFormat(attributes.excess_compulsory || 0, currencyCode) }} comp. +
              {{ currencyFormat(attributes.excess_voluntary || 0, currencyCode) }} vol.
            </div>
          </div>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <FeatureChips :items="features" :class="additionalDrivers.length > 0 ? 'mt-2 mb-4' : 'mt-2'" />

    <div v-if="additionalDrivers.length > 0">
      <div class="text-body-small font-weight-bold text-medium-emphasis mb-1">
        Additional Drivers
      </div>
      <v-card variant="outlined" class="bg-surface-light">
        <v-list density="compact" class="bg-transparent py-0">
          <v-list-item v-for="(driver, i) in additionalDrivers" :key="i" min-height="32">
            <template #prepend>
              <v-icon icon="mdi-account-outline" size="x-small" class="mr-2 text-medium-emphasis" />
            </template>
            <v-list-item-title class="text-body-small">{{ driver }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </div>
  </v-col>
</template>

<script setup>
import { computed } from 'vue'
import { currencyFormat, resolvedNumberLocale } from '@/utils/Formats'
import FeatureChips from '@/components/details/FeatureChips.vue'

const props = defineProps({
  asset: { type: Object, default: null },
  attributes: { type: Object, default: () => ({}) },
  currencyCode: String,
})

const vehicleMake = computed(
  () =>
    props.asset?.details?.make?.trim() ||
    props.attributes?.make?.trim() ||
    props.attributes?.make_model?.trim().split(/\s+/)[0] ||
    '',
)

const formattedMileage = computed(
  () =>
    `${new Intl.NumberFormat(resolvedNumberLocale.value).format(props.attributes.annual_mileage)} miles`,
)

const additionalDrivers = computed(() =>
  Array.isArray(props.attributes.additional_drivers)
    ? props.attributes.additional_drivers.map((d) => String(d).trim()).filter(Boolean)
    : [],
)

const features = computed(() => [
  { label: 'Courtesy Car', enabled: Boolean(props.attributes.courtesy_car) },
  { label: 'Legal Cover', enabled: Boolean(props.attributes.legal_cover) },
  { label: 'Breakdown', enabled: Boolean(props.attributes.breakdown) },
  { label: 'Windscreen', enabled: Boolean(props.attributes.windscreen) },
  { label: 'Protected NCD', enabled: Boolean(props.attributes.protected_ncd) },
  { label: 'Driving Other Cars', enabled: Boolean(props.attributes.driving_other_cars) },
  { label: 'Key Cover', enabled: Boolean(props.attributes.key_cover) },
])
</script>

<style scoped>
.reg-plate {
  font-family: monospace;
  letter-spacing: 0.06em;
}
</style>
