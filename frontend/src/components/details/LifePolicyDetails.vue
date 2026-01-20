<template>
  <v-col cols="12" md="6">
    <v-list density="compact" class="bg-transparent">
      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-shield-star" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Cover Type</v-list-item-title>
        <template v-slot:append>
          <span class="font-weight-medium">
            {{ attributes.cover_type || 'Level Term' }}
          </span>
        </template>
      </v-list-item>
      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-account-group" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Beneficiaries</v-list-item-title>
        <template v-slot:append>
          <div class="text-right text-caption font-weight-bold" style="max-width: 150px">
            {{ attributes.beneficiaries || '-' }}
          </div>
        </template>
      </v-list-item>
      <v-list-item>
        <template v-slot:prepend>
          <v-icon icon="mdi-piggy-bank" size="small" class="mr-4" />
        </template>
        <v-list-item-title>Sum Assured</v-list-item-title>
        <template v-slot:append>
          <span class="text-h6 font-weight-bold text-success">
            {{ formatCurrency(attributes.sum_assured || 0) }}
          </span>
        </template>
      </v-list-item>
    </v-list>
  </v-col>

  <v-col cols="12" md="6">
    <div class="d-flex flex-wrap gap-2 mt-2">
      <v-chip :color="attributes.joint_policy ? 'purple' : 'default'" variant="tonal">
        <v-icon
          start
          :icon="attributes.joint_policy ? 'mdi-account-multiple-check' : 'mdi-account'"
        />
        {{ attributes.joint_policy ? 'Joint Policy' : 'Single Policy' }}
      </v-chip>

      <v-chip :color="attributes.critical_illness ? 'green' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.critical_illness ? 'mdi-check' : 'mdi-close'" />
        Critical Illness
      </v-chip>

      <v-chip :color="attributes.in_trust ? 'blue' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.in_trust ? 'mdi-bank' : 'mdi-bank-outline'" />
        In Trust
      </v-chip>

      <v-chip :color="attributes.waiver_premium ? 'green' : 'default'" variant="tonal">
        <v-icon start :icon="attributes.waiver_premium ? 'mdi-check' : 'mdi-close'" />
        Waiver of Premium
      </v-chip>
    </div>
  </v-col>
</template>

<script>
export default {
  props: {
    attributes: { type: Object, default: () => ({}) },
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: this.currencyCode,
        currencyDisplay: 'narrowSymbol',
      }).format(value)
    },
  },
}
</script>
