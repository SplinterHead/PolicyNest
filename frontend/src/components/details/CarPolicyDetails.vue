<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-identifier" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Reg Plate</v-list-item-title>
        <template #append>
          <v-chip size="small" variant="outlined" class="text-uppercase font-weight-bold">
            {{ attributes.reg_number || 'N/A' }}
          </v-chip>
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
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Total Excess</v-list-item-title>
        <template #append>
          <span class="font-weight-bold text-red">
            {{
              currencyFormat(
                (attributes.excess_voluntary || 0) + (attributes.excess_compulsory || 0),
                currencyCode,
              )
            }}
          </span>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="d-flex flex-wrap ga-2 mt-2">
      <v-chip :color="attributes.courtesy_car ? 'green' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.courtesy_car ? 'mdi-check' : 'mdi-close'" />
        Courtesy Car
      </v-chip>
      <v-chip :color="attributes.legal_cover ? 'green' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.legal_cover ? 'mdi-check' : 'mdi-close'" />
        Legal Cover
      </v-chip>
      <v-chip :color="attributes.breakdown ? 'green' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.breakdown ? 'mdi-check' : 'mdi-close'" />
        Breakdown
      </v-chip>
      <v-chip :color="attributes.windscreen ? 'green' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.windscreen ? 'mdi-check' : 'mdi-close'" />
        Windscreen
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
