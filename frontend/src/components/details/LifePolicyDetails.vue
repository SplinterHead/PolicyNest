<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-shield-star" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Cover Type</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">
            {{ attributes.cover_type || 'Level Term' }}
          </span>
        </template>
      </v-list-item>
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-account-group" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Beneficiaries</v-list-item-title>
        <template #append>
          <div class="text-right text-body-small font-weight-bold" style="max-width: 150px">
            {{ attributes.beneficiaries || '-' }}
          </div>
        </template>
      </v-list-item>
      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-piggy-bank" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Sum Assured</v-list-item-title>
        <template #append>
          <span class="text-title-large font-weight-bold text-success">
            {{ currencyFormat(attributes.sum_assured || 0, currencyCode) }}
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
  { label: 'Joint Policy', enabled: Boolean(props.attributes.joint_policy) },
  { label: 'Critical Illness', enabled: Boolean(props.attributes.critical_illness) },
  { label: 'In Trust', enabled: Boolean(props.attributes.in_trust) },
  { label: 'Waiver of Premium', enabled: Boolean(props.attributes.waiver_premium) },
])
</script>
