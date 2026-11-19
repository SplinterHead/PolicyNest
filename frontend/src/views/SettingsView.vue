<template>
  <div>
    <v-row>
      <v-col>
        <h1 class="text-headline-large font-weight-thin">Settings</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2" rounded="lg" class="pa-4">
          <h2 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
            <v-icon icon="mdi-earth" class="mr-2" />
            Localization
          </h2>

          <v-select
            :model-value="currencyCode"
            :items="currencies"
            item-title="label"
            item-value="code"
            label="Application Currency"
            variant="outlined"
            density="comfortable"
            hint="This affects how premiums and sums are displayed."
            persistent-hint
            @update:model-value="emit('update-currency', $event)"
          >
            <template #selection="{ item }">
              <span class="mr-2 text-title-large">{{ item.symbol }}</span>
              {{ item.label }}
            </template>
            <template #item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.code">
                <template #prepend>
                  <span class="mr-4 font-weight-bold">{{ item.symbol }}</span>
                </template>
              </v-list-item>
            </template>
          </v-select>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
defineProps({
  currencyCode: String,
})

const emit = defineEmits(['update-currency'])

const currencies = [
  { code: 'GBP', label: 'British Pound', symbol: '£' },
  { code: 'EUR', label: 'Euro', symbol: '€' },
  { code: 'USD', label: 'US Dollar', symbol: '$' },
  { code: 'AUD', label: 'Australian Dollar', symbol: 'A$' },
  { code: 'CAD', label: 'Canadian Dollar', symbol: 'C$' },
]
</script>
