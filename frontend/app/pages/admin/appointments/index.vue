<template>
  <div class="admin-page">
    <header class="page-header">
      <h2>Appointments</h2>
      <div class="actions">
        <button class="btn btn-primary" @click="fetchAppointments">Refresh</button>
      </div>
    </header>

    <div class="filter-bar">
      <select v-model="filter" class="filter-select">
        <option value="all">All Statuses</option>
        <option value="pending">Pending</option>
        <option value="confirmed">Confirmed</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

    <div v-if="loading" class="loading-state">Loading appointments...</div>

    <div v-else class="upcoming-list">
      <div v-if="filteredAppointments.length === 0" class="empty-state">
        No {{ filter !== 'all' ? filter : '' }} appointments found.
      </div>

      <div class="appointment-card" v-for="appt in filteredAppointments" :key="appt.id" :class="appt.status">
        <div class="time-block">
          <span class="day">{{ getDay(appt.date_time) }}</span>
          <span class="month">{{ getMonth(appt.date_time) }}</span>
        </div>
        <div class="details">
          <h4>{{ appt.property?.title || 'Unknown Property' }}</h4>
          <div class="meta-row">
            <span class="client-info">👤 {{ appt.client?.full_name || 'Client' }} ({{ appt.client?.phone || appt.client?.email }})</span>
            <span class="agent-info" v-if="appt.agent">👔 Agent: {{ appt.agent.full_name }}</span>
          </div>
          <p class="time">⏰ {{ formatTime(appt.date_time) }}</p>
          <div class="notes" v-if="appt.notes">
            <small>📝 {{ appt.notes }}</small>
          </div>
        </div>
        
        <div class="status-badge-container">
          <span :class="['status-badge', appt.status]">{{ appt.status }}</span>
        </div>

        <div class="actions">
          <button class="btn btn-outline" @click="viewDetails(appt.id)">Details</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const appointments = ref([])
const loading = ref(true)
const filter = ref('all')

const filteredAppointments = computed(() => {
  if (filter.value === 'all') return appointments.value
  return appointments.value.filter(a => a.status === filter.value)
})

const getDay = (d) => new Date(d).getDate()
const getMonth = (d) => new Date(d).toLocaleString('default', { month: 'short' }).toUpperCase()
const formatTime = (d) => new Date(d).toLocaleString('en-GB', { hour: '2-digit', minute: '2-digit' })

const fetchAppointments = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('auth_token')
    appointments.value = await $fetch('http://localhost:8000/appointments/', {
      headers: { Authorization: `Bearer ${token}` }
    })
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const viewDetails = (id) => {
  // Logic to view details or open modal (placeholder for now, serves as basic interaction)
  // In a real app, might route to /admin/appointments/[id]
  alert(`Viewing details for appointment #${id}`)
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style scoped>
.admin-page { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.page-header h2 { margin: 0; color: #0f172a; }

.filter-bar { margin-bottom: 1.5rem; }
.filter-select { padding: 0.5rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 0.95rem; }

.upcoming-list { display: flex; flex-direction: column; gap: 1rem; }

.appointment-card {
  background: white; padding: 1.25rem; border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  display: flex; align-items: center; gap: 1.5rem; border: 1px solid #e2e8f0;
  transition: transform 0.2s;
}
.appointment-card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }

.appointment-card.pending { border-left: 4px solid #f59e0b; }
.appointment-card.confirmed { border-left: 4px solid #10b981; }
.appointment-card.completed { border-left: 4px solid #3b82f6; }
.appointment-card.cancelled { border-left: 4px solid #ef4444; }

.time-block { text-align: center; background-color: #f8fafc; padding: 0.75rem 1.25rem; border-radius: 8px; min-width: 70px; }
.day { display: block; font-size: 1.75rem; font-weight: 800; color: #0f172a; line-height: 1; }
.month { font-size: 0.85rem; color: #64748b; font-weight: 700; text-transform: uppercase; }

.details { flex: 1; }
.details h4 { margin: 0 0 0.5rem; color: #0f172a; font-size: 1.1rem; }
.meta-row { display: flex; gap: 1rem; margin-bottom: 0.5rem; flex-wrap: wrap; }
.client-info, .agent-info { font-size: 0.9rem; color: #475569; font-weight: 500; }
.time { margin: 0; font-size: 0.95rem; color: #64748b; font-weight: 600; }
.notes { margin-top: 0.5rem; color: #94a3b8; font-style: italic; }

.status-badge { padding: 0.35rem 0.85rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
.status-badge.pending { background: #fef3c7; color: #92400e; }
.status-badge.confirmed { background: #d1fae5; color: #065f46; }
.status-badge.completed { background: #dbeafe; color: #1e40af; }
.status-badge.cancelled { background: #fee2e2; color: #991b1b; }

.actions { display: flex; gap: 0.75rem; }

/* Fixing button size as requested */
.btn {
  padding: 0.6rem 1.2rem; /* Increased padding */
  font-size: 0.95rem;     /* Increased font size */
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
}
.btn-primary { background: #0f172a; color: white; }
.btn-primary:hover { background: #1e293b; }
.btn-outline { background: white; border: 1.5px solid #e2e8f0; color: #475569; }
.btn-outline:hover { border-color: #94a3b8; color: #0f172a; }

.empty-state, .loading-state { text-align: center; padding: 4rem; color: #94a3b8; background: white; border-radius: 12px; }
</style>
