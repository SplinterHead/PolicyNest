<template>
  <v-card elevation="2" rounded="lg">
    <v-data-table :headers="headers" :items="policies" :loading="loading" hover>
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
      <template v-slot:item.premium="{ item }">
        <strong>${{ item.premium.toFixed(2) }}</strong>
      </template>
      <template v-slot:item.document_path="{ item }">
        <v-btn
          v-if="item.document_path"
          size="small"
          variant="tonal"
          color="primary"
          prepend-icon="mdi-file-pdf-box"
          :href="getDocumentUrl(item.document_path)"
          target="_blank"
        >
          View
        </v-btn>
        <span v-else class="text-caption text-grey">No Doc</span>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  props: {
    policies: Array,
    loading: Boolean,
  },
  data() {
    return {
      headers: [
        { title: 'Provider', key: 'provider', align: 'start' },
        { title: 'Type', key: 'type' },
        { title: 'Start Date', key: 'start_date' },
        { title: 'End Date', key: 'end_date' },
        { title: 'Premium', key: 'premium' },
        { title: 'Document', key: 'document_path', sortable: false },
      ],
    }
  },
  methods: {
    getTypeColor(type) {
      const colors = { Car: 'blue', Home: 'orange', Life: 'green', Medical: 'red', Pet: 'purple' }
      return colors[type] || 'grey'
    },
    getDocumentUrl(path) {
      if (!path) return '#'
      const filename = path.split('/').pop()
      return `http://localhost:8000/uploads/${filename}`
    },
  },
}
</script>
