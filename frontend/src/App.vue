<template>
  <div class="container">
    <h1>Insurance Tracker</h1>

    <div class="card">
      <h2>Add New Policy</h2>
      <form @submit.prevent="submitPolicy">
        <input v-model="form.provider" placeholder="Provider (e.g. Geico)" required />
        <select v-model="form.type" required>
          <option disabled value="">Select Type</option>
          <option>Car</option>
          <option>Home</option>
          <option>Life</option>
          <option>Medical</option>
        </select>
        <div class="date-group">
          <label>Start: <input type="date" v-model="form.start_date" required /></label>
          <label>End: <input type="date" v-model="form.end_date" required /></label>
        </div>
        <input
          type="number"
          step="0.01"
          v-model="form.premium"
          placeholder="Premium Cost"
          required
        />
        <input type="file" @change="handleFileUpload" />
        <button type="submit">Save Policy</button>
      </form>
    </div>

    <div class="card">
      <h2>Your Policies</h2>
      <table>
        <thead>
          <tr>
            <th>Provider</th>
            <th>Type</th>
            <th>Dates</th>
            <th>Premium</th>
            <th>Doc</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="policy in policies" :key="policy.id">
            <td>{{ policy.provider }}</td>
            <td>{{ policy.type }}</td>
            <td>{{ policy.start_date }} to {{ policy.end_date }}</td>
            <td>${{ policy.premium }}</td>
            <td>
              <span v-if="policy.document_path">✅</span>
              <span v-else>❌</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      policies: [],
      form: {
        provider: '',
        type: '',
        start_date: '',
        end_date: '',
        premium: '',
      },
      file: null,
    }
  },
  methods: {
    async fetchPolicies() {
      const res = await axios.get('http://localhost:8000/policies/')
      this.policies = res.data
    },
    handleFileUpload(event) {
      this.file = event.target.files[0]
    },
    async submitPolicy() {
      let formData = new FormData()
      formData.append('provider', this.form.provider)
      formData.append('type', this.form.type)
      formData.append('start_date', this.form.start_date)
      formData.append('end_date', this.form.end_date)
      formData.append('premium', this.form.premium)
      if (this.file) {
        formData.append('file', this.file)
      }

      await axios.post('http://localhost:8000/policies/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      this.fetchPolicies()
      this.form = { provider: '', type: '', start_date: '', end_date: '', premium: '' }
      this.file = null
    },
  },
  mounted() {
    this.fetchPolicies()
  },
}
</script>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  font-family: sans-serif;
}
.card {
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
}
input,
select,
button {
  display: block;
  margin-bottom: 10px;
  width: 100%;
  padding: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  text-align: left;
  padding: 8px;
  border-bottom: 1px solid #ddd;
}
</style>
