<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-medical-bag" class="mr-2" />
      Medical Policy Details
    </div>

    <v-row dense>
      <v-col cols="12" sm="6">
        <v-select
          v-model="modelValue.cover_type"
          :items="coverTypes"
          label="Plan Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          prepend-inner-icon="mdi-account-group"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="modelValue.underwriting_type"
          :items="underwritingTypes"
          label="Underwriting Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.excess"
          label="Annual Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Amount you pay per claim/year"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.outpatient_limit"
          label="Out-patient Limit"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          placeholder="Leave empty if full"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12">
        <v-text-field
          v-model="modelValue.hospital_list"
          label="Hospital List / Network Tier"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          placeholder="e.g. London / Provincial / Key List"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-caption font-weight-bold text-medium-emphasis mb-2">
          Included Extras & Benefits
        </div>
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.dental"
              label="Dental Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.optical"
              label="Optical Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.mental_health"
              label="Mental Health"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.therapies"
              label="Therapies (Physio/Osteo)"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.travel_cover"
              label="Worldwide Travel"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.cancer_cover"
              label="Full Cancer Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: 'MedicalPolicyForm',
  props: {
    currencySymbol: String,
    modelValue: { type: Object, default: () => ({}) },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      policyTypes: ['Individual', 'Couple', 'Family', 'Single Parent', 'Child Only'],
      underwritingTypes: ['Full Medical Underwriting', 'Moratorium', 'Switch/Continued', 'Unknown'],
    }
  },
  methods: {
    update() {
      this.$emit('update:modelValue', this.modelValue)
    },
  },
}
</script>
