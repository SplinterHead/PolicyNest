<template>
  <div>
    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-h4 font-weight-thin">Inventory</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" size="large" @click="dialog = true">
          Add Vehicle
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="asset in assets" :key="asset.id" cols="12" sm="6" md="4">
        <v-card rounded="lg" elevation="2" class="h-100 position-relative">
          <v-card-item>
            <v-btn
              icon="mdi-delete"
              variant="text"
              color="red-lighten-1"
              size="small"
              class="position-absolute top-0 right-0 ma-2"
              style="z-index: 10"
              @click.stop="confirmDelete(asset)"
            />
            <template v-slot:prepend>
              <v-avatar color="primary" variant="tonal" rounded="0">
                <v-icon icon="mdi-car" />
              </v-avatar>
            </template>
            <v-card-title>{{ asset.name }}</v-card-title>
            <v-card-subtitle>{{ asset.details.make }} {{ asset.details.model }}</v-card-subtitle>
          </v-card-item>
          <v-divider />
          <v-card-text>
            <div class="d-flex justify-space-between">
              <span class="text-medium-emphasis">Registration</span>
              <span class="font-weight-bold">{{ asset.details.reg }}</span>
            </div>
            <div class="d-flex justify-space-between mt-2">
              <span class="text-medium-emphasis">VIN</span>
              <span class="font-weight-mono text-caption">{{ asset.details.vin || 'N/A' }}</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Add Vehicle</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="form.name"
            label="Nickname (e.g. Dad's Car)"
            variant="outlined"
            class="mb-2"
          />
          <v-text-field v-model="form.make" label="Make" variant="outlined" density="compact" />
          <v-text-field v-model="form.model" label="Model" variant="outlined" density="compact" />
          <v-text-field
            v-model="form.reg"
            label="Registration Plate"
            variant="outlined"
            density="compact"
          />
          <v-text-field
            v-model="form.vin"
            label="VIN (Optional)"
            variant="outlined"
            density="compact"
          />
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" variant="flat" @click="saveAsset" :loading="saving">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5 text-red">Delete Asset?</v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ assetToDelete?.name }}</strong
          >? <br /><br />
          <v-alert type="warning" variant="tonal" density="compact" border="start">
            This action cannot be undone. Any policies linked to this
            {{ assetToDelete?.type.toLowerCase() }} will also be deleted.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" variant="flat" @click="executeDelete" :loading="deleting">
            Delete Forever
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  props: { currentHousehold: Object },
  data() {
    return {
      assets: [],
      assetToDelete: null,
      deleteDialog: false,
      deleting: false,
      dialog: false,
      form: { name: '', make: '', model: '', reg: '', vin: '' },
      saving: false,
    }
  },
  watch: {
    currentHousehold: {
      immediate: true,
      handler(val) {
        if (val) this.fetchAssets()
      },
    },
  },
  methods: {
    confirmDelete(asset) {
      this.assetToDelete = asset
      this.deleteDialog = true
    },
    async executeDelete() {
      if (!this.assetToDelete) return
      this.deleting = true
      try {
        await api.delete(`/assets/${this.assetToDelete.id}`)
        this.assets = this.assets.filter((a) => a.id !== this.assetToDelete.id)
        this.deleteDialog = false
        this.assetToDelete = null
      } catch (e) {
        console.error('Delete failed', e)
      } finally {
        this.deleting = false
      }
    },
    async fetchAssets() {
      const res = await api.get(`/assets/?household_id=${this.currentHousehold.id}`)
      this.assets = res.data
    },
    async saveAsset() {
      this.saving = true
      const details = {
        make: this.form.make,
        model: this.form.model,
        reg: this.form.reg,
        vin: this.form.vin,
      }

      let formData = new FormData()
      formData.append('household_id', this.currentHousehold.id)
      formData.append('name', this.form.name)
      formData.append('type', 'Vehicle')
      formData.append('details', JSON.stringify(details))

      await api.post('/assets/', formData)
      this.fetchAssets()
      this.dialog = false
      this.saving = false
      this.form = { name: '', make: '', model: '', reg: '', vin: '' }
    },
  },
}
</script>
