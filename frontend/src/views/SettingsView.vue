<template>
  <div>
    <v-row>
      <v-col>
        <h1 class="text-h4 font-weight-thin">Settings</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2" rounded="lg" class="pa-4">
          <div class="d-flex align-center mb-4 text-primary font-weight-bold">
            <v-icon icon="mdi-earth" class="mr-2" />
            Localization
          </div>

          <v-select
            :model-value="currencyCode"
            @update:modelValue="$emit('update-currency', $event)"
            :items="currencies"
            item-title="label"
            item-value="code"
            label="Application Currency"
            variant="outlined"
            density="comfortable"
            hint="This affects how premiums and sums are displayed."
            persistent-hint
          >
            <template v-slot:selection="{ item }">
              <span class="mr-2 text-h6">{{ item.raw.symbol }}</span>
              {{ item.raw.label }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.code">
                <template v-slot:prepend>
                  <span class="mr-4 font-weight-bold">{{ item.raw.symbol }}</span>
                </template>
              </v-list-item>
            </template>
          </v-select>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  props: ['currencyCode'],
  emits: ['update-currency'],
  data() {
    return {
      currencies: [
        { code: 'GBP', label: 'British Pound', symbol: '£' },
        { code: 'EUR', label: 'Euro', symbol: '€' },
        { code: 'USD', label: 'US Dollar', symbol: '$' },
        { code: 'AUD', label: 'Australian Dollar', symbol: 'A$' },
        { code: 'CAD', label: 'Canadian Dollar', symbol: 'C$' },
      ],
    }
  },
}
</script>
