<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    width="80%"
    scrollable
  >
    <v-card rounded="lg">
      <v-toolbar :color="getHeaderColor(policy.type)">
        <v-toolbar-title class="font-weight-bold text-white">
          {{ policy.provider }}
          <span class="text-subtitle-2 ml-2 opacity-80 text-white"> {{ policy.type }} Policy </span>
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon="mdi-close" @click="$emit('update:modelValue', false)" />
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
                  {{ formatCurrency(policy.premium) }}
                </div>
                <div class="text-caption mt-1">Per Year</div>
              </v-card>
            </v-col>
            <v-col cols="12" md="4">
              <v-card variant="flat" class="pa-4 border bg-surface">
                <div class="text-caption text-medium-emphasis mb-1">Policy Start</div>
                <div class="text-h6">{{ formatDate(policy.start_date) }}</div>
              </v-card>
            </v-col>
            <v-col cols="12" md="4">
              <v-card variant="flat" class="pa-4 border bg-surface">
                <div class="text-caption text-medium-emphasis mb-1">Policy Renewal</div>
                <div class="text-h6" :class="getRenewalColor(policy.end_date)">
                  {{ formatDate(policy.end_date) }}
                </div>
              </v-card>
            </v-col>
          </v-row>

          <v-row class="mt-2">
            <v-col cols="12">
              <v-card class="pa-4 bg-surface" border variant="flat">
                <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center">
                  <v-icon icon="mdi-list-box-outline" class="mr-2" color="primary" />
                  Policy Details
                </div>

                <div>
                  <v-row dense>
                    <BuildingsPolicyDetails
                      v-if="policy.type === 'Buildings'"
                      :attributes="policy.attributes"
                      :currencyCode="currencyCode"
                    />
                    <CarPolicyDetails
                      v-if="policy.type === 'Car'"
                      :attributes="policy.attributes"
                      :currencyCode="currencyCode"
                    />
                    <ContentsPolicyDetails
                      v-if="policy.type === 'Contents'"
                      :attributes="policy.attributes"
                      :currencyCode="currencyCode"
                    />
                    <LifePolicyDetails
                      v-if="policy.type === 'Life'"
                      :attributes="policy.attributes"
                      :currencyCode="currencyCode"
                    />
                    <MedicalPolicyDetails
                      v-if="policy.type === 'Medical'"
                      :attributes="policy.attributes"
                      :currencyCode="currencyCode"
                    />
                    <PetPolicyDetails
                      v-if="policy.type === 'Pet'"
                      :attributes="policy.attributes"
                    />
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
                  policy.document_path ? 'bg-white' : 'bg-surface',
                  isDragging ? 'border-primary border-dashed bg-blue-lighten-5' : '',
                ]"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
              >
                <object
                  v-if="policy.document_path"
                  :data="getDocumentUrl(policy.document_path)"
                  type="application/pdf"
                  width="100%"
                  height="100%"
                >
                  <div class="text-center text-black">
                    <v-icon icon="mdi-file-pdf-box" size="64" color="grey" />
                    <div class="mt-2">Preview not supported.</div>
                    <v-btn
                      color="primary"
                      class="mt-4"
                      :href="getDocumentUrl(policy.document_path)"
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
                    <v-icon
                      size="40"
                      :color="isDragging ? 'primary' : 'grey-darken-1'"
                      :icon="isDragging ? 'mdi-arrow-up-bold' : 'mdi-cloud-upload'"
                    />
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
</template>

<script>
import { getFileUrl } from '../services/api'

import BuildingsPolicyDetails from './details/BuildingsPolicyDetails.vue'
import CarPolicyDetails from './details/CarPolicyDetails.vue'
import ContentsPolicyDetails from './details/ContentsPolicyDetails.vue'
import LifePolicyDetails from './details/LifePolicyDetails.vue'
import MedicalPolicyDetails from './details/MedicalPolicyDetails.vue'
import PetPolicyDetails from './details/PetPolicyDetails.vue'

export default {
  name: 'PolicyDetailsDialog',
  components: {
    BuildingsPolicyDetails,
    CarPolicyDetails,
    ContentsPolicyDetails,
    LifePolicyDetails,
    MedicalPolicyDetails,
    PetPolicyDetails,
  },
  props: {
    currencyCode: String,
    modelValue: Boolean,
    policy: Object,
  },
  emits: ['update:modelValue', 'edit'],
  computed: {
    isDark() {
      return this.$vuetify.theme.global.name === 'dark'
    },
  },
  data() {
    return {
      isDragging: false,
      isUploading: false,
    }
  },
  methods: {
    getDocumentUrl(path) {
      return getFileUrl(path)
    },
    getHeaderColor(type) {
      const colors = {
        Car: 'blue-darken-2',
        Home: 'brown-darken-1',
        Buildings: 'blue-grey-darken-2',
        Contents: 'amber-darken-3',
        Medical: 'teal-darken-2',
        Pet: 'green-darken-2',
      }
      return colors[type] || 'grey-darken-2'
    },
    getRenewalColor(dateStr) {
      if (!dateStr) return 'text-grey'
      const daysLeft = (new Date(dateStr) - new Date()) / (1000 * 60 * 60 * 24)
      if (daysLeft < 0) return 'text-red font-weight-bold'
      if (daysLeft < 30) return 'text-orange font-weight-bold'
      return 'text-success'
    },
    getIcon(type) {
      const icons = {
        Car: 'mdi-car',
        Buildings: 'mdi-home-city',
        Contents: 'mdi-sofa',
        Medical: 'mdi-medical-bag',
        Pet: 'mdi-paw',
      }
      return icons[type] || 'mdi-file-certificate'
    },
    isActive(endDate) {
      if (!endDate) return true
      return new Date(endDate) >= new Date()
    },
    formatDate(date) {
      if (!date) return 'Perpetual'
      return new Date(date).toLocaleDateString()
    },
    formatCurrency(val) {
      if (val === null || val === undefined) return '-'
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: this.currencyCode,
      }).format(val)
    },
    displayableAttributes(attrs) {
      if (!attrs) return {}
      return Object.fromEntries(
        Object.entries(attrs).filter(([_, v]) => typeof v !== 'object' && v !== null),
      )
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
    async uploadDocument(file) {
      this.isUploading = true
      let formData = new FormData()
      formData.append('file', file)

      try {
        const res = await api.put(`/policies/${this.policy.id}/document`, formData)
        this.policy.document_path = res.data.document_path
        const index = this.policies.findIndex((p) => p.id === this.policy.id)
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
