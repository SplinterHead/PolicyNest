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
      <v-list-item v-if="attributes.life_assured">
        <template #prepend>
          <v-icon icon="mdi-account-outline" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Life Assured</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">{{ attributes.life_assured }}</span>
        </template>
      </v-list-item>
      <v-list-item v-if="attributes.premium_type">
        <template #prepend>
          <v-icon icon="mdi-tune-variant" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Premium Type</v-list-item-title>
        <template #append>
          <span class="font-weight-medium">{{ attributes.premium_type }}</span>
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
    <FeatureChips :items="features" :class="beneficiariesList.length > 0 ? 'mt-2 mb-4' : 'mt-2'" />

    <div v-if="beneficiariesList.length > 0">
      <div class="text-body-small font-weight-bold text-medium-emphasis mb-1">Beneficiaries</div>
      <v-card variant="outlined" class="bg-surface-light">
        <v-list density="compact" class="bg-transparent py-0">
          <v-list-item v-for="(beneficiary, i) in beneficiariesList" :key="i" min-height="32">
            <template #prepend>
              <v-icon
                icon="mdi-account-group-outline"
                size="x-small"
                class="mr-2 text-medium-emphasis"
              />
            </template>
            <v-list-item-title class="text-body-small">{{ beneficiary }}</v-list-item-title>
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

const beneficiariesList = computed(() => {
  const raw = props.attributes.beneficiaries
  if (Array.isArray(raw)) {
    return raw.map((b) => String(b).trim()).filter(Boolean)
  }
  if (typeof raw === 'string' && raw.trim()) {
    return raw
      .split(',')
      .map((b) => b.trim())
      .filter(Boolean)
  }
  return []
})

const features = computed(() => [
  { label: 'Joint Policy', enabled: Boolean(props.attributes.joint_policy) },
  { label: 'Critical Illness', enabled: Boolean(props.attributes.critical_illness) },
  { label: 'Terminal Illness', enabled: Boolean(props.attributes.terminal_illness) },
  { label: "Children's CIC", enabled: Boolean(props.attributes.children_critical_illness) },
  { label: 'In Trust', enabled: Boolean(props.attributes.in_trust) },
  { label: 'Waiver of Premium', enabled: Boolean(props.attributes.waiver_premium) },
])
</script>
