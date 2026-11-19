<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-car" class="mr-2" />
      Vehicle Details
    </div>

    <v-row density="compact">
      <v-col cols="12">
        <v-select
          :model-value="assetId"
          :items="assets"
          item-title="name"
          item-value="id"
          label="Select Vehicle from Inventory"
          variant="outlined"
          bg-color="surface"
          prepend-inner-icon="mdi-garage"
          @update:model-value="onAssetSelect"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model="attributes.reg_number"
          label="Registration"
          variant="outlined"
          density="comfortable"
          readonly
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="attributes.make_model"
          label="Make / Model"
          variant="outlined"
          density="comfortable"
          readonly
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess_voluntary"
          label="Voluntary Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess_compulsory"
          label="Compulsory Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12">
        <v-select
          v-model="attributes.cover_level"
          :items="['Comprehensive', 'Third Party, Fire & Theft', 'Third Party Only']"
          label="Cover Level"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">
          Included Extras
        </div>
        <v-row density="compact">
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.courtesy_car"
              label="Courtesy Car"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.legal_cover"
              label="Legal Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.breakdown"
              label="Breakdown Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.windscreen"
              label="Windscreen Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.protected_ncd"
              label="Protected NCD"
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
const assetId = defineModel('assetId', { default: null })

const props = defineProps({
  assets: { type: Array, default: () => [] },
  currencySymbol: String,
})

function onAssetSelect(id) {
  assetId.value = id
  const asset = props.assets.find((a) => a.id === id)

  if (asset) {
    attributes.value.reg_number = asset.details.reg
    attributes.value.make_model = `${asset.details.make} ${asset.details.model}`
  }
}
</script>
