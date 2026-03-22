<template>
  <div>
    <div class="page-header">
      <h2>Agency Verification</h2>
      <div class="filter-tabs">
        <button v-for="s in ['all','pending','verified','rejected']" :key="s" :class="['tab', { active: filter === s }]" @click="filter = s">{{ s }}</button>
      </div>
    </div>

    <div class="agencies-grid">
      <div class="agency-card" v-for="a in filtered" :key="a.id" :class="a.status">
        <div class="agency-header">
          <div>
            <h3>{{ a.name }}</h3>
            <p>{{ a.address || 'No address provided' }}</p>
          </div>
          <span :class="['status-badge', a.status]">{{ a.status }}</span>
        </div>

        <div class="agency-details">
          <div class="detail-item"><span class="detail-label">License</span><span>{{ a.license_number || '—' }}</span></div>
          <div class="detail-item"><span class="detail-label">Trust Score</span><span class="trust">{{ a.trust_score }}</span></div>
          <div class="detail-item"><span class="detail-label">Registered</span><span>{{ formatDate(a.created_at) }}</span></div>
        </div>

        <div v-if="a.status === 'pending'" class="agency-actions">
          <button @click="verify(a.id, 'verified')" class="btn btn-success btn-sm">✅ Verify</button>
          <button @click="openReject(a)" class="btn btn-danger btn-sm">❌ Reject</button>
        </div>
        <div v-else-if="a.status === 'verified'" class="agency-actions">
          <button @click="verify(a.id, 'rejected')" class="btn btn-outline btn-sm">Revoke</button>
        </div>
        <div v-if="a.rejection_reason" class="rejection-note">
          <strong>Reason:</strong> {{ a.rejection_reason }}
        </div>
      </div>
    </div>

    <div v-if="filtered.length === 0" class="empty-state">No {{ filter === 'all' ? '' : filter }} agencies found</div>

    <!-- Reject Modal -->
    <div v-if="rejectModal" class="modal-overlay" @click.self="rejectModal = false">
      <div class="modal">
        <h3>Reject Agency</h3>
        <p>Please provide a reason for rejecting <strong>{{ rejectingAgency?.name }}</strong>:</p>
        <div class="form-group">
          <textarea v-model="rejectReason" rows="4" placeholder="Explain why this agency is being rejected..."></textarea>
        </div>
        <div class="modal-actions">
          <button @click="rejectModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="doReject" class="btn btn-danger">Confirm Reject</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })
const agencies = ref([])
const filter = ref('all')
const rejectModal = ref(false)
const rejectingAgency = ref(null)
const rejectReason = ref('')

const filtered = computed(() => filter.value === 'all' ? agencies.value : agencies.value.filter(a => a.status === filter.value))
const formatDate = (d) => new Date(d).toLocaleDateString('en-GB')

const fetchAgencies = async () => {
  agencies.value = await $fetch('http://localhost:8000/agencies/')
}

const verify = async (id, status) => {
  await $fetch(`http://localhost:8000/agencies/${id}/verify`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  })
  fetchAgencies()
}

const openReject = (a) => { rejectingAgency.value = a; rejectReason.value = ''; rejectModal.value = true }

const doReject = async () => {
  await $fetch(`http://localhost:8000/agencies/${rejectingAgency.value.id}/verify`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'rejected', reason: rejectReason.value })
  })
  rejectModal.value = false
  fetchAgencies()
}

onMounted(fetchAgencies)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; }
.page-header h2 { margin: 0; }
.filter-tabs { display: flex; gap: 0.5rem; }
.tab { padding: 0.4rem 1rem; border-radius: 20px; border: 1.5px solid #e2e8f0; background: white; cursor: pointer; font-size: 0.8rem; font-weight: 600; text-transform: capitalize; }
.tab.active { background: #0f172a; color: white; border-color: #0f172a; }
.agencies-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.25rem; }
.agency-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid #e2e8f0; }
.agency-card.verified { border-left-color: #16a34a; }
.agency-card.pending { border-left-color: #d97706; }
.agency-card.rejected { border-left-color: #dc2626; }
.agency-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
.agency-header h3 { margin: 0 0 0.25rem; font-size: 1rem; }
.agency-header p { margin: 0; font-size: 0.8rem; color: #64748b; }
.status-badge { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: capitalize; flex-shrink: 0; }
.status-badge.verified { background: #dcfce7; color: #166534; }
.status-badge.pending { background: #fef9c3; color: #713f12; }
.status-badge.rejected { background: #fee2e2; color: #991b1b; }
.agency-details { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.25rem; padding: 1rem; background: #f8fafc; border-radius: 8px; }
.detail-item { text-align: center; }
.detail-label { display: block; font-size: 0.68rem; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 0.25rem; }
.trust { font-weight: 700; color: #16a34a; }
.agency-actions { display: flex; gap: 0.75rem; }
.btn-sm { padding: 0.45rem 1rem; font-size: 0.825rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: none; }
.btn-success { background: #dcfce7; color: #166534; }
.btn-success:hover { background: #bbf7d0; }
.btn-danger { background: #fee2e2; color: #dc2626; }
.btn-danger:hover { background: #fecaca; }
.btn-outline { background: white; border: 1.5px solid #e2e8f0; color: #64748b; }
.rejection-note { margin-top: 0.75rem; padding: 0.65rem 0.85rem; background: #fff7ed; border-radius: 8px; font-size: 0.8rem; color: #92400e; }
.empty-state { text-align: center; color: #94a3b8; padding: 4rem; background: white; border-radius: 12px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 90%; max-width: 460px; }
.modal h3 { margin: 0 0 0.75rem; }
.modal p { font-size: 0.875rem; color: #475569; margin: 0 0 1.25rem; }
.form-group textarea { width: 100%; padding: 0.75rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-family: inherit; box-sizing: border-box; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>
