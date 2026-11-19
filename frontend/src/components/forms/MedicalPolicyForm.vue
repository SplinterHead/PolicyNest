<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-medical-bag" class="mr-2" />
      Medical Policy Details
    </div>

    <v-row density="compact">
      <v-col cols="12" sm="6">
        <v-select
          v-model="attributes.cover_type"
          :items="coverTypes"
          label="Plan Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          prepend-inner-icon="mdi-account-group"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="attributes.underwriting_type"
          :items="underwritingTypes"
          label="Underwriting Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess"
          label="Annual Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Amount you pay per claim/year"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.outpatient_limit"
          label="Out-patient Limit"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          placeholder="Leave empty if full"
        />
      </v-col>

      <v-col cols="12">
        <v-text-field
          v-model="attributes.hospital_list"
          label="Hospital List / Network Tier"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          placeholder="e.g. London / Provincial / Key List"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">
          Included Extras & Benefits
        </div>
        <v-row density="compact">
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.dental"
              label="Dental Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.optical"
              label="Optical Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.mental_health"
              label="Mental Health"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.therapies"
              label="Therapies (Physio/Osteo)"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.travel_cover"
              label="Worldwide Travel"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.cancer_cover"
              label="Full Cancer Cover"
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

const coverTypes = ['Individual', 'Couple', 'Family', 'Single Parent', 'Child Only']
const underwritingTypes = ['Full Medical Underwriting', 'Moratorium', 'Switch/Continued', 'Unknown']
</script>
