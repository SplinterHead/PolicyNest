<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-hammer-wrench" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Rebuild Cost</v-list-item-title>
        <template #append>
          <span class="font-weight-bold">
            {{ currencyFormat(attributes.rebuild_cost, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-bed" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Alt. Accommodation</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">
            {{ currencyFormat(attributes.alternative_accommodation, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Standard Excess</v-list-item-title>
        <template #append>
          <span class="font-weight-bold text-red">
            {{ currencyFormat(attributes.excess_standard, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-alert-box-outline" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Subsidence Excess</v-list-item-title>
        <template #append>
          <span class="font-weight-bold text-red">
            {{ currencyFormat(attributes.excess_subsidence, currencyCode) }}
          </span>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="d-flex flex-wrap ga-2 mt-2">
      <v-chip :color="attributes.accidental_damage ? 'blue-grey' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.accidental_damage ? 'mdi-check' : 'mdi-close'" />
        Accidental Dmg
      </v-chip>
      <v-chip :color="attributes.trace_access ? 'blue-grey' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.trace_access ? 'mdi-water-magnify' : 'mdi-close'" />
        Trace & Access
      </v-chip>
      <v-chip :color="attributes.home_emergency ? 'blue-grey' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.home_emergency ? 'mdi-pipe-wrench' : 'mdi-close'" />
        Home Emergency
      </v-chip>
      <v-chip :color="attributes.matching_sets ? 'blue-grey' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.matching_sets ? 'mdi-toilet' : 'mdi-close'" />
        Matching Sets
      </v-chip>
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
