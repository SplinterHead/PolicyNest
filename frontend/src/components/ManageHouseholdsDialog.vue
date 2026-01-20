<template>
  <v-dialog
    :model-value="modelValue"
    max-width="500px"
    @update:modelValue="$emit('update:modelValue', $event)"
  >
    <v-card>
      <v-toolbar color="transparent" density="compact">
        <v-toolbar-title class="text-h6">My Households</v-toolbar-title>
        <v-spacer />
        <v-btn icon="mdi-close" @click="$emit('update:modelValue', false)" />
      </v-toolbar>

      <v-card-text class="pa-0">
        <v-list lines="two">
          <v-list-item
            v-for="house in households"
            :key="house.id"
            :active="house.id === currentId"
            color="primary"
            @click="$emit('select', house)"
          >
            <template v-slot:prepend>
              <v-icon :icon="house.id === currentId ? 'mdi-home' : 'mdi-home-outline'" />
            </template>

            <v-list-item-title>{{ house.name }}</v-list-item-title>
            <v-list-item-subtitle v-if="house.id === currentId"
              >Currently Selected</v-list-item-subtitle
            >

            <template v-slot:append>
              <v-icon v-if="house.id === currentId" color="primary" icon="mdi-check" />
              <v-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="grey"
                class="ml-2"
                @click="confirmDeleteHousehold(house)"
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

  <v-dialog v-model="deleteHouseholdDialog" max-width="500px">
    <v-card>
      <v-card-title class="text-h5 text-red">Delete Household?</v-card-title>
      <v-card-text>
        Are you sure you want to delete
        <strong>{{ householdToDelete?.name }}</strong
        >? <br /><br />
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
          @click="executeDeleteHousehold"
          :loading="deletingHousehold"
        >
          Delete Forever
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from '../services/api'
import NewHouseholdDialog from './NewHouseholdDialog.vue'

export default {
  components: { NewHouseholdDialog },
  props: {
    modelValue: Boolean,
    households: Array,
    currentId: Number,
  },
  emits: ['update:modelValue', 'select', 'created'],
  data() {
    return {
      deleteHouseholdDialog: false,
      deletingHousehold: false,
      householdToDelete: null,
      showCreate: false,
    }
  },
  methods: {
    handleCreate(newHousehold) {
      this.showCreate = false
      this.$emit('created', newHousehold)
    },
    confirmDeleteHousehold(household) {
      this.householdToDelete = household
      this.deleteHouseholdDialog = true
    },
    async executeDeleteHousehold() {
      if (!this.householdToDelete) return
      this.deletingHousehold = true
      try {
        const household = this.householdToDelete
        await api.delete(`/households/${household.id}`)
        this.deleteHouseholdDialog = false
        this.householdToDelete = null
        this.$emit('deleted', household)
      } catch (e) {
        console.error('Failed to delete household', e)
      } finally {
        this.deletingHousehold = false
      }
    },
  },
}
</script>
