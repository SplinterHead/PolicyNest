<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-paw" class="mr-2" />
      Pet Policy Details
    </div>

    <v-row dense>
      <v-col cols="12">
        <v-select
          :model-value="selectedAssetId"
          :items="assets"
          item-title="name"
          item-value="id"
          label="Select Pet from Inventory"
          variant="outlined"
          bg-color="surface"
          prepend-inner-icon="mdi-cat"
          clearable
          placeholder="Or leave blank for generic cover"
          @update:modelValue="onAssetSelect"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-text-field
          v-model="modelValue.pet_name"
          label="Pet Name"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          :readonly="!!selectedAssetId"
          hint="Auto-filled if pet selected"
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="modelValue.cover_type"
          :items="coverTypes"
          label="Cover Type"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.vet_fees_limit"
          label="Vet Fees Limit"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Max payout per year/condition"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.excess"
          label="Fixed Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12">
        <div class="text-caption text-medium-emphasis mb-1">Co-payment (Percentage you pay)</div>
        <v-slider
          v-model="modelValue.copay_percent"
          :min="0"
          :max="50"
          :step="5"
          thumb-label="always"
          color="primary"
          track-color="grey-lighten-2"
        >
          <template v-slot:append>
            <div class="font-weight-bold" style="width: 40px">
              {{ modelValue.copay_percent || 0 }}%
            </div>
          </template>
        </v-slider>
      </v-col>

      <v-col cols="12">
        <div class="text-caption font-weight-bold text-medium-emphasis mb-2">Included Extras</div>
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.boarding_fees"
              label="Boarding Fees"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.advertising_reward"
              label="Lost/Stolen (Advertising)"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.death_benefit"
              label="Death from Illness/Injury"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.third_party_liability"
              label="Third Party Liability"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.travel_cover"
              label="Overseas Travel"
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
  name: 'PetPolicyForm',
  props: {
    assets: { type: Array, default: () => [] },
    currencySymbol: String,
    modelValue: { type: Object, default: () => ({}) },
  },
  emits: ['update:modelValue', 'update:assetId'],
  data() {
    return {
      coverTypes: ['Lifetime', 'Maximum Benefit', 'Time Limited', 'Accident Only'],
      selectedAssetId: null,
    }
  },
  methods: {
    onAssetSelect(id) {
      this.selectedAssetId = id
      this.$emit('update:assetId', id)

      if (id) {
        const asset = this.assets.find((a) => a.id === id)
        if (asset) {
          this.modelValue.pet_name = asset.name
          this.update()
        }
      } else {
        this.modelValue.pet_name = ''
        this.update()
      }
    },
    update() {
      this.$emit('update:modelValue', this.modelValue)
    },
  },
}
</script>
