<template>
  <v-card class="mt-2 mb-2 elevation-0" rounded="lg">
    <h3 class="text-title-medium font-weight-bold text-primary d-flex align-center mb-4">
      <v-icon icon="mdi-sofa" class="mr-2" />
      Contents Details
    </h3>

    <v-row density="compact">
      <v-col cols="6">
        <v-text-field
          v-model.number="attributes.total_cover"
          label="Total Sum Insured"
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
          v-model.number="attributes.single_item_limit"
          label="Single Item Limit"
          type="number"
          min="0"
          persistent-placeholder
          variant="outlined"
          density="comfortable"
          :prefix="currencySymbol"
          bg-color="surface"
          hint="Max per item unless specified"
        />
      </v-col>

      <v-col cols="12" class="mt-2">
        <div class="d-flex justify-space-between align-center mb-2">
          <h4 class="text-body-small font-weight-bold text-medium-emphasis">
            Specified High Value Items
          </h4>
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
          <v-row
            v-for="(item, index) in itemsList"
            :key="index"
            density="compact"
            class="align-center mb-1"
          >
            <v-col cols="7">
              <v-text-field
                v-model="item.name"
                label="Item Description"
                placeholder="e.g. Diamond Ring"
                variant="outlined"
                density="comfortable"
                hide-details
                bg-color="surface"
              />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model.number="item.value"
                label="Value"
                type="number"
                min="0"
                persistent-placeholder
                :prefix="currencySymbol"
                variant="outlined"
                density="comfortable"
                hide-details
                bg-color="surface"
              />
            </v-col>
            <v-col cols="1" class="d-flex justify-center">
              <v-icon-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="red-lighten-2"
                aria-label="Remove item"
                @click="removeItem(index)"
              />
            </v-col>
          </v-row>
        </div>

        <v-sheet
          v-else
          rounded="md"
          border
          class="d-flex align-center px-3 py-2 text-body-small text-medium-emphasis bg-surface-light"
        >
          <v-icon icon="mdi-information-outline" size="small" class="mr-2" aria-hidden="true" />
          No specified items added.
        </v-sheet>
      </v-col>

      <v-col cols="12" class="mt-2">
        <h4 class="text-body-small font-weight-bold text-medium-emphasis mb-2">Included Extras</h4>
        <v-row density="compact">
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.accidental_damage"
              label="Accidental Damage"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.personal_possessions"
              label="Cover Away From Home"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.bicycle_cover"
              label="Bicycle Cover"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.garden_cover"
              label="Garden / Outbuildings"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.student_cover"
              label="Student Cover (Uni)"
              color="primary"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-checkbox
              v-model="attributes.freezer_contents"
              label="Freezer Contents"
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
import { computed } from 'vue'

const attributes = defineModel({ type: Object, default: () => ({}) })

defineProps({
  currencySymbol: String,
})

const itemsList = computed(() => attributes.value.high_value_items ?? [])

function addItem() {
  if (!Array.isArray(attributes.value.high_value_items)) {
    attributes.value.high_value_items = []
  }
  attributes.value.high_value_items.push({ name: '', value: null })
}

function removeItem(index) {
  attributes.value.high_value_items?.splice(index, 1)
}
</script>
