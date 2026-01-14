<template>
  <v-app>
    <v-app-bar color="primary" elevation="2">
      <v-app-bar-title>
        <v-icon icon="mdi-shield-check" class="mr-2"></v-icon>
        PolicyNest 
        <span v-if="currentHousehold" class="text-subtitle-1 ml-2 text-white">
           | {{ currentHousehold.name }}
        </span>
      </v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container>
        
        <div v-if="initialized">
          <v-row class="mb-4" align="center">
            <v-col>
              <h2 class="text-h4">Overview</h2>
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
              </template>
            </v-data-table>
          </v-card>
        </div>

        <div v-else-if="checkingStatus" class="d-flex justify-center align-center" style="height: 80vh">
           <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </div>

      </v-container>
    </v-main>

    <v-dialog v-model="showOnboarding" persistent max-width="500px">
      <v-card class="text-center pa-4">
        <v-icon icon="mdi-home-heart" size="64" color="primary" class="mb-4"></v-icon>
        <v-card-title class="text-h5">Welcome Home</v-card-title>
        <v-card-text>
          <p class="mb-4">It looks like this is your first time here. Let's create a household to store your documents.</p>
          <v-text-field 
            v-model="householdName" 
            label="Household Name" 
            placeholder="e.g. The Smith Residence"
            variant="outlined"
            @keyup.enter="createHousehold"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn block color="primary" size="large" variant="flat" @click="createHousehold" :loading="creatingHousehold">
            Create Household
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog" max-width="600px">
       <v-card>
            <v-card-title>
              <span class="text-h5">New Policy</span>
            </v-card-title>
            <v-card-text>
              <v-form ref="form" @submit.prevent="submitPolicy">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="form.provider" label="Provider" variant="outlined" required></v-text-field>
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

  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // App State
      checkingStatus: true,
      initialized: false,
      showOnboarding: false,
      currentHousehold: null,

      // Onboarding State
      householdName: '',
      creatingHousehold: false,

      // Dashboard State
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
        provider: '', type: null, start_date: '', end_date: '', premium: '',
      },
      file: null
    };
  },
  methods: {
    async checkSystemStatus() {
      try {
        const res = await axios.get('http://localhost:8000/system/status');
        if (res.data.initialized) {
          this.initialized = true;
          this.currentHousehold = res.data.household;
          this.fetchPolicies();
        } else {
          this.showOnboarding = true;
        }
      } catch (e) {
        console.error("Connection error", e);
      } finally {
        this.checkingStatus = false;
      }
    },
    async createHousehold() {
      if (!this.householdName) return;
      this.creatingHousehold = true;
      try {
        let formData = new FormData();
        formData.append('name', this.householdName);
        const res = await axios.post('http://localhost:8000/households/', formData);
        
        this.currentHousehold = res.data;
        this.initialized = true;
        this.showOnboarding = false;
        this.fetchPolicies(); // Load empty table
      } catch(e) {
        console.error(e);
      } finally {
        this.creatingHousehold = false;
      }
    },
    async fetchPolicies() {
      if (!this.currentHousehold) return;
      this.loading = true;
      try {
        // Fetch policies only for this household
        const res = await axios.get(`http://localhost:8000/policies/?household_id=${this.currentHousehold.id}`);
        this.policies = res.data;
      } catch (e) {
        console.error(e);
      } finally {
        this.loading = false;
      }
    },
    async submitPolicy() {
        if (!this.form.provider || !this.form.premium) return; 

        this.submitting = true;
        let formData = new FormData();
        // IMPORTANT: Attach the household ID
        formData.append('household_id', this.currentHousehold.id); 
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
            this.form = { provider: '', type: null, start_date: '', end_date: '', premium: '' };
            this.file = null;
        } catch (e) {
            console.error("Error upload", e);
        } finally {
            this.submitting = false;
        }
    },
    handleFileUpload(event) {
        this.file = event.target.files[0];
    },
    getTypeColor(type) {
      const colors = { 'Car': 'blue', 'Home': 'orange', 'Life': 'green', 'Medical': 'red', 'Pet': 'purple' };
      return colors[type] || 'grey';
    },
    getDocumentUrl(path) {
      if (!path) return '#';
      const filename = path.split('/').pop();
      return `http://localhost:8000/uploads/${filename}`;
    }
  },
  mounted() {
    this.checkSystemStatus();
  }
};
</script>