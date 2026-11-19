<template>
  <div>
    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-headline-large font-weight-light">Inventory</h1>
      </v-col>
    </v-row>

    <v-fab app color="primary" location="right bottom" size="large" style="z-index: 900" icon>
      <v-icon :icon="openFab ? 'mdi-close' : 'mdi-plus'" />
      <v-speed-dial
        v-model="openFab"
        location="top left"
        transition="slide-y-reverse-transition"
        activator="parent"
        scrim
        :activator-props="{ 'aria-label': openFab ? 'Close new asset menu' : 'Add asset' }"
      >
        <v-btn
          v-for="(config, type) in AssetTypes"
          :key="type"
          :color="config.colour"
          :prepend-icon="config.icon"
          rounded="xl"
          size="large"
          width="160"
          class="justify-start px-4"
          @click="openCreateDialog(type)"
        >
          {{ config.label }}
        </v-btn>
      </v-speed-dial>
    </v-fab>

    <div v-for="group in groupedAssets" :key="group.type" class="mb-8">
      <div class="d-flex align-center mb-3">
        <v-icon :icon="getAssetIcon(group.type)" class="mr-2" />
        <h2 class="text-headline-small font-weight-light">
          {{ group.label }}
        </h2>
        <v-divider class="ml-4" />
      </div>

      <div class="asset-grid">
        <v-card
          v-for="asset in group.items"
          :key="asset.id"
          tag="article"
          rounded="lg"
          elevation="2"
          class="asset-card h-100"
        >
          <v-card-item>
            <template #prepend>
              <v-avatar :color="getAssetColour(asset.type, isDark)" variant="tonal" rounded="0">
                <v-icon :icon="getAssetIcon(asset.type)" />
              </v-avatar>
            </template>
            <v-card-title>{{ asset.name }}</v-card-title>

            <v-card-subtitle v-if="asset.type === 'Vehicle'">
              {{ [asset.details.make, asset.details.model].filter(Boolean).join(' ') || 'Vehicle' }}
            </v-card-subtitle>
            <v-card-subtitle v-else-if="asset.type === 'Pet'">
              {{
                [asset.details.species, asset.details.breed].filter(Boolean).join(' - ') || 'Pet'
              }}
            </v-card-subtitle>

            <template #append>
              <div class="d-flex align-center ga-1">
                <v-icon-btn
                  icon="mdi-pencil-outline"
                  variant="text"
                  class="card-action-btn"
                  :aria-label="`Edit ${asset.name}`"
                  @click.stop="openEditDialog(asset)"
                />
                <v-icon-btn
                  icon="mdi-delete-outline"
                  variant="text"
                  color="error"
                  class="card-action-btn"
                  :aria-label="`Delete ${asset.name}`"
                  @click.stop="confirmDelete(asset)"
                />
              </div>
            </template>
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
                <span class="text-mono text-body-small">
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
                <span class="text-mono">{{ asset.details.chip_id || 'N/A' }}</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </div>
    </div>

    <div v-if="assets.length === 0" class="text-center mt-12 text-medium-emphasis">
      <v-icon icon="mdi-package-variant" size="64" class="mb-4" />
      <div class="text-title-large">No assets found</div>
      <div>Click the + button to add your first asset.</div>
    </div>

    <AssetDialog
      v-model="dialog"
      :type="dialogType"
      :household-id="currentHousehold?.id"
      :asset-to-edit="assetToEdit"
      @saved="fetchAssets"
    />

    <v-dialog v-model="deleteDialog" max-width="400px" aria-labelledby="delete-asset-title">
      <v-card>
        <v-card-title id="delete-asset-title" class="text-headline-small text-red">
          Delete Asset?
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ assetToDelete?.name }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" variant="flat" :loading="deleting" @click="executeDelete">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useTheme } from 'vuetify'
import api from '@/services/api'
import { AssetTypes, getAssetColour, getAssetIcon } from '@/utils/AssetTypes'
import AssetDialog from '@/components/AssetDialog.vue'

const props = defineProps({
  currentHousehold: Object,
})

const theme = useTheme()
const isDark = computed(() => theme.current.value.dark)

const assets = ref([])
const assetToEdit = ref(null)
const dialog = ref(false)
const dialogType = ref('Vehicle')
const deleteDialog = ref(false)
const assetToDelete = ref(null)
const deleting = ref(false)
const openFab = ref(false)

const groupedAssets = computed(() => {
  const groups = {}
  assets.value.forEach((asset) => {
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
      type,
      label: `${type}s`,
      items: groups[type],
    }))
})

function openCreateDialog(type) {
  openFab.value = false
  assetToEdit.value = null
  dialogType.value = type
  dialog.value = true
}

function openEditDialog(asset) {
  assetToEdit.value = asset
  dialogType.value = asset.type
  dialog.value = true
}

watch(dialog, (isOpen) => {
  if (!isOpen) {
    assetToEdit.value = null
  }
})

async function fetchAssets() {
  if (!props.currentHousehold) return
  try {
    const res = await api.get(`/assets/?household_id=${props.currentHousehold.id}`)
    assets.value = res.data
  } catch (e) {
    console.error(e)
  }
}

function confirmDelete(asset) {
  assetToDelete.value = asset
  deleteDialog.value = true
}

async function executeDelete() {
  if (!assetToDelete.value) return
  deleting.value = true
  try {
    await api.delete(`/assets/${assetToDelete.value.id}`)
    assets.value = assets.value.filter((a) => a.id !== assetToDelete.value.id)
    deleteDialog.value = false
    assetToDelete.value = null
  } catch (e) {
    console.error('Delete failed', e)
  } finally {
    deleting.value = false
  }
}

watch(
  () => props.currentHousehold,
  (val) => {
    if (val) fetchAssets()
  },
  { immediate: true },
)
</script>

<style scoped>
.asset-grid {
  display: grid;
  inline-size: 100%;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 380px), 1fr));
  gap: 1.5rem;
}

.asset-grid > * {
  min-inline-size: 0;
}

.asset-card {
  transition: box-shadow 0.2s ease;
}

.asset-card:hover {
  box-shadow:
    0 4px 10px -1px rgba(var(--v-shadow-color), 0.16),
    0 2px 6px -1px rgba(var(--v-shadow-color), 0.12) !important;
}

.card-action-btn {
  min-inline-size: 44px;
  min-block-size: 44px;
}
</style>
