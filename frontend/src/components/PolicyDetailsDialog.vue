<template>
  <v-dialog
    :model-value="modelValue"
    max-width="700px"
    @update:modelValue="$emit('update:modelValue', $event)"
  >
    <v-card v-if="policy" rounded="lg">
      <v-toolbar :color="getHeaderColor(policy.type)" dark density="compact">
        <v-icon :icon="getIcon(policy.type)" class="ml-4 mr-2" />
        <v-toolbar-title class="font-weight-bold">
          {{ policy.provider }}
          <span class="text-caption ml-2 text-white">{{ policy.type }} Policy</span>
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon="mdi-close" variant="text" @click="$emit('update:modelValue', false)" />
      </v-toolbar>

      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="4" class="border-e">
            <div class="text-caption text-medium-emphasis mb-1">Status</div>
            <div class="mb-4">
              <v-chip :color="isActive(policy.end_date) ? 'success' : 'grey'" size="small" label>
                {{ isActive(policy.end_date) ? 'Active' : 'Expired' }}
              </v-chip>
            </div>

            <div class="text-caption text-medium-emphasis mb-1">Premium</div>
            <div class="text-h6 font-weight-bold mb-4">
              {{ formatCurrency(policy.premium) }}
              <span class="text-caption text-medium-emphasis">/ {{ policy.frequency }}</span>
            </div>

            <div class="text-caption text-medium-emphasis mb-1">Dates</div>
            <div class="text-body-2 mb-1">
              <strong>Start:</strong> {{ formatDate(policy.start_date) }}
            </div>
            <div class="text-body-2">
              <strong>End:</strong>
              <span v-if="policy.end_date">{{ formatDate(policy.end_date) }}</span>
              <span v-else class="text-success">Ongoing</span>
            </div>
          </v-col>

          <v-col cols="12" md="8">
            <div class="text-subtitle-2 font-weight-bold mb-3 text-primary">Coverage Details</div>

            <div v-if="policy.type === 'Contents'">
              <v-table density="compact" class="mb-3 border rounded">
                <tbody>
                  <tr>
                    <td class="text-medium-emphasis">Total Cover</td>
                    <td class="font-weight-bold">
                      {{ formatCurrency(policy.attributes?.total_cover) }}
                    </td>
                  </tr>
                  <tr>
                    <td class="text-medium-emphasis">Single Item Limit</td>
                    <td>{{ formatCurrency(policy.attributes?.single_item_limit) }}</td>
                  </tr>
                </tbody>
              </v-table>

              <div v-if="policy.attributes?.high_value_items?.length" class="mt-3">
                <div class="text-caption font-weight-bold mb-1">Specified Items:</div>
                <v-list density="compact" bg-color="grey-lighten-4" rounded="lg" class="py-0">
                  <v-list-item v-for="(item, i) in policy.attributes.high_value_items" :key="i">
                    <template v-slot:prepend>
                      <v-icon icon="mdi-diamond-stone" size="small" color="grey" />
                    </template>
                    <v-list-item-title class="text-body-2">{{ item.name }}</v-list-item-title>
                    <template v-slot:append>
                      <div class="font-weight-bold">{{ formatCurrency(item.value) }}</div>
                    </template>
                  </v-list-item>
                </v-list>
              </div>
            </div>

            <div v-else-if="policy.type === 'Medical'">
              <div class="d-flex flex-wrap gap-2 mb-3">
                <v-chip size="small" color="blue-lighten-4" class="text-blue-darken-3">
                  Type: {{ policy.attributes?.cover_type || 'N/A' }}
                </v-chip>
                <v-chip size="small" color="blue-lighten-4" class="text-blue-darken-3">
                  Excess: {{ formatCurrency(policy.attributes?.excess) }}
                </v-chip>
              </div>
              <div class="text-body-2 text-medium-emphasis">
                <strong>Hospital List:</strong> {{ policy.attributes?.hospital_list || 'Standard' }}
              </div>
            </div>

            <div v-else>
              <v-row dense>
                <v-col
                  v-for="(value, key) in displayableAttributes(policy.attributes)"
                  :key="key"
                  cols="6"
                >
                  <div class="text-caption text-medium-emphasis text-capitalize">
                    {{ key.replace(/_/g, ' ') }}
                  </div>
                  <div class="text-body-2">{{ value }}</div>
                </v-col>
              </v-row>
            </div>
          </v-col>
        </v-row>

        <v-divider class="my-4" />
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center">
            <v-icon icon="mdi-file-document-outline" class="mr-2" color="grey" />
            <span
              v-if="policy.document_path"
              class="text-body-2 text-decoration-underline text-primary cursor-pointer"
            >
              View Policy Document
            </span>
            <span v-else class="text-caption text-medium-emphasis">No document attached</span>
          </div>

          <v-btn
            color="primary"
            variant="tonal"
            size="small"
            prepend-icon="mdi-pencil"
            @click="$emit('edit', policy)"
          >
            Edit Policy
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'PolicyDetailsDialog',
  props: {
    modelValue: Boolean,
    policy: Object,
  },
  emits: ['update:modelValue', 'edit'],
  methods: {
    getHeaderColor(type) {
      const colors = {
        Car: 'blue-darken-2',
        Home: 'brown-darken-1',
        Buildings: 'blue-grey-darken-2',
        Contents: 'amber-darken-3',
        Medical: 'teal-darken-2',
        Pet: 'green-darken-2',
      }
      return colors[type] || 'grey-darken-2'
    },
    getIcon(type) {
      const icons = {
        Car: 'mdi-car',
        Buildings: 'mdi-home-city',
        Contents: 'mdi-sofa',
        Medical: 'mdi-medical-bag',
        Pet: 'mdi-paw',
      }
      return icons[type] || 'mdi-file-certificate'
    },
    isActive(endDate) {
      if (!endDate) return true
      return new Date(endDate) >= new Date()
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    formatCurrency(val) {
      if (val === null || val === undefined) return '-'
      return new Intl.Number('en-GB', { style: 'currency', currency: 'GBP' }).format(val)
    },
    // Helper to filter out complex objects from the generic fallback view
    displayableAttributes(attrs) {
      if (!attrs) return {}
      // Filter out arrays or objects, leave simple strings/numbers
      return Object.fromEntries(
        Object.entries(attrs).filter(([_, v]) => typeof v !== 'object' && v !== null),
      )
    },
  },
}
</script>
