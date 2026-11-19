<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-paw" class="mr-2" />
      Pet Policy Details
    </div>

    <v-row density="compact">
      <v-col cols="12">
        <v-select
          v-model:menu="assetMenuOpen"
          :model-value="assetId"
          :items="assets"
          item-title="name"
          item-value="id"
          label="Select Pet from Inventory"
          variant="outlined"
          bg-color="surface"
          prepend-inner-icon="mdi-cat"
          clearable
          placeholder="Or leave blank for generic cover"
          @update:model-value="onAssetSelect"
        >
          <template #no-data>
            <div class="d-flex align-center justify-space-between px-4 py-2 ga-2">
              <span class="text-body-medium text-medium-emphasis">No pets in inventory</span>
              <v-btn
                size="small"
                color="primary"
                variant="tonal"
                prepend-icon="mdi-plus"
                @click="handleAddAsset"
              >
                Add Pet
              </v-btn>
            </div>
          </template>
        </v-select>
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model="attributes.pet_name"
          label="Pet Name"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          :readonly="!!assetId"
          hint="Auto-filled if pet selected"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="attributes.cover_type"
          :items="coverTypes"
          label="Cover Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.vet_fees_limit"
          label="Vet Fees Limit"
          type="number"
          min="0"
          persistent-placeholder
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Max payout per year/condition"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.excess"
          label="Fixed Excess"
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
        <div id="pet-copay-label" class="text-body-small text-medium-emphasis mb-1">
          Co-payment (Percentage you pay)
        </div>
        <v-slider
          v-model="attributes.copay_percent"
          :min="0"
          :max="50"
          :step="5"
          aria-labelledby="pet-copay-label"
          variant="pill"
          color="primary"
          track-color="grey-lighten-2"
        >
          <template #append>
            <div class="font-weight-bold" style="width: 40px">
              {{ attributes.copay_percent || 0 }}%
            </div>
          </template>
        </v-slider>
      </v-col>

      <v-col cols="12">
        <div class="text-body-small font-weight-bold text-medium-emphasis mb-2">
          Included Extras
        </div>
        <v-row density="compact">
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.boarding_fees"
              label="Boarding Fees"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.advertising_reward"
              label="Lost/Stolen (Advertising)"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.death_benefit"
              label="Death from Illness/Injury"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.third_party_liability"
              label="Third Party Liability"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.travel_cover"
              label="Overseas Travel"
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

const attributes = defineModel({ type: Object, default: () => ({}) })
const assetId = defineModel('assetId', { default: null })

const props = defineProps({
  assets: { type: Array, default: () => [] },
  currencySymbol: String,
})

const emit = defineEmits(['add-asset'])

const assetMenuOpen = ref(false)
const coverTypes = ['Lifetime', 'Maximum Benefit', 'Time Limited', 'Accident Only']

function handleAddAsset() {
  assetMenuOpen.value = false
  emit('add-asset')
}

function onAssetSelect(id) {
  assetId.value = id

  if (id) {
    const asset = props.assets.find((a) => a.id === id)
    if (asset) {
      attributes.value.pet_name = asset.name
    }
  } else {
    attributes.value.pet_name = ''
  }
}
</script>
