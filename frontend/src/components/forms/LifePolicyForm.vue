<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-heart-pulse" class="mr-2" />
      Cover Details
    </div>

    <v-row dense>
      <v-col cols="12" sm="6">
        <v-select
          v-model="modelValue.cover_type"
          :items="policyTypes"
          label="Policy Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="modelValue.sum_assured"
          label="Sum Assured (Payout)"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12">
        <v-text-field
          v-model="modelValue.beneficiaries"
          label="Beneficiaries / Trust Name"
          placeholder="e.g. Spouse, Children, or 'The Smith Family Trust'"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-caption font-weight-bold text-medium-emphasis mb-2">ADDITIONAL COVER</div>
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.joint_policy"
              label="Joint Policy"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.critical_illness"
              label="Critical Illness Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.waiver_premium"
              label="Waiver of Premium"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.in_trust"
              label="Held in Trust"
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
  name: 'LifePolicyForm',
  props: {
    currencySymbol: String,
    modelValue: { type: Object, default: () => ({}) },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      policyTypes: ['Level Term', 'Decreasing Term (Mortgage)', 'Whole of Life', 'Over 50s Plan'],
    }
  },
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  methods: {
    update() {
      this.$emit('update:modelValue', this.modelValue)
    },
  },
}
</script>
