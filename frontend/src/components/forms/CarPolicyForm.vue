<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <h3 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
      <v-icon icon="mdi-car" class="mr-2" />
      Vehicle Details
    </h3>

    <v-row density="compact">
      <v-col cols="12">
        <v-select
          v-model:menu="assetMenuOpen"
          :model-value="assetId"
          :items="assets"
          item-title="name"
          item-value="id"
          label="Select Vehicle from Inventory"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          prepend-inner-icon="mdi-garage"
          clearable
          placeholder="Or leave blank to enter manually"
          @update:model-value="onAssetSelect"
        >
          <template #no-data>
            <div class="d-flex align-center justify-space-between px-4 py-2 ga-2">
              <span class="text-body-medium text-medium-emphasis">No vehicles in inventory</span>
              <v-btn
                size="small"
                color="primary"
                variant="tonal"
                prepend-icon="mdi-plus"
                @click="handleAddAsset"
              >
                Add Vehicle
              </v-btn>
            </div>
          </template>
        </v-select>
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model="attributes.reg_number"
          label="Registration"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          :readonly="!!assetId"
          hint="Auto-filled if vehicle selected, or enter manually"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="attributes.make_model"
          label="Make / Model"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          :readonly="!!assetId"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess_voluntary"
          label="Voluntary Excess"
          type="number"
          min="0"
          persistent-placeholder
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
          min="0"
          persistent-placeholder
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

      <v-col cols="12" sm="6">
        <v-select
          v-model="attributes.class_of_use"
          :items="classOfUseOptions"
          label="Class of Use"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          clearable
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model.number="attributes.annual_mileage"
          label="Annual Mileage"
          type="number"
          min="0"
          persistent-placeholder
          suffix="miles"
          placeholder="e.g. 8000"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <StringListField
          v-model="attributes.additional_drivers"
          title="Additional Drivers"
          add-label="Add Driver"
          item-label="Driver Name"
          placeholder="e.g. Jane Doe"
          empty-text="No additional drivers added."
          remove-aria-label="Remove driver"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <h4 class="text-body-small font-weight-bold text-medium-emphasis mb-2">Included Extras</h4>
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
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.driving_other_cars"
              label="Driving Other Cars"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.key_cover"
              label="Key Cover"
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
import { ref } from 'vue'
import StringListField from '@/components/forms/StringListField.vue'

const attributes = defineModel({ type: Object, default: () => ({}) })
const assetId = defineModel('assetId', { default: null })

const props = defineProps({
  assets: { type: Array, default: () => [] },
  currencySymbol: String,
})

const emit = defineEmits(['add-asset'])

const assetMenuOpen = ref(false)
const classOfUseOptions = ['Social, Domestic & Pleasure', 'SDP & Commuting', 'Business Use']

function handleAddAsset() {
  assetMenuOpen.value = false
  emit('add-asset')
}

function onAssetSelect(id) {
  assetId.value = id

  if (id) {
    const asset = props.assets.find((a) => a.id === id)
    if (asset) {
      attributes.value.reg_number = asset.details?.reg || ''
      attributes.value.make_model = [asset.details?.make, asset.details?.model]
        .filter(Boolean)
        .join(' ')
    }
  } else {
    attributes.value.reg_number = ''
    attributes.value.make_model = ''
  }
}
</script>
