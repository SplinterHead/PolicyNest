<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-sofa" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Total Sum Insured</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-bold">{{ formatCurrency(attributes.total_cover) }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-alert-circle-outline" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Single Item Limit</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-medium">{{ formatCurrency(attributes.single_item_limit) }}</span>
        </template>
      </v-list-item>

      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-cash-minus" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Excess</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-bold text-red">{{ formatCurrency(attributes.excess) }}</span>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="d-flex flex-wrap gap-2 mt-2 mb-4">
      <v-chip
        :color="attributes.accidental_damage ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.accidental_damage ? 'mdi-check' : 'mdi-close'" />
        Accidental
      </v-chip>
      <v-chip
        :color="attributes.personal_possessions ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.personal_possessions ? 'mdi-bag-suitcase' : 'mdi-close'" />
        Away Cover
      </v-chip>
      <v-chip
        :color="attributes.bicycle_cover ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.bicycle_cover ? 'mdi-bicycle' : 'mdi-close'" />
        Bicycles
      </v-chip>
      <v-chip
        :color="attributes.student_cover ? 'amber-darken-3' : 'default'"
        variant="tonal"
        size="small"
      >
        <v-icon start :icon="attributes.student_cover ? 'mdi-school' : 'mdi-close'" />
        Student
      </v-chip>
    </div>

    <div v-if="attributes.high_value_items && attributes.high_value_items.length > 0">
      <div class="text-caption font-weight-bold text-medium-emphasis mb-1">Specified Items</div>
      <v-card variant="outlined" class="bg-surface-light">
        <v-list density="compact" class="bg-transparent py-0">
          <v-list-item v-for="(item, i) in attributes.high_value_items" :key="i" min-height="32">
            <template v-slot:prepend>
              <v-icon icon="mdi-diamond-stone" size="x-small" class="mr-2 text-medium-emphasis" />
            </template>
            <v-list-item-title class="text-caption">{{ item.name }}</v-list-item-title>
            <template v-slot:append>
              <span class="text-caption font-weight-bold">{{ formatCurrency(item.value) }}</span>
            </template>
          </v-list-item>
        </v-list>
      </v-card>
    </div>
  </v-col>
</template>

<script>
export default {
  name: 'ContentsPolicyDetails',
  props: {
    attributes: { type: Object, default: () => ({}) },
    currencyCode: String,
  },
  methods: {
    formatCurrency(value) {
      if (value === undefined || value === null) return 'N/A'
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: this.currencyCode,
        currencyDisplay: 'narrowSymbol',
      }).format(value)
    },
  },
}
</script>
