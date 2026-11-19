<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-sofa" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Total Sum Insured</v-list-item-title>
        <template #append>
          <span class="font-weight-bold">
            {{ currencyFormat(attributes.total_cover, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-alert-circle-outline" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Single Item Limit</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">
            {{ currencyFormat(attributes.single_item_limit, currencyCode) }}
          </span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Excess</v-list-item-title>
        <template #append>
          <span class="font-weight-bold text-red">
            {{ currencyFormat(attributes.excess, currencyCode) }}
          </span>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="d-flex flex-wrap ga-2 mt-2 mb-4">
      <v-chip
        :color="attributes.accidental_damage ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.accidental_damage ? 'mdi-check' : 'mdi-close'" />
        Accidental
      </v-chip>
      <v-chip
        :color="attributes.personal_possessions ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.personal_possessions ? 'mdi-bag-suitcase' : 'mdi-close'" />
        Away Cover
      </v-chip>
      <v-chip
        :color="attributes.bicycle_cover ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.bicycle_cover ? 'mdi-bicycle' : 'mdi-close'" />
        Bicycles
      </v-chip>
      <v-chip
        :color="attributes.student_cover ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.student_cover ? 'mdi-school' : 'mdi-close'" />
        Student
      </v-chip>
    </div>

    <div v-if="attributes.high_value_items && attributes.high_value_items.length > 0">
      <div class="text-body-small font-weight-bold text-medium-emphasis mb-1">Specified Items</div>
      <v-card variant="outlined" class="bg-surface-light">
        <v-list density="compact" class="bg-transparent py-0">
          <v-list-item v-for="(item, i) in attributes.high_value_items" :key="i" min-height="32">
            <template #prepend>
              <v-icon icon="mdi-diamond-stone" size="x-small" class="mr-2 text-medium-emphasis" />
            </template>
            <v-list-item-title class="text-body-small">{{ item.name }}</v-list-item-title>
            <template #append>
              <span class="text-body-small font-weight-bold">
                {{ currencyFormat(item.value, currencyCode) }}
              </span>
            </template>
          </v-list-item>
        </v-list>
      </v-card>
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
