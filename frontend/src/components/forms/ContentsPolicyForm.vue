<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <div class="d-flex align-center text-primary font-weight-bold mb-4">
      <v-icon icon="mdi-sofa" class="mr-2" />
      Contents Details
    </div>

    <v-row dense>
      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.total_cover"
          label="Total Sum Insured"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          @update:modelValue="update"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model.number="modelValue.single_item_limit"
          label="Single Item Limit"
          type="number"
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Max per item unless specified"
          @update:modelValue="update"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="d-flex justify-space-between align-center mb-2">
          <div class="text-caption font-weight-bold text-medium-emphasis">
            Specified High Value Items
          </div>
          <v-btn
            size="small"
            variant="text"
            color="primary"
            prepend-icon="mdi-plus"
            @click="addItem"
          >
            Add Item
          </v-btn>
        </div>

        <div v-if="itemsList.length > 0">
          <v-row v-for="(item, index) in itemsList" :key="index" dense class="align-center mb-1">
            <v-col cols="7">
              <v-text-field
                v-model="item.name"
                label="Item Description"
                placeholder="e.g. Diamond Ring"
                variant="outlined"
                density="compact"
                hide-details
                bg-color="surface"
                @update:modelValue="update"
              />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model.number="item.value"
                label="Value"
                type="number"
                :prefix="currencySymbol"
                variant="outlined"
                density="compact"
                hide-details
                bg-color="surface"
                @update:modelValue="update"
              />
            </v-col>
            <v-col cols="1" class="d-flex justify-center">
              <v-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="red-lighten-2"
                @click="removeItem(index)"
              />
            </v-col>
          </v-row>
        </div>

        <v-alert v-else type="info" variant="tonal" density="compact" class="text-caption">
          No specified items added.
        </v-alert>
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="text-caption font-weight-bold text-medium-emphasis mb-2">Included Extras</div>
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.accidental_damage"
              label="Accidental Damage"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.personal_possessions"
              label="Cover Away From Home"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.bicycle_cover"
              label="Bicycle Cover"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.garden_cover"
              label="Garden / Outbuildings"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.student_cover"
              label="Student Cover (Uni)"
              color="primary"
              density="compact"
              hide-details
              @update:modelValue="update"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="modelValue.freezer_contents"
              label="Freezer Contents"
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
  name: 'ContentsPolicyForm',
  props: {
    currencySymbol: String,
    modelValue: { type: Object, default: () => ({}) },
  },
  emits: ['update:modelValue'],
  computed: {
    itemsList() {
      if (!Array.isArray(this.modelValue.high_value_items)) {
        this.modelValue.high_value_items = []
      }
      return this.modelValue.high_value_items
    },
  },
  methods: {
    addItem() {
      if (!this.modelValue.high_value_items) {
        this.modelValue.high_value_items = []
      }
      this.modelValue.high_value_items.push({ name: '', value: null })
      this.update()
    },
    removeItem(index) {
      this.modelValue.high_value_items.splice(index, 1)
      this.update()
    },
    update() {
      this.$emit('update:modelValue', this.modelValue)
    },
  },
}
</script>
