<template>
  <v-dialog v-model="open" max-width="500px" aria-labelledby="manage-households-title">
    <v-card rounded="lg" elevation="2">
      <v-card-title id="manage-households-title" class="pa-4 bg-surface-light d-flex align-center">
        <v-icon icon="mdi-home-group" color="primary" class="mr-2" />
        My Households
        <v-spacer />
        <v-icon-btn icon="mdi-close" variant="text" aria-label="Close" @click="open = false" />
      </v-card-title>
      <v-divider />

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
              <v-icon v-if="house.id === currentId" color="primary" icon="mdi-check" class="mr-2" />
              <v-icon-btn
                icon="mdi-pencil-outline"
                size="small"
                variant="text"
                :aria-label="`Rename ${house.name}`"
                @click.stop="openRenameHousehold(house)"
              />
              <v-divider vertical inset class="mx-2" />
              <v-icon-btn
                icon="mdi-delete-outline"
                size="small"
                variant="text"
                color="error"
                :aria-label="`Delete ${house.name}`"
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

  <v-dialog v-model="renameDialog" max-width="460px" aria-labelledby="rename-household-title">
    <v-card rounded="lg">
      <v-card-title id="rename-household-title" class="pa-4 bg-surface-light d-flex align-center">
        <v-icon icon="mdi-home-edit-outline" color="primary" class="mr-2" />
        Rename Household
        <v-spacer />
        <v-icon-btn
          icon="mdi-close"
          variant="text"
          aria-label="Close"
          :disabled="renamingHousehold"
          @click="renameDialog = false"
        />
      </v-card-title>
      <v-divider />
      <v-card-text class="pt-4">
        <v-form v-model="renameValid" @submit.prevent="executeRenameHousehold">
          <v-text-field
            v-model="renameName"
            label="Household Name"
            variant="outlined"
            density="comfortable"
            :rules="[(v) => !!(v && v.trim()) || 'Name is required']"
            autofocus
          />
        </v-form>
      </v-card-text>
      <v-card-actions class="pa-4 pt-0">
        <v-spacer />
        <v-btn variant="text" :disabled="renamingHousehold" @click="renameDialog = false">
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          :loading="renamingHousehold"
          :disabled="!renameValid || !renameName.trim()"
          @click="executeRenameHousehold"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

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

        <v-alert
          v-if="isLastHousehold"
          type="error"
          variant="tonal"
          density="compact"
          border="start"
          class="mt-3"
        >
          This is the <strong>last remaining household</strong>. Deleting it will erase all data and
          return to initial setup.
        </v-alert>

        <v-text-field
          v-if="isLastHousehold"
          v-model="confirmDeleteName"
          :label="`Type &quot;${householdToDelete?.name || ''}&quot; to confirm`"
          variant="outlined"
          density="comfortable"
          autocomplete="off"
          class="mt-4"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="grey" variant="text" autofocus @click="deleteHouseholdDialog = false">
          Cancel
        </v-btn>
        <v-btn
          color="red"
          variant="flat"
          :loading="deletingHousehold"
          :disabled="
            isLastHousehold && confirmDeleteName.trim() !== (householdToDelete?.name || '').trim()
          "
          @click="executeDeleteHousehold"
        >
          Delete Forever
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import api from '@/services/api'
import NewHouseholdDialog from '@/components/NewHouseholdDialog.vue'

const open = defineModel({ type: Boolean })

const props = defineProps({
  households: Array,
  currentId: Number,
})

const emit = defineEmits(['select', 'created', 'updated', 'deleted'])

const isLastHousehold = computed(() => (props.households?.length ?? 0) <= 1)

const deleteHouseholdDialog = ref(false)
const deletingHousehold = ref(false)
const householdToDelete = ref(null)
const confirmDeleteName = ref('')

const renameDialog = ref(false)
const renamingHousehold = ref(false)
const renameValid = ref(false)
const householdToRename = ref(null)
const renameName = ref('')

const showCreate = ref(false)

watch(deleteHouseholdDialog, (isOpen) => {
  if (!isOpen) {
    confirmDeleteName.value = ''
  }
})

watch(renameDialog, (isOpen) => {
  if (!isOpen) {
    householdToRename.value = null
    renameName.value = ''
  }
})

function handleCreate(newHousehold) {
  showCreate.value = false
  emit('created', newHousehold)
}

function openRenameHousehold(household) {
  householdToRename.value = household
  renameName.value = household.name || ''
  renameDialog.value = true
}

async function executeRenameHousehold() {
  const trimmedName = renameName.value.trim()
  if (!householdToRename.value || !trimmedName) return
  renamingHousehold.value = true
  try {
    const formData = new FormData()
    formData.append('name', trimmedName)
    const res = await api.put(`/households/${householdToRename.value.id}`, formData)
    renameDialog.value = false
    householdToRename.value = null
    emit('updated', res.data)
  } catch (e) {
    console.error('Failed to rename household', e)
  } finally {
    renamingHousehold.value = false
  }
}

function confirmDeleteHousehold(household) {
  householdToDelete.value = household
  confirmDeleteName.value = ''
  deleteHouseholdDialog.value = true
}

async function executeDeleteHousehold() {
  if (!householdToDelete.value) return
  if (
    isLastHousehold.value &&
    confirmDeleteName.value.trim() !== (householdToDelete.value.name || '').trim()
  ) {
    return
  }
  deletingHousehold.value = true
  try {
    const household = householdToDelete.value
    await api.delete(`/households/${household.id}`)
    deleteHouseholdDialog.value = false
    householdToDelete.value = null
    confirmDeleteName.value = ''
    emit('deleted', household)
  } catch (e) {
    console.error('Failed to delete household', e)
  } finally {
    deletingHousehold.value = false
  }
}
</script>
