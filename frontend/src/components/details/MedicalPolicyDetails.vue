<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-account-group" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Plan Type</v-list-item-title>
        <template #append>
          <v-chip size="small" color="blue" variant="flat" class="font-weight-bold">
            {{ attributes.cover_type || 'N/A' }}
          </v-chip>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-hospital-building" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Hospital List</v-list-item-title>
        <template #append>
          <span class="font-weight-medium text-body-small">
            {{ attributes.hospital_list || 'Standard' }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Annual Excess</v-list-item-title>
        <template #append>
          <span class="font-weight-bold text-red">
            {{ currencyFormat(attributes.excess, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-chart-timeline-variant" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Out-patient Limit</v-list-item-title>
        <template #append>
          <span v-if="attributes.outpatient_limit" class="font-weight-medium">
            {{ currencyFormat(attributes.outpatient_limit, currencyCode) }}
          </span>
          <v-chip v-else size="x-small" color="green" variant="tonal">Full Cover</v-chip>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">Benefits Included</div>
    <div class="d-flex flex-wrap ga-2">
      <v-chip :color="attributes.cancer_cover ? 'pink' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.cancer_cover ? 'mdi-ribbon' : 'mdi-close'" />
        Cancer Care
      </v-chip>
      <v-chip :color="attributes.mental_health ? 'teal' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.mental_health ? 'mdi-brain' : 'mdi-close'" />
        Mental Health
      </v-chip>
      <v-chip :color="attributes.therapies ? 'teal' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.therapies ? 'mdi-human-handsup' : 'mdi-close'" />
        Therapies
      </v-chip>
      <v-chip :color="attributes.dental ? 'teal' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.dental ? 'mdi-tooth' : 'mdi-close'" />
        Dental
      </v-chip>
      <v-chip :color="attributes.optical ? 'teal' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.optical ? 'mdi-eye' : 'mdi-close'" />
        Optical
      </v-chip>
      <v-chip :color="attributes.travel_cover ? 'teal' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.travel_cover ? 'mdi-airplane' : 'mdi-close'" />
        Travel
      </v-chip>
    </div>

    <div v-if="attributes.underwriting_type" class="mt-4">
      <div class="text-body-small text-medium-emphasis">Underwriting</div>
      <div class="text-body-medium">{{ attributes.underwriting_type }}</div>
    </div>
  </v-col>
</template>

<script setup>
import { currencyFormat } from '@/utils/Formats'

defineProps({
  attributes: { type: Object, default: () => ({}) },
  currencyCode: String,
})
</script>
