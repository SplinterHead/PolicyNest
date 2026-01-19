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
            :color="getTypeColor(item.type)"
            size="small"
            variant="flat"
            class="font-weight-bold"
          >
            {{ item.type }}
          </v-chip>
        </template>
        <template v-slot:item.start_date="{ item }">
          <div>
            {{ new Date(item.start_date).toLocaleDateString() }}
          </div>
        </template>
        <template v-slot:item.end_date="{ item }">
          <div v-if="!item.end_date">Perpetual</div>
          <div v-else>
            {{ new Date(item.end_date).toLocaleDateString() }}
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
              <v-icon>mdi-pencil</v-icon>
              <v-tooltip activator="parent" location="top">Edit</v-tooltip>
            </v-btn>

            <v-btn icon size="small" variant="text" color="red" @click.stop="confirmDelete(item)">
              <v-icon>mdi-delete</v-icon>
              <v-tooltip activator="parent" location="top">Delete</v-tooltip>
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="showDetail" width="80%" scrollable>
      <v-card v-if="selectedPolicy" rounded="lg">
        <v-toolbar :color="getTypeColor(selectedPolicy.type)">
          <v-toolbar-title class="font-weight-bold text-white">
            {{ selectedPolicy.provider }}
            <span class="text-subtitle-2 ml-2 opacity-80 text-white">
              {{ selectedPolicy.type }} Policy
            </span>
          </v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="showDetail = false" color="white">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text
          class="pa-0"
          :class="isDark ? 'bg-grey-darken-4' : 'bg-grey-lighten-5'"
          style="height: 85vh"
        >
          <v-container fluid class="pa-6">
            <v-row>
              <v-col cols="12" md="4">
                <v-card variant="flat" class="pa-4 border bg-surface">
                  <div class="text-caption text-medium-emphasis mb-1">Premium</div>
                  <div class="text-h5 font-weight-bold text-primary">
                    {{ formatCurrency(selectedPolicy.premium) }}
                  </div>
                  <div class="text-caption mt-1">Per Year</div>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card variant="flat" class="pa-4 border bg-surface">
                  <div class="text-caption text-medium-emphasis mb-1">Policy Start</div>
                  <div class="text-h6">{{ formatDate(selectedPolicy.start_date) }}</div>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card variant="flat" class="pa-4 border bg-surface">
                  <div class="text-caption text-medium-emphasis mb-1">Policy Renewal</div>
                  <div class="text-h6" :class="getRenewalColor(selectedPolicy.end_date)">
                    {{ formatDate(selectedPolicy.end_date) }}
                  </div>
                </v-card>
              </v-col>
            </v-row>

            <v-row class="mt-2" v-if="['Car', 'Life'].includes(selectedPolicy.type)">
              <v-col cols="12">
                <v-card class="pa-4 bg-surface" border variant="flat">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center">
                    <v-icon icon="mdi-list-box-outline" class="mr-2" color="primary"></v-icon>
                    Policy Details
                  </div>

                  <div v-if="selectedPolicy.type === 'Car'">
                    <v-row dense>
                      <v-col cols="12" md="6">
                        <v-list density="compact" class="bg-transparent">
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon size="small" class="mr-4">mdi-identifier</v-icon>
                            </template>
                            <v-list-item-title>Reg Plate</v-list-item-title>
                            <template v-slot:append
                              ><v-chip
                                size="small"
                                variant="outlined"
                                class="text-uppercase font-weight-bold"
                                >{{ selectedPolicy.attributes.reg_number || 'N/A' }}</v-chip
                              ></template
                            >
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend
                              ><v-icon size="small" class="mr-4"
                                >mdi-shield-half-full</v-icon
                              ></template
                            >
                            <v-list-item-title>Cover Level</v-list-item-title>
                            <template v-slot:append
                              ><span class="font-weight-medium">{{
                                selectedPolicy.attributes.cover_level
                              }}</span></template
                            >
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend
                              ><v-icon size="small" class="mr-4">mdi-cash-minus</v-icon>
                            </template>
                            <v-list-item-title>Total Excess</v-list-item-title>
                            <template v-slot:append
                              ><span class="font-weight-bold text-red">{{
                                formatCurrency(
                                  (selectedPolicy.attributes.excess_voluntary || 0) +
                                    (selectedPolicy.attributes.excess_compulsory || 0),
                                )
                              }}</span></template
                            >
                          </v-list-item>
                        </v-list>
                      </v-col>

                      <v-col cols="12" md="6">
                        <div class="d-flex flex-wrap gap-2 mt-2">
                          <v-chip
                            :color="selectedPolicy.attributes.courtesy_car ? 'green' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.courtesy_car ? 'mdi-check' : 'mdi-close'
                              "
                            ></v-icon>
                            Courtesy Car
                          </v-chip>
                          <v-chip
                            :color="selectedPolicy.attributes.legal_cover ? 'green' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.legal_cover ? 'mdi-check' : 'mdi-close'
                              "
                            ></v-icon>
                            Legal Cover
                          </v-chip>
                          <v-chip
                            :color="selectedPolicy.attributes.breakdown ? 'green' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.breakdown ? 'mdi-check' : 'mdi-close'
                              "
                            ></v-icon>
                            Breakdown
                          </v-chip>
                          <v-chip
                            :color="selectedPolicy.attributes.windscreen ? 'green' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.windscreen ? 'mdi-check' : 'mdi-close'
                              "
                            ></v-icon>
                            Windscreen
                          </v-chip>
                        </div>
                      </v-col>
                    </v-row>
                  </div>
                  <div v-else-if="selectedPolicy.type === 'Life'">
                    <v-row dense>
                      <v-col cols="12" md="6">
                        <v-list density="compact" class="bg-transparent">
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon size="small" class="mr-4">mdi-shield-star</v-icon>
                            </template>
                            <v-list-item-title>Cover Type</v-list-item-title>
                            <template v-slot:append>
                              <span class="font-weight-medium">
                                {{ selectedPolicy.attributes.cover_type || 'Level Term' }}
                              </span>
                            </template>
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon size="small" class="mr-4"> mdi-account-group </v-icon>
                            </template>
                            <v-list-item-title>Beneficiaries</v-list-item-title>
                            <template v-slot:append>
                              <div
                                class="text-right text-caption font-weight-bold"
                                style="max-width: 150px"
                              >
                                {{ selectedPolicy.attributes.beneficiaries || '-' }}
                              </div>
                            </template>
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon size="small" class="mr-4">mdi-piggy-bank</v-icon>
                            </template>
                            <v-list-item-title>Sum Assured</v-list-item-title>
                            <template v-slot:append>
                              <span class="text-h6 font-weight-bold text-success">
                                {{ formatCurrency(selectedPolicy.attributes.sum_assured || 0) }}
                              </span>
                            </template>
                          </v-list-item>
                        </v-list>
                      </v-col>

                      <v-col cols="12" md="6">
                        <div class="d-flex flex-wrap gap-2 mt-2">
                          <v-chip
                            :color="selectedPolicy.attributes.joint_policy ? 'purple' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.joint_policy
                                  ? 'mdi-account-multiple-check'
                                  : 'mdi-account'
                              "
                            />
                            {{
                              selectedPolicy.attributes.joint_policy
                                ? 'Joint Policy'
                                : 'Single Policy'
                            }}
                          </v-chip>

                          <v-chip
                            :color="
                              selectedPolicy.attributes.critical_illness ? 'green' : 'default'
                            "
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.critical_illness
                                  ? 'mdi-check'
                                  : 'mdi-close'
                              "
                            />
                            Critical Illness
                          </v-chip>

                          <v-chip
                            :color="selectedPolicy.attributes.in_trust ? 'blue' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.in_trust ? 'mdi-bank' : 'mdi-bank-outline'
                              "
                            />
                            In Trust
                          </v-chip>

                          <v-chip
                            :color="selectedPolicy.attributes.waiver_premium ? 'green' : 'default'"
                            variant="tonal"
                          >
                            <v-icon
                              start
                              :icon="
                                selectedPolicy.attributes.waiver_premium ? 'mdi-check' : 'mdi-close'
                              "
                            />
                            Waiver of Premium
                          </v-chip>
                        </div>
                      </v-col>
                    </v-row>
                  </div>
                </v-card>
              </v-col>
            </v-row>

            <v-row class="mt-2">
              <v-col cols="12">
                <div class="text-subtitle-1 font-weight-bold mb-2">Policy Document</div>

                <v-card
                  height="600px"
                  border
                  class="d-flex align-center justify-center overflow-hidden position-relative"
                  :class="[
                    selectedPolicy.document_path ? 'bg-white' : 'bg-surface',
                    isDragging ? 'border-primary border-dashed bg-blue-lighten-5' : '',
                  ]"
                  @dragover.prevent="isDragging = true"
                  @dragleave.prevent="isDragging = false"
                  @drop.prevent="handleDrop"
                >
                  <object
                    v-if="selectedPolicy.document_path"
                    :data="getDocumentUrl(selectedPolicy.document_path)"
                    type="application/pdf"
                    width="100%"
                    height="100%"
                  >
                    <div class="text-center text-black">
                      <v-icon size="64" color="grey">mdi-file-pdf-box</v-icon>
                      <div class="mt-2">Preview not supported.</div>
                      <v-btn
                        color="primary"
                        class="mt-4"
                        :href="getDocumentUrl(selectedPolicy.document_path)"
                        target="_blank"
                      >
                        Download PDF
                      </v-btn>
                    </div>
                  </object>

                  <div v-else-if="isUploading" class="text-center">
                    <v-progress-circular indeterminate color="primary" size="64" />
                    <div class="mt-4 font-weight-bold text-primary">Uploading...</div>
                  </div>

                  <div v-else class="text-center cursor-pointer" @click="triggerFileInput">
                    <v-avatar color="grey-lighten-3" size="80" class="mb-4">
                      <v-icon size="40" :color="isDragging ? 'primary' : 'grey-darken-1'">
                        {{ isDragging ? 'mdi-arrow-up-bold' : 'mdi-cloud-upload' }}
                      </v-icon>
                    </v-avatar>

                    <h3 class="text-h6 font-weight-bold" :class="isDragging ? 'text-primary' : ''">
                      {{ isDragging ? 'Drop file to upload' : 'No Document Uploaded' }}
                    </h3>
                    <div class="text-body-2 text-medium-emphasis mt-1">
                      Drag & Drop a PDF here, or click to browse
                    </div>

                    <input
                      type="file"
                      ref="fileInput"
                      class="d-none"
                      accept=".pdf"
                      @change="handleFileSelect"
                    />
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>

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
import api, { getFileUrl } from '../services/api'

export default {
  props: {
    currencyCode: String,
    loading: Boolean,
    policies: Array,
  },
  emits: ['edit', 'delete'],
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  data() {
    return {
      deleteDialog: false,
      isDragging: false,
      isUploading: false,
      policyToDelete: null,
      selectedPolicy: null,
      showDetail: false,
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
    openPolicy(event, { item }) {
      this.selectedPolicy = item
      this.showDetail = true
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: this.currencyCode,
        currencyDisplay: 'narrowSymbol',
      }).format(value)
    },
    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      })
    },
    getTypeColor(type) {
      const colors = { Car: 'blue', Home: 'orange', Life: 'green', Medical: 'red', Pet: 'purple' }
      return colors[type] || 'grey'
    },
    getRenewalColor(dateStr) {
      const daysLeft = (new Date(dateStr) - new Date()) / (1000 * 60 * 60 * 24)
      if (daysLeft < 0) return 'text-red font-weight-bold'
      if (daysLeft < 30) return 'text-orange font-weight-bold'
      return 'text-success'
    },
    getDocumentUrl(path) {
      return getFileUrl(path)
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) this.uploadDocument(file)
    },
    handleDrop(event) {
      this.isDragging = false
      const file = event.dataTransfer.files[0]
      if (file && file.type === 'application/pdf') {
        this.uploadDocument(file)
      } else {
        alert('Please upload a PDF file.')
      }
    },
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
    async uploadDocument(file) {
      this.isUploading = true
      let formData = new FormData()
      formData.append('file', file)

      try {
        const res = await api.put(`/policies/${this.selectedPolicy.id}/document`, formData)
        this.selectedPolicy.document_path = res.data.document_path
        const index = this.policies.findIndex((p) => p.id === this.selectedPolicy.id)
        if (index !== -1) {
          this.policies[index].document_path = res.data.document_path
        }
      } catch (e) {
        console.error('Upload failed', e)
        alert('Failed to upload document')
      } finally {
        this.isUploading = false
      }
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
