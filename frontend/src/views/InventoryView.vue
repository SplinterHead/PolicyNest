<template>
  <div>
    <v-row class="mb-4" align="center">
      <v-col>
        <div class="text-caption text-medium-emphasis">INVENTORY</div>
        <h1 class="text-h4 font-weight-thin">My Assets</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" size="large" @click="dialog = true">
          Add Vehicle
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="asset in assets" :key="asset.id" cols="12" sm="6" md="4">
        <v-card variant="outlined" class="fill-height">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="primary" variant="tonal" rounded="0">
                <v-icon icon="mdi-car"></v-icon>
              </v-avatar>
            </template>
            <v-card-title>{{ asset.name }}</v-card-title>
            <v-card-subtitle>{{ asset.details.make }} {{ asset.details.model }}</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
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
          ></v-text-field>
          <v-text-field
            v-model="form.make"
            label="Make"
            variant="outlined"
            density="compact"
          ></v-text-field>
          <v-text-field
            v-model="form.model"
            label="Model"
            variant="outlined"
            density="compact"
          ></v-text-field>
          <v-text-field
            v-model="form.reg"
            label="Registration Plate"
            variant="outlined"
            density="compact"
          ></v-text-field>
          <v-text-field
            v-model="form.vin"
            label="VIN (Optional)"
            variant="outlined"
            density="compact"
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" variant="flat" @click="saveAsset" :loading="saving">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: { currentHousehold: Object },
  data() {
    return {
      assets: [],
      dialog: false,
      saving: false,
      form: { name: '', make: '', model: '', reg: '', vin: '' },
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
    async fetchAssets() {
      const res = await axios.get(
        `http://localhost:8000/assets/?household_id=${this.currentHousehold.id}`,
      )
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

      await axios.post('http://localhost:8000/assets/', formData)
      this.fetchAssets()
      this.dialog = false
      this.saving = false
      this.form = { name: '', make: '', model: '', reg: '', vin: '' }
    },
  },
}
</script>
