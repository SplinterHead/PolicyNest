<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-heart-pulse" class="mr-2" />
      Cover Details
    </div>

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

      <v-col cols="12">
        <v-text-field
          v-model="attributes.beneficiaries"
          label="Beneficiaries / Trust Name"
          placeholder="e.g. Spouse, Children, or 'The Smith Family Trust'"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">
          ADDITIONAL COVER
        </div>
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
const attributes = defineModel({ type: Object, default: () => ({}) })

defineProps({
  currencySymbol: String,
})

const policyTypes = ['Level Term', 'Decreasing Term (Mortgage)', 'Whole of Life', 'Over 50s Plan']
</script>
