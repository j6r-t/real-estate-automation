<template>
  <div>
    <div class="page-header"><h2>Agency Profile</h2></div>

    <div class="profile-grid">
      <!-- Status Card -->
      <div class="status-card" :class="agency.status">
        <div class="status-icon">
          {{ agency.status === 'verified' ? '✅' : agency.status === 'pending' ? '⏳' : '❌' }}
        </div>
        <div>
          <div class="status-title">{{ statusLabel }}</div>
          <div class="status-sub">{{ statusSub }}</div>
        </div>
        <div class="trust-score" v-if="agency.trust_score !== undefined">
          <div class="score-label">Trust Score</div>
          <div class="score-value">{{ agency.trust_score }}</div>
        </div>
      </div>

      <!-- Edit Form -->
      <div class="card">
        <h3>Agency Details</h3>
        <form @submit.prevent="saveAgency">
          <div class="form-group"><label>Agency Name</label><input v-model="form.name" required /></div>
          <div class="form-group"><label>Official Address</label><input v-model="form.address" /></div>
          <div class="form-group"><label>Trade License Number</label><input v-model="form.license_number" /></div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save Changes</button>
            <button type="button" v-if="!agency.id" @click="createAgency" class="btn btn-success">Register Agency</button>
          </div>
        </form>
        <p v-if="savedMsg" class="saved-msg">✅ Saved successfully</p>
      </div>
    </div>

    <!-- Rejection notice -->
    <div v-if="agency.status === 'rejected' && agency.rejection_reason" class="rejection-notice">
      <strong>❌ Rejection Reason:</strong> {{ agency.rejection_reason }}
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'head-agent' })
const agency = ref({})
const form = ref({ name: '', address: '', license_number: '' })
const savedMsg = ref(false)

const statusLabel = computed(() => ({ verified: 'Agency Verified', pending: 'Verification Pending', rejected: 'Verification Rejected' }[agency.value.status] || 'No Agency Created')
)
const statusSub = computed(() => ({ verified: 'Full publishing privileges active', pending: 'Under review by admin', rejected: 'See rejection reason below' }[agency.value.status] || 'Register your agency to get started')
)

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  try {
    const me = await $fetch('http://localhost:8000/users/me', { headers: { Authorization: `Bearer ${token}` } })
    const agencies = await $fetch('http://localhost:8000/agencies/')
    const mine = agencies.find(a => a.head_agent_id === me.id)
    if (mine) { agency.value = mine; form.value = { name: mine.name, address: mine.address, license_number: mine.license_number } }
  } catch(e) {}
})

const saveAgency = async () => {
  const token = localStorage.getItem('auth_token')
  if (agency.value.id) {
    const updated = await $fetch(`http://localhost:8000/agencies/${agency.value.id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify(form.value)
    })
    agency.value = updated
  }
  savedMsg.value = true
  setTimeout(() => savedMsg.value = false, 2500)
}

const createAgency = async () => {
  const token = localStorage.getItem('auth_token')
  const newAgency = await $fetch('http://localhost:8000/agencies/', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(form.value)
  })
  agency.value = newAgency
}
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h2 { margin: 0; }
.profile-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 1.5rem; }
.status-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); display: flex; flex-direction: column; align-items: center; text-align: center; gap: 1rem; border-top: 4px solid #e2e8f0; }
.status-card.verified { border-top-color: #16a34a; }
.status-card.pending { border-top-color: #d97706; }
.status-card.rejected { border-top-color: #dc2626; }
.status-icon { font-size: 2.5rem; }
.status-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
.status-sub { font-size: 0.8rem; color: #64748b; margin-top: 0.25rem; }
.trust-score { margin-top: 1rem; }
.score-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; font-weight: 600; }
.score-value { font-size: 2rem; font-weight: 800; color: #16a34a; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 1.5rem; }
.form-group { margin-bottom: 1.25rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; }
.form-group input { width: 100%; padding: 0.75rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-family: inherit; box-sizing: border-box; }
.form-group input:focus { outline: none; border-color: #8b5cf6; }
.form-actions { display: flex; gap: 0.75rem; }
.btn-success { background: #16a34a; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer; }
.saved-msg { margin-top: 1rem; color: #16a34a; font-size: 0.875rem; font-weight: 600; }
.rejection-notice { margin-top: 1.5rem; background: #fee2e2; border: 1.5px solid #fecaca; border-radius: 10px; padding: 1rem 1.25rem; color: #991b1b; font-size: 0.875rem; }
</style>
