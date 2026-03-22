<template>
  <div>
    <div class="page-header">
      <h1>Appointments</h1>
      <div class="filters">
        <select v-model="filterStatus">
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="cancelled">Cancelled</option>
          <option value="completed">Completed</option>
        </select>
      </div>
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Client</th>
            <th>Phone</th>
            <th>Property</th>
            <th>Date & Time</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appt in filtered" :key="appt.id">
            <td>
              <strong>{{ appt.client?.full_name || 'N/A' }}</strong><br>
              <small>{{ appt.client?.email }}</small>
            </td>
            <td>{{ appt.client?.phone || '—' }}</td>
            <td>{{ appt.property?.title || 'N/A' }}</td>
            <td>{{ formatDate(appt.date_time) }}</td>
            <td><span :class="['badge', appt.status]">{{ appt.status }}</span></td>
            <td class="actions">
              <button v-if="['confirmed', 'pending'].includes(appt.status) && new Date(appt.date_time) < new Date()" @click="openFeedback(appt)" class="btn-icon" title="Add Feedback">💬</button>
              <button @click="openEdit(appt)" class="btn-icon" title="Edit">✏️</button>
            </td>
          </tr>
          <tr v-if="filtered.length === 0">
            <td colspan="6" class="empty">No appointments found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Feedback Modal -->
    <div v-if="feedbackAppt" class="modal-overlay" @click.self="feedbackAppt = null">
      <div class="modal">
        <h3>Visit Feedback</h3>
        <p class="modal-subtitle">For appointment at <strong>{{ feedbackAppt.property?.title }}</strong></p>

        <div class="form-group">
          <label>Outcome</label>
          <div class="outcome-buttons">
            <button type="button" :class="['btn-outcome', { selected: feedbackForm.feedback_status === 'completed' }]" @click="feedbackForm.feedback_status = 'completed'">✅ Completed</button>
            <button type="button" :class="['btn-outcome', { selected: feedbackForm.feedback_status === 'no_show' }]" @click="feedbackForm.feedback_status = 'no_show'">❌ No Show</button>
          </div>
        </div>

        <div class="form-group">
          <label>Feedback Notes</label>
          <textarea v-model="feedbackForm.feedback_notes" rows="4" placeholder="How did the visit go? Is the client interested?"></textarea>
        </div>

        <div class="modal-actions">
          <button @click="feedbackAppt = null" class="btn btn-secondary">Cancel</button>
          <button @click="submitFeedback" class="btn btn-primary" :disabled="saving || !feedbackForm.feedback_status">Submit Feedback</button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingAppt" class="modal-overlay" @click.self="editingAppt = null">
      <div class="modal">
        <h3>Update Appointment</h3>

        <div class="info-block">
          <p><strong>Client:</strong> {{ editingAppt.client?.full_name }} ({{ editingAppt.client?.email }})</p>
          <p><strong>Property:</strong> {{ editingAppt.property?.title }}</p>
          <p><strong>Scheduled:</strong> {{ formatDate(editingAppt.date_time) }}</p>
        </div>

        <div class="form-group">
          <label>New Date & Time (leave blank to keep)</label>
          <input type="datetime-local" v-model="editForm.date_time" />
        </div>

        <div class="form-group">
          <label>Status</label>
          <select v-model="editForm.status">
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="cancelled">Cancelled</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div class="form-group">
          <label>Agent Notes (visible to team only)</label>
          <textarea v-model="editForm.agent_notes" rows="3" placeholder="Internal notes..."></textarea>
        </div>

        <div class="notice" v-if="editForm.status !== editingAppt.status">
          📧 Client will be notified by email about this status change.
        </div>

        <div class="modal-actions">
          <button @click="editingAppt = null" class="btn btn-secondary">Cancel</button>
          <button @click="saveEdit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save & Notify Client' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'agent' })
const auth = useAuthStore()
const appointments = ref([])
const filterStatus = ref('')
const editingAppt = ref(null)
const feedbackAppt = ref(null)
const saving = ref(false)

const editForm = ref({ status: '', agent_notes: '', date_time: '' })
const feedbackForm = ref({ feedback_status: '', feedback_notes: '' })

const filtered = computed(() =>
  filterStatus.value
    ? appointments.value.filter(a => a.status === filterStatus.value)
    : appointments.value
)

const formatDate = (dt) => new Date(dt).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' })

const fetchAppointments = async () => {
  const token = localStorage.getItem('auth_token')
  if (!token) return
  appointments.value = await $fetch('http://localhost:8000/appointments/', {
    headers: { Authorization: `Bearer ${token}` }
  })
}

const openEdit = (appt) => {
  editingAppt.value = appt
  editForm.value = {
    status: appt.status,
    agent_notes: appt.agent_notes || '',
    date_time: ''
  }
}

const openFeedback = (appt) => {
  feedbackAppt.value = appt
  feedbackForm.value = { feedback_status: '', feedback_notes: '' }
}

const submitFeedback = async () => {
  saving.value = true
  try {
    const token = localStorage.getItem('auth_token')
    await $fetch(`http://localhost:8000/appointments/${feedbackAppt.value.id}/feedback`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(feedbackForm.value)
    })
    feedbackAppt.value = null
    await fetchAppointments()
  } catch(e) { alert('Failed to submit feedback') }
  finally { saving.value = false }
}

const saveEdit = async () => {
  saving.value = true
  try {
    const token = localStorage.getItem('auth_token')
    const payload = { status: editForm.value.status, agent_notes: editForm.value.agent_notes }
    if (editForm.value.date_time) payload.date_time = editForm.value.date_time

    await $fetch(`http://localhost:8000/appointments/${editingAppt.value.id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    editingAppt.value = null
    await fetchAppointments()
  } catch (e) {
    alert('Failed to update appointment')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  auth.initAuth()
  fetchAppointments()
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.page-header h1 { font-size: 1.75rem; color: var(--primary-color); margin: 0; }

.filters select {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-family: var(--font-body);
  color: #334155;
}

.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }

.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 0.875rem 1rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.table th { font-size: 0.8rem; font-weight: 600; color: #64748b; text-transform: uppercase; }
.table td small { color: #94a3b8; font-size: 0.8rem; }

.badge { padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: capitalize; }
.badge.pending   { background: #fef3c7; color: #92400e; }
.badge.confirmed { background: #d1fae5; color: #065f46; }
.badge.cancelled { background: #fee2e2; color: #991b1b; }
.badge.completed { background: #dbeafe; color: #1e40af; }

.actions { display: flex; gap: 0.5rem; }
.btn-icon { background: none; border: none; cursor: pointer; font-size: 1.1rem; padding: 0.25rem; border-radius: 4px; }
.btn-icon:hover { background: #f1f5f9; }
.empty { text-align: center; color: #94a3b8; padding: 2rem; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 16px; width: 90%; max-width: 520px; }
.modal h3 { margin: 0 0 0.5rem; color: var(--primary-color); font-size: 1.25rem; }
.modal-subtitle { color: #64748b; font-size: 0.9rem; margin: 0 0 1.5rem; }

.info-block { background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1.25rem; }
.info-block p { margin: 0.25rem 0; font-size: 0.9rem; color: #334155; }

.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.4rem; color: #374151; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 0.65rem 0.875rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 0.9rem;
  box-sizing: border-box;
}

.outcome-buttons { display: flex; gap: 1rem; }
.btn-outcome { flex: 1; padding: 0.75rem; border: 1.5px solid #e2e8f0; background: white; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-outcome:hover { border-color: var(--primary-color); }
.btn-outcome.selected { background: #eff6ff; border-color: #2563eb; color: #1e40af; }

.notice { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.875rem; margin-bottom: 1rem; }

.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.25rem; }
</style>
