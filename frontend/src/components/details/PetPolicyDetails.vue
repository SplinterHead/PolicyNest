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
          <span class="font-weight-medium">{{ attributes.cover_type || 'Unknown' }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template #prepend>
          <v-icon icon="mdi-medical-bag" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Vet Fees Limit</v-list-item-title>
        <template #append>
          <div class="text-right">
            <div class="font-weight-bold text-primary">
              {{ currencyFormat(attributes.vet_fees_limit, currencyCode) }}
            </div>
            <div v-if="attributes.vet_fees_limit_type" class="text-body-small text-medium-emphasis">
              {{ attributes.vet_fees_limit_type }}
            </div>
          </div>
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
    <FeatureChips :items="features" />

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
import { computed } from 'vue'
import { currencyFormat } from '@/utils/Formats'
import FeatureChips from '@/components/details/FeatureChips.vue'

const props = defineProps({
  attributes: { type: Object, default: () => ({}) },
  currencyCode: String,
})

const features = computed(() => [
  { label: 'Liability', enabled: Boolean(props.attributes.third_party_liability) },
  { label: 'Dental Cover', enabled: Boolean(props.attributes.dental_cover) },
  { label: 'Hydro/Physio', enabled: Boolean(props.attributes.complementary_therapies) },
  { label: 'Death Benefit', enabled: Boolean(props.attributes.death_benefit) },
  { label: '24/7 Video Vet', enabled: Boolean(props.attributes.video_vet) },
])
</script>
