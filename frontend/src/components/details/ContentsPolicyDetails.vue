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
    <FeatureChips :items="features" class="mt-2 mb-4" />

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
import { computed } from 'vue'
import { currencyFormat } from '@/utils/Formats'
import FeatureChips from '@/components/details/FeatureChips.vue'

const props = defineProps({
  attributes: { type: Object, default: () => ({}) },
  currencyCode: String,
})

const features = computed(() => [
  { label: 'Accidental', enabled: Boolean(props.attributes.accidental_damage) },
  { label: 'Away Cover', enabled: Boolean(props.attributes.personal_possessions) },
  { label: 'Bicycles', enabled: Boolean(props.attributes.bicycle_cover) },
  { label: 'Student', enabled: Boolean(props.attributes.student_cover) },
  { label: 'Garden', enabled: Boolean(props.attributes.garden_cover) },
  { label: 'Freezer', enabled: Boolean(props.attributes.freezer_contents) },
])
</script>
