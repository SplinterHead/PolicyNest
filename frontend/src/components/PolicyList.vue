<template>
  <div>
    <v-card elevation="2" rounded="lg">
      <v-data-table
        :headers="headers"
        :items="policies"
        :loading="loading"
        hover
        @click:row="openPolicy"
        class="cursor-pointer"
      >
        <template v-slot:item.type="{ item }">
          <v-chip
            :color="getChipColour(item.type)"
            size="small"
            variant="flat"
            class="font-weight-bold"
          >
            {{ item.type }}
          </v-chip>
        </template>
        <template v-slot:item.start_date="{ item }">
          <div>
            {{ formatDate(item.start_date) }}
          </div>
        </template>
        <template v-slot:item.end_date="{ item }">
          <div v-if="!item.end_date">Perpetual</div>
          <div v-else>
            {{ formatDate(item.end_date) }}
          </div>
        </template>
        <template v-slot:item.premium="{ item }">
          <div class="d-flex flex-column align-start">
            <strong>{{ formatCurrency(item.premium) }}</strong>
            <span
              class="text-caption text-medium-emphasis"
              style="font-size: 0.7rem !important; line-height: 1"
            >
              {{ item.attributes.payment_frequency === 'Monthly' ? '/ month' : '/ year' }}
            </span>
          </div>
        </template>
        <template v-slot:item.actions="{ item }">
          <div class="d-flex justify-end">
            <v-btn icon size="small" variant="text" color="blue" @click.stop="$emit('edit', item)">
              <v-icon icon="mdi-pencil" />
              <v-tooltip activator="parent" location="top">Edit</v-tooltip>
            </v-btn>

            <v-btn icon size="small" variant="text" color="red" @click.stop="confirmDelete(item)">
              <v-icon icon="mdi-delete" />
              <v-tooltip activator="parent" location="top">Delete</v-tooltip>
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <PolicyDetailsDialog
      v-model="showPolicy"
      :policy="selectedPolicy"
      :currencyCode="currencyCode"
      @edit="handleEditFromDialog"
    />

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Delete Policy?</v-card-title>
        <v-card-text>
          Are you sure you want to delete the policy for
          <strong>{{ policyToDelete?.provider }}</strong
          >? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" variant="flat" @click="executeDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { getPolicyColour } from '@/utils/PolicyStyles'
import { currencyFormat } from '@/utils/Formats'
import PolicyDetailsDialog from '@/components/PolicyDetailsDialog.vue'

export default {
  name: 'PolicyList',
  components: {
    PolicyDetailsDialog,
  },
  props: {
    currencyCode: String,
    loading: Boolean,
    policies: Array,
  },
  emits: ['edit', 'delete', 'upload'],
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  data() {
    return {
      deleteDialog: false,
      policyToDelete: null,
      selectedPolicy: null,
      showPolicy: false,
      headers: [
        { title: 'Provider', key: 'provider', align: 'start' },
        { title: 'Type', key: 'type' },
        { title: 'Start Date', key: 'start_date' },
        { title: 'End Date', key: 'end_date' },
        { title: 'Premium', key: 'premium' },
        { title: '', key: 'actions', sortable: false, align: 'end' },
      ],
    }
  },
  methods: {
    confirmDelete(item) {
      this.policyToDelete = item
      this.deleteDialog = true
    },
    executeDelete() {
      if (this.policyToDelete) {
        this.$emit('delete', this.policyToDelete.id)
        this.deleteDialog = false
        this.policyToDelete = null
      }
    },
    formatCurrency(value) {
      return currencyFormat(value)
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    getChipColour(policyType) {
      return getPolicyColour(policyType)
    },
    handleEditFromDialog(policy) {
      this.showPolicy = false
      this.$emit('edit', policy)
    },
    openPolicy(event, { item }) {
      this.selectedPolicy = item
      this.showPolicy = true
    },
  },
}
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
.border-dashed {
  border-style: dashed !important;
}
</style>
