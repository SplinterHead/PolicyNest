<template>
  <v-card variant="tonal" class="pa-3 mt-2" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-car" class="mr-2"></v-icon>
      Vehicle Details
    </div>

    <v-row dense>
      <v-col cols="12">
        <v-select
          :model-value="selectedAssetId"
          :items="assets"
          item-title="name"
          item-value="id"
          label="Select Vehicle from Inventory"
          variant="outlined"
          bg-color="surface"
          prepend-inner-icon="mdi-garage"
          @update:modelValue="onAssetSelect"
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model="modelValue.reg_number"
          label="Registration"
          variant="outlined"
          density="comfortable"
          readonly
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="modelValue.make_model"
          label="Make / Model"
          variant="outlined"
          density="comfortable"
          readonly
        />
      </v-col>

      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.excess_voluntary"
          label="Voluntary Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          prefix="£"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.excess_compulsory"
          label="Compulsory Excess"
          type="number"
          variant="outlined"
          density="comfortable"
          prefix="£"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12">
        <v-select
          v-model="modelValue.cover_level"
          :items="['Comprehensive', 'Third Party, Fire & Theft', 'Third Party Only']"
          label="Cover Level"
          variant="outlined"
          density="comfortable"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-caption font-weight-bold text-medium-emphasis mb-2">Included Extras</div>
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.courtesy_car"
              label="Courtesy Car"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.legal_cover"
              label="Legal Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.breakdown"
              label="Breakdown Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.windscreen"
              label="Windscreen Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.protected_ncd"
              label="Protected NCD"
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
  props: {
    modelValue: { type: Object, default: () => ({}) },
    assets: { type: Array, default: () => [] },
  },
  data() {
    return {
      selectedAssetId: null,
    }
  },
  emits: ['update:modelValue', 'update:assetId'],
  methods: {
    onAssetSelect(id) {
      this.selectedAssetId = id
      const asset = this.assets.find((a) => a.id === id)

      if (asset) {
        this.modelValue.reg_number = asset.details.reg
        this.modelValue.make_model = `${asset.details.make} ${asset.details.model}`
        this.$emit('update:modelValue', this.modelValue)
        this.$emit('update:assetId', id)
      }
    },
    update() {
      this.$emit('update:modelValue', this.modelValue)
    },
  },
}
</script>
