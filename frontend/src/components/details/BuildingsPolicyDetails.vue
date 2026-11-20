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
    <FeatureChips :items="features" class="mt-2" />
  </v-col>
</template>

<script setup>
import { computed } from 'vue'
import { currencyFormat } from '@/utils/Formats'
import FeatureChips from '@/components/details/FeatureChips.vue'

const props = defineProps({
  attributes: { type: Object, default: () => ({}) },
  currencyCode: String,
})

const features = computed(() => [
  { label: 'Accidental Dmg', enabled: Boolean(props.attributes.accidental_damage) },
  { label: 'Trace & Access', enabled: Boolean(props.attributes.trace_access) },
  { label: 'Home Emergency', enabled: Boolean(props.attributes.home_emergency) },
  { label: 'Matching Sets', enabled: Boolean(props.attributes.matching_sets) },
])
</script>
