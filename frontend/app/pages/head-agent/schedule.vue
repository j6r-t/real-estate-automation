<template>
  <div>
    <div class="page-header"><h2>Global Schedule</h2></div>

    <div class="filter-bar">
      <select v-model="agentFilter" class="filter-select">
        <option value="">All Agents</option>
        <option v-for="a in agents" :key="a.id" :value="a.id">{{ a.full_name }}</option>
      </select>
      <select v-model="statusFilter" class="filter-select">
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="confirmed">Confirmed</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

    <div class="card">
      <table class="data-table" v-if="filtered.length > 0">
        <thead>
          <tr>
            <th>Client</th>
            <th>Property</th>
            <th>Agent</th>
            <th>Date & Time</th>
            <th>Status</th>
            <th>Feedback</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appt in filtered" :key="appt.id">
            <td>
              <strong>{{ appt.client?.full_name || '—' }}</strong>
              <div class="sub-text">{{ appt.client?.phone || appt.client?.email }}</div>
            </td>
            <td>{{ appt.property?.title || '—' }}</td>
            <td>{{ appt.agent?.full_name || '— Unassigned' }}</td>
            <td>{{ formatDate(appt.date_time) }}</td>
            <td><span :class="['badge', appt.status]">{{ appt.status }}</span></td>
            <td><span v-if="appt.feedback_status" :class="['badge', appt.feedback_status]">{{ appt.feedback_status }}</span><span v-else class="sub-text">—</span></td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">No appointments found</div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'head-agent' })
const appointments = ref([])
const agents = ref([])
const agentFilter = ref('')
const statusFilter = ref('')

const filtered = computed(() => {
  let list = appointments.value
  if (agentFilter.value) list = list.filter(a => a.agent_id === Number(agentFilter.value))
  if (statusFilter.value) list = list.filter(a => a.status === statusFilter.value)
  return list
})

const formatDate = (d) => new Date(d).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' })

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  const h = { Authorization: `Bearer ${token}` }
  const [appts, users] = await Promise.all([
    $fetch('http://localhost:8000/appointments/', { headers: h }),
    $fetch('http://localhost:8000/users/')
  ])
  appointments.value = appts
  agents.value = users.filter(u => u.role === 'sub_agent')
})
</script>

<style scoped>
.page-header { margin-bottom: 1rem; }
.page-header h2 { margin: 0; }
.filter-bar { display: flex; gap: 1rem; margin-bottom: 1.25rem; }
.filter-select { padding: 0.5rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid #f1f5f9; font-size: 0.875rem; }
.data-table th { color: #64748b; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.badge { padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: capitalize; }
.badge.pending { background: #fef9c3; color: #713f12; }
.badge.confirmed { background: #dcfce7; color: #166534; }
.badge.completed { background: #dbeafe; color: #1e40af; }
.badge.cancelled { background: #fee2e2; color: #991b1b; }
.badge.no_show { background: #ede9fe; color: #5b21b6; }
.sub-text { font-size: 0.75rem; color: #94a3b8; }
.empty-state { text-align: center; color: #94a3b8; padding: 3rem; }
</style>
