<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <h3 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
      <v-icon icon="mdi-heart-pulse" class="mr-2" />
      Life Cover Details
    </h3>

    <v-row density="compact">
      <v-col cols="12" sm="6">
        <v-select
          v-model="attributes.cover_type"
          :items="policyTypes"
          label="Policy Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.sum_assured"
          label="Sum Assured (Payout)"
          type="number"
          min="0"
          persistent-placeholder
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="attributes.premium_type"
          :items="premiumTypes"
          label="Premium Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          clearable
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model="attributes.life_assured"
          label="Life Assured"
          placeholder="e.g. John Smith"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <StringListField
          v-model="attributes.beneficiaries"
          title="Beneficiaries"
          add-label="Add Beneficiary"
          item-label="Beneficiary Name"
          placeholder="e.g. Jane Smith (Spouse)"
          empty-text="No beneficiaries added."
          remove-aria-label="Remove beneficiary"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <h4 class="text-body-small font-weight-bold text-medium-emphasis mb-2">Included Extras</h4>
        <v-row density="compact">
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.joint_policy"
              label="Joint Policy"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.critical_illness"
              label="Critical Illness Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.terminal_illness"
              label="Terminal Illness Benefit"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.children_critical_illness"
              label="Children's Critical Illness"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.waiver_premium"
              label="Waiver of Premium"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.in_trust"
              label="Held in Trust"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
import StringListField from '@/components/forms/StringListField.vue'

const attributes = defineModel({ type: Object, default: () => ({}) })

defineProps({
  currencySymbol: String,
})

const policyTypes = [
  'Level Term',
  'Decreasing Term (Mortgage)',
  'Increasing Term (Inflation-Linked)',
  'Family Income Benefit',
  'Whole of Life',
  'Over 50s Plan',
]
const premiumTypes = ['Guaranteed', 'Reviewable']
</script>
