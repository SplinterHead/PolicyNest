<template>
  <v-app>
    <v-app-bar color="primary" elevation="2">
      <v-app-bar-title>
        <v-icon icon="mdi-shield-check" class="mr-2"></v-icon>
        PolicyNest
      </v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container>
        
        <v-row class="mb-4" align="center">
          <v-col>
            <h2 class="text-h4">My Policies</h2>
          </v-col>
          <v-col cols="auto">
            <v-btn color="primary" prepend-icon="mdi-plus" @click="dialog = true">
              Add Policy
            </v-btn>
          </v-col>
        </v-row>

        <v-card elevation="2">
          <v-data-table
            :headers="headers"
            :items="policies"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.type="{ item }">
              <v-chip :color="getTypeColor(item.type)" size="small" variant="flat">
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
                variant="text"
                color="primary"
                prepend-icon="mdi-file-pdf-box"
                :href="getDocumentUrl(item.document_path)"
                target="_blank"
              >
                View PDF
              </v-btn>
              <span v-else class="text-caption text-grey">No Doc</span>
            </template>
          </v-data-table>
        </v-card>

        <v-dialog v-model="dialog" max-width="600px">
          <v-card>
            <v-card-title>
              <span class="text-h5">New Policy</span>
            </v-card-title>

            <v-card-text>
              <v-form ref="form" @submit.prevent="submitPolicy">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="form.provider" label="Provider (e.g. Geico)" variant="outlined" required></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-select 
                      v-model="form.type" 
                      :items="['Car', 'Home', 'Life', 'Medical', 'Pet']" 
                      label="Type" 
                      variant="outlined"
                      required
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field type="date" v-model="form.start_date" label="Start Date" variant="outlined" required></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field type="date" v-model="form.end_date" label="End Date" variant="outlined" required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field type="number" step="0.01" v-model="form.premium" label="Premium ($)" variant="outlined" prefix="$" required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-file-input 
                      @change="handleFileUpload" 
                      label="Upload Policy Document (PDF)" 
                      variant="outlined" 
                      prepend-icon="mdi-paperclip"
                      accept=".pdf"
                    ></v-file-input>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey-darken-1" variant="text" @click="dialog = false">Cancel</v-btn>
              <v-btn color="primary" variant="flat" @click="submitPolicy" :loading="submitting">Save Policy</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dialog: false,
      loading: false,
      submitting: false,
      policies: [],
      headers: [
        { title: 'Provider', key: 'provider', align: 'start' },
        { title: 'Type', key: 'type' },
        { title: 'Start Date', key: 'start_date' },
        { title: 'End Date', key: 'end_date' },
        { title: 'Premium', key: 'premium' },
        { title: 'Document', key: 'document_path', sortable: false },
      ],
      form: {
        provider: '',
        type: null,
        start_date: '',
        end_date: '',
        premium: '',
      },
      file: null
    };
  },
  methods: {
    async fetchPolicies() {
      this.loading = true;
      try {
        const res = await axios.get('http://localhost:8000/policies/');
        this.policies = res.data;
      } catch (e) {
        console.error(e);
      } finally {
        this.loading = false;
      }
    },
    handleFileUpload(event) {
      // Vuetify file input returns an array of files
      this.file = event.target.files[0];
    },
    async submitPolicy() {
      if (!this.form.provider || !this.form.premium) return; // Simple validation

      this.submitting = true;
      let formData = new FormData();
      formData.append('provider', this.form.provider);
      formData.append('type', this.form.type);
      formData.append('start_date', this.form.start_date);
      formData.append('end_date', this.form.end_date);
      formData.append('premium', this.form.premium);
      if (this.file) {
        formData.append('file', this.file);
      }

      try {
        await axios.post('http://localhost:8000/policies/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.fetchPolicies();
        this.dialog = false;
        // Reset form
        this.form = { provider: '', type: null, start_date: '', end_date: '', premium: '' };
        this.file = null;
      } catch (e) {
        console.error("Error upload", e);
      } finally {
        this.submitting = false;
      }
    },
    getTypeColor(type) {
      const colors = {
        'Car': 'blue',
        'Home': 'orange',
        'Life': 'green',
        'Medical': 'red',
        'Pet': 'purple'
      };
      return colors[type] || 'grey';
    },
    getDocumentUrl(path) {
      if (!path) return '#';
      const filename = path.split('/').pop();
      return `http://localhost:8000/uploads/${filename}`;
    }
  },
  mounted() {
    this.fetchPolicies();
  }
};
</script>