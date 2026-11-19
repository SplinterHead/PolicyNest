<template>
  <v-dialog v-model="open" max-width="500px" aria-labelledby="manage-households-title">
    <v-card rounded="lg" elevation="2" class="pa-2">
      <v-toolbar color="transparent" density="compact">
        <v-toolbar-title id="manage-households-title" class="text-title-large">
          My Households
        </v-toolbar-title>
        <v-spacer />
        <v-icon-btn icon="mdi-close" variant="text" aria-label="Close" @click="open = false" />
      </v-toolbar>

      <v-card-text class="pa-0">
        <v-list lines="two">
          <v-list-item
            v-for="house in households"
            :key="house.id"
            :active="house.id === currentId"
            color="primary"
            @click="emit('select', house)"
          >
            <template #prepend>
              <v-icon :icon="house.id === currentId ? 'mdi-home' : 'mdi-home-outline'" />
            </template>

            <v-list-item-title>{{ house.name }}</v-list-item-title>
            <v-list-item-subtitle v-if="house.id === currentId">
              Currently Selected
            </v-list-item-subtitle>

            <template #append>
              <v-icon v-if="house.id === currentId" color="primary" icon="mdi-check" />
              <v-icon-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="grey"
                class="ml-2"
                aria-label="Delete household"
                @click.stop="confirmDeleteHousehold(house)"
              />
            </template>
          </v-list-item>
        </v-list>
      </v-card-text>

      <v-divider />

      <v-card-actions>
        <v-btn
          block
          prepend-icon="mdi-plus"
          color="primary"
          variant="text"
          @click="showCreate = true"
        >
          Add New Household
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <NewHouseholdDialog
    v-model="showCreate"
    title="Add New Household"
    subtitle="Create a separate space for another property."
    :show-cancel="true"
    @complete="handleCreate"
  />

  <v-dialog
    v-model="deleteHouseholdDialog"
    max-width="500px"
    aria-labelledby="delete-household-title"
  >
    <v-card>
      <v-card-title id="delete-household-title" class="text-headline-small text-red">
        Delete Household?
      </v-card-title>
      <v-card-text>
        Are you sure you want to delete
        <strong>{{ householdToDelete?.name }}</strong>? <br /><br />
        <v-alert type="warning" variant="tonal" density="compact" border="start">
          This will permanently delete all
          <strong>Policies, Assets, and Documents</strong> associated with this household.
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="grey" variant="text" @click="deleteHouseholdDialog = false">Cancel</v-btn>
        <v-btn
          color="red"
          variant="flat"
          :loading="deletingHousehold"
          @click="executeDeleteHousehold"
        >
          Delete Forever
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'
import NewHouseholdDialog from '@/components/NewHouseholdDialog.vue'

const open = defineModel({ type: Boolean })

defineProps({
  households: Array,
  currentId: Number,
})

const emit = defineEmits(['select', 'created', 'deleted'])

const deleteHouseholdDialog = ref(false)
const deletingHousehold = ref(false)
const householdToDelete = ref(null)
const showCreate = ref(false)

function handleCreate(newHousehold) {
  showCreate.value = false
  emit('created', newHousehold)
}

function confirmDeleteHousehold(household) {
  householdToDelete.value = household
  deleteHouseholdDialog.value = true
}

async function executeDeleteHousehold() {
  if (!householdToDelete.value) return
  deletingHousehold.value = true
  try {
    const household = householdToDelete.value
    await api.delete(`/households/${household.id}`)
    deleteHouseholdDialog.value = false
    householdToDelete.value = null
    emit('deleted', household)
  } catch (e) {
    console.error('Failed to delete household', e)
  } finally {
    deletingHousehold.value = false
  }
}
</script>
