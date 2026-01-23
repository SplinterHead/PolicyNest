<template>
  <div>
    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-h4 font-weight-thin">Inventory</h1>
      </v-col>
    </v-row>

    <v-fab app color="primary" location="right bottom" size="large" icon>
      <v-icon :icon="openFab ? 'mdi-close' : 'mdi-plus'" />
      <v-speed-dial
        v-model="openFab"
        location="top left"
        transition="slide-y-reverse-transition"
        activator="parent"
      >
        <v-btn
          v-for="(config, type) in createOptions"
          :key="type"
          :color="config.colour"
          :prepend-icon="config.icon"
          rounded="xl"
          size="large"
          width="150"
          @click="openCreateDialog(type)"
        >
          {{ config.label }}
        </v-btn>
      </v-speed-dial>
    </v-fab>

    <div v-for="group in groupedAssets" :key="group.type" class="mb-8">
      <div class="d-flex align-center mb-3">
        <v-icon :icon="getAssetIcon(group.type)" size="large" class="mr-2" />
        <h2 class="text-h5 font-weight-light">
          {{ group.label }}
        </h2>
        <v-divider class="ml-4" />
      </div>

      <v-row>
        <v-col v-for="asset in group.items" :key="asset.id" cols="12" sm="6" md="4">
          <v-card rounded="lg" elevation="2" class="h-100 position-relative">
            <v-btn
              icon="mdi-delete"
              variant="text"
              color="red-lighten-1"
              size="small"
              class="position-absolute top-0 right-0 ma-2"
              style="z-index: 10"
              @click.stop="confirmDelete(asset)"
            />

            <v-card-item>
              <template v-slot:prepend>
                <v-avatar :color="getAssetColor(asset.type)" variant="tonal" rounded="0">
                  <v-icon :icon="getAssetIcon(asset.type)" />
                </v-avatar>
              </template>
              <v-card-title>{{ asset.name }}</v-card-title>

              <v-card-subtitle v-if="asset.type === 'Vehicle'">
                {{ asset.details.make }} {{ asset.details.model }}
              </v-card-subtitle>
              <v-card-subtitle v-else-if="asset.type === 'Pet'">
                {{ asset.details.species }} - {{ asset.details.breed }}
              </v-card-subtitle>
            </v-card-item>

            <v-divider />

            <v-card-text>
              <div v-if="asset.type === 'Vehicle'">
                <div class="d-flex justify-space-between">
                  <span class="text-medium-emphasis">Registration</span>
                  <span class="font-weight-bold">{{ asset.details.reg }}</span>
                </div>
                <div class="d-flex justify-space-between mt-2">
                  <span class="text-medium-emphasis">VIN</span>
                  <span class="font-weight-mono text-caption">
                    {{ asset.details.vin || 'N/A' }}
                  </span>
                </div>
              </div>

              <div v-else-if="asset.type === 'Pet'">
                <div class="d-flex justify-space-between">
                  <span class="text-medium-emphasis">Color</span>
                  <span>{{ asset.details.color || 'N/A' }}</span>
                </div>
                <div class="d-flex justify-space-between mt-2">
                  <span class="text-medium-emphasis">Microchip</span>
                  <span class="font-weight-mono">{{ asset.details.chip_id || 'N/A' }}</span>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <div v-if="assets.length === 0" class="text-center mt-12 text-medium-emphasis">
      <v-icon icon="mdi-package-variant" size="64" class="mb-4" />
      <div class="text-h6">No assets found</div>
      <div>Click the + button to add your first asset.</div>
    </div>

    <AssetDialog
      v-model="dialog"
      :type="dialogType"
      :household-id="currentHousehold?.id"
      @saved="fetchAssets"
    />

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5 text-red">Delete Asset?</v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ assetToDelete?.name }}</strong
          >?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" variant="flat" @click="executeDelete" :loading="deleting">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '@/services/api'
import { AssetTypes, getAssetColour, getAssetIcon } from '@/utils/AssetTypes'
import AssetDialog from '@/components/AssetDialog.vue'

export default {
  name: 'InventoryView',
  components: { AssetDialog },
  props: { currentHousehold: Object },
  data() {
    return {
      assets: [],
      assetTheme: AssetTypes,
      dialog: false,
      dialogType: 'Vehicle',
      deleteDialog: false,
      assetToDelete: null,
      deleting: false,
      openFab: false,
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
  computed: {
    createOptions() {
      return this.assetTheme
    },
    groupedAssets() {
      const groups = {}
      this.assets.forEach((asset) => {
        if (!groups[asset.type]) {
          groups[asset.type] = []
        }
        groups[asset.type].push(asset)
      })
      const orderedTypes = ['Vehicle', 'Pet']
      const activeTypes = Object.keys(groups)
      return activeTypes
        .sort((a, b) => {
          const idxA = orderedTypes.indexOf(a)
          const idxB = orderedTypes.indexOf(b)
          return (idxA === -1 ? 999 : idxA) - (idxB === -1 ? 999 : idxB)
        })
        .map((type) => ({
          type: type,
          label: type + 's',
          items: groups[type],
        }))
    },
  },
  methods: {
    openCreateDialog(type) {
      this.dialogType = type
      this.dialog = true
    },
    getAssetColor(type) {
      return getAssetColour(type)
    },
    getAssetIcon(type) {
      return getAssetIcon(type)
    },
    async fetchAssets() {
      if (!this.currentHousehold) return
      try {
        const res = await api.get(`/assets/?household_id=${this.currentHousehold.id}`)
        this.assets = res.data
      } catch (e) {
        console.error(e)
      }
    },
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
  },
}
</script>
