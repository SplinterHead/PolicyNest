<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-home-city" class="mr-2" />
      Buildings Details
    </div>
    <v-row dense>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="modelValue.rebuild_cost"
          label="Rebuild Cost"
          :prefix="currencySymbol"
          type="number"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="modelValue.excess"
          label="Standard Excess"
          :prefix="currencySymbol"
          type="number"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>
      <v-col cols="12">
        <v-checkbox
          v-model="modelValue.accidental_damage"
          label="Accidental Damage Cover"
          color="primary"
          density="compact"
          hide-details
          @update:modelValue="update"
        />
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  props: {
    currencySymbol: String,
    modelValue: { type: Object, default: () => ({}) },
  },
  emits: ['update:modelValue'],
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
