<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-hammer-wrench" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Rebuild Cost</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-bold">{{ formatCurrency(attributes.rebuild_cost) }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-bed" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Alt. Accommodation</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-medium">{{
            formatCurrency(attributes.alternative_accommodation)
          }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Standard Excess</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-bold text-red">{{
            formatCurrency(attributes.excess_standard)
          }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-alert-box-outline" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Subsidence Excess</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-bold text-red">{{
            formatCurrency(attributes.excess_subsidence)
          }}</span>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="d-flex flex-wrap gap-2 mt-2">
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

<script>
import { currencyFormat } from '@/utils/Formats'

export default {
  name: 'BuildingsPolicyDetails',
  props: {
    attributes: { type: Object, default: () => ({}) },
    currencyCode: String,
  },
  methods: {
    formatCurrency(value) {
      return currencyFormat(value)
    },
  },
}
</script>
