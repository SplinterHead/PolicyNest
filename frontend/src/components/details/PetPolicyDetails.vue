<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-paw" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Pet Name</v-list-item-title>
        <template #append>
          <span class="font-weight-bold">{{ attributes.pet_name || 'N/A' }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-shield-star-outline" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Cover Type</v-list-item-title>
        <template #append>
          <v-chip size="small" color="brown" variant="tonal" class="font-weight-medium">
            {{ attributes.cover_type || 'Unknown' }}
          </v-chip>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-medical-bag" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Vet Fees Limit</v-list-item-title>
        <template #append>
          <span class="font-weight-bold text-primary">
            {{ currencyFormat(attributes.vet_fees_limit, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Excess</v-list-item-title>
        <template #append>
          <div class="text-right">
            <div class="font-weight-bold text-red">
              {{ currencyFormat(attributes.excess, currencyCode) }}
            </div>
            <div v-if="attributes.copay_percent" class="text-body-small text-red">
              + {{ attributes.copay_percent }}% Co-pay
            </div>
          </div>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">Policy Features</div>
    <div class="d-flex flex-wrap ga-2">
      <v-chip :color="attributes.third_party_liability ? 'brown' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.third_party_liability ? 'mdi-gavel' : 'mdi-close'" />
        Liability
      </v-chip>
      <v-chip :color="attributes.boarding_fees ? 'brown' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.boarding_fees ? 'mdi-home-outline' : 'mdi-close'" />
        Boarding
      </v-chip>
      <v-chip :color="attributes.advertising_reward ? 'brown' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.advertising_reward ? 'mdi-bullhorn' : 'mdi-close'" />
        Lost/Stolen
      </v-chip>
      <v-chip :color="attributes.death_benefit ? 'brown' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.death_benefit ? 'mdi-heart-broken' : 'mdi-close'" />
        Death Benefit
      </v-chip>
      <v-chip :color="attributes.travel_cover ? 'brown' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.travel_cover ? 'mdi-airplane' : 'mdi-close'" />
        Travel
      </v-chip>
    </div>

    <v-alert
      v-if="attributes.cover_type === 'Accident Only'"
      type="warning"
      variant="tonal"
      density="compact"
      class="mt-4 text-body-small"
      icon="mdi-alert"
    >
      This policy does not cover illness.
    </v-alert>
  </v-col>
</template>

<script setup>
import { currencyFormat } from '@/utils/Formats'

defineProps({
  attributes: { type: Object, default: () => ({}) },
  currencyCode: String,
})
</script>
