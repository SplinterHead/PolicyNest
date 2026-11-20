<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <h3 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
      <v-icon icon="mdi-home-city" class="mr-2" />
      Buildings Details
    </h3>

    <v-row density="compact">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.rebuild_cost"
          label="Rebuild Cost"
          type="number"
          min="0"
          persistent-placeholder
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Cost to rebuild, not market value"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.alternative_accommodation"
          label="Alternative Accommodation"
          type="number"
          min="0"
          persistent-placeholder
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          placeholder="e.g. 50000"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.excess_standard"
          label="Standard Excess"
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
        <v-text-field
          v-model.number="attributes.excess_subsidence"
          label="Subsidence Excess"
          type="number"
          min="0"
          persistent-placeholder
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          :hint="`Usually ${currencySymbol}1000+`"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.excess_escape_water"
          label="Escape of Water Excess"
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
        <v-text-field
          v-model.number="attributes.unoccupancy_limit"
          label="Unoccupancy Limit"
          type="number"
          min="0"
          persistent-placeholder
          suffix="days"
          placeholder="e.g. 30"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          hint="Max consecutive days unoccupied"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <h4 class="text-body-small font-weight-bold text-medium-emphasis mb-2">Included Extras</h4>
        <v-row density="compact">
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.accidental_damage"
              label="Full Accidental Damage"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.trace_access"
              label="Trace & Access (Leak Detection)"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.home_emergency"
              label="Home Emergency (Boiler/Plumbing)"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.matching_sets"
              label="Matching Sets (Bathroom suites)"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.legal_expenses"
              label="Legal Expenses"
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
</script>
