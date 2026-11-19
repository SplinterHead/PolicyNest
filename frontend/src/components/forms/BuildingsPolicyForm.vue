<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-home-city" class="mr-2" />
      Buildings Details
    </div>

    <v-row density="compact">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.rebuild_cost"
          label="Rebuild Cost"
          type="number"
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
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          placeholder="e.g. 50000"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess_standard"
          label="Standard Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess_subsidence"
          label="Subsidence Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Usually £1000+"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">
          Coverage Extensions
        </div>
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
