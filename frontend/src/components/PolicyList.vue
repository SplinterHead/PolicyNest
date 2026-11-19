<template>
  <div>
    <v-card elevation="2" rounded="lg">
      <v-data-table
        :headers="headers"
        :items="policies"
        :loading="loading"
        hover
        class="cursor-pointer"
        @click:row="openPolicy"
      >
        <template #item.type="{ item }">
          <v-chip
            :color="getPolicyColour(item.type)"
            size="small"
            variant="flat"
            class="font-weight-bold"
          >
            {{ item.type }}
          </v-chip>
        </template>
        <template #item.start_date="{ item }">
          <div>
            {{ formatDate(item.start_date) }}
          </div>
        </template>
        <template #item.end_date="{ item }">
          <div v-if="!item.end_date">Perpetual</div>
          <div v-else>
            {{ formatDate(item.end_date) }}
          </div>
        </template>
        <template #item.premium="{ item }">
          <div class="d-flex flex-column align-start">
            <strong>{{ currencyFormat(item.premium, currencyCode) }}</strong>
            <span
              class="text-body-small text-medium-emphasis"
              style="font-size: 0.7rem !important; line-height: 1"
            >
              {{ item.attributes.payment_frequency === 'Monthly' ? '/ month' : '/ year' }}
            </span>
          </div>
        </template>
        <template #item.actions="{ item }">
          <div class="d-flex justify-end ga-1">
            <v-tooltip text="Edit" location="top">
              <template #activator="{ props: tooltipProps }">
                <v-icon-btn
                  v-bind="tooltipProps"
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  color="blue"
                  aria-label="Edit policy"
                  @click.stop="emit('edit', item)"
                />
              </template>
            </v-tooltip>

            <v-tooltip text="Delete" location="top">
              <template #activator="{ props: tooltipProps }">
                <v-icon-btn
                  v-bind="tooltipProps"
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="red"
                  aria-label="Delete policy"
                  @click.stop="confirmDelete(item)"
                />
              </template>
            </v-tooltip>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <PolicyDetailsDialog
      v-model="showPolicy"
      :policy="selectedPolicy"
      :currency-code="currencyCode"
      @edit="handleEditFromDialog"
      @uploaded="handleDocumentUploaded"
    />

    <v-dialog v-model="deleteDialog" max-width="400px" aria-labelledby="delete-policy-title">
      <v-card>
        <v-card-title id="delete-policy-title" class="text-headline-small">
          Delete Policy?
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete the policy for
          <strong>{{ policyToDelete?.provider }}</strong>? This action cannot be undone.
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

<script setup>
import { ref } from 'vue'
import { getPolicyColour } from '@/utils/PolicyTypes'
import { currencyFormat, formatDate } from '@/utils/Formats'
import PolicyDetailsDialog from '@/components/PolicyDetailsDialog.vue'

defineProps({
  currencyCode: String,
  loading: Boolean,
  policies: Array,
})

const emit = defineEmits(['edit', 'delete', 'uploaded'])

const deleteDialog = ref(false)
const policyToDelete = ref(null)
const selectedPolicy = ref(null)
const showPolicy = ref(false)

const headers = [
  { title: 'Provider', key: 'provider', align: 'start' },
  { title: 'Type', key: 'type' },
  { title: 'Start Date', key: 'start_date' },
  { title: 'End Date', key: 'end_date' },
  { title: 'Premium', key: 'premium' },
  { title: '', key: 'actions', sortable: false, align: 'end' },
]

function confirmDelete(item) {
  policyToDelete.value = item
  deleteDialog.value = true
}

function executeDelete() {
  if (policyToDelete.value) {
    emit('delete', policyToDelete.value.id)
    deleteDialog.value = false
    policyToDelete.value = null
  }
}

function handleEditFromDialog(policy) {
  showPolicy.value = false
  emit('edit', policy)
}

function handleDocumentUploaded(updatedPolicy) {
  selectedPolicy.value = updatedPolicy
  emit('uploaded', updatedPolicy)
}

function openPolicy(event, { item }) {
  selectedPolicy.value = item
  showPolicy.value = true
}
</script>
