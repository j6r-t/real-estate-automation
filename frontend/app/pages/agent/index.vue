<template>
  <div>
    <!-- Stats Row -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon green">🏠</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.assigned_properties }}</div>
          <div class="stat-label">My Properties</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon blue">📅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_appointments }}</div>
          <div class="stat-label">Total Appointments</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon yellow">⏳</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.pending }}</div>
          <div class="stat-label">Pending</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange">🎯</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.leads }}</div>
          <div class="stat-label">Active Leads</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon purple">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.attendance_rate }}%</div>
          <div class="stat-label">Attendance Rate</div>
        </div>
      </div>
    </div>

    <!-- Upcoming Appointments -->
    <div class="card mt">
      <div class="card-header-row">
        <h3>Upcoming Appointments</h3>
        <NuxtLink to="/agent/appointments" class="link-btn">View All →</NuxtLink>
      </div>
      <table class="data-table" v-if="upcoming.length > 0">
        <thead>
          <tr>
            <th>Client</th>
            <th>Property</th>
            <th>Date & Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appt in upcoming" :key="appt.id">
            <td><strong>{{ appt.client?.full_name || '—' }}</strong><br><small>{{ appt.client?.phone || appt.client?.email }}</small></td>
            <td>{{ appt.property?.title || '—' }}</td>
            <td>{{ formatDate(appt.date_time) }}</td>
            <td><span :class="['badge', appt.status]">{{ appt.status }}</span></td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">No upcoming appointments</div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'agent' })
const auth = useAuthStore()
onMounted(() => auth.initAuth())

const stats = ref({ assigned_properties: 0, total_appointments: 0, pending: 0, leads: 0, attendance_rate: 0 })
const upcoming = ref([])

const formatDate = (dt) => new Date(dt).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' })

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  const headers = token ? { Authorization: `Bearer ${token}` } : {}
  try {
    const me = await $fetch('http://localhost:8000/users/me', { headers })
    const [s, appts] = await Promise.all([
      $fetch(`http://localhost:8000/analytics/agent/${me.id}`),
      $fetch('http://localhost:8000/appointments/', { headers })
    ])
    stats.value = s
    upcoming.value = appts.filter(a => a.status !== 'cancelled' && a.status !== 'completed').slice(0, 8)
  } catch(e) { console.error(e) }
})
</script>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1.25rem; }
.stat-card { background: white; border-radius: 12px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.stat-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }
.stat-icon.green { background: #dcfce7; }
.stat-icon.blue { background: #dbeafe; }
.stat-icon.yellow { background: #fef9c3; }
.stat-icon.orange { background: #ffedd5; }
.stat-icon.purple { background: #ede9fe; }
.stat-value { font-size: 1.6rem; font-weight: 800; color: #0f172a; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #64748b; margin-top: 0.2rem; }
.mt { margin-top: 2rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.card-header-row h3 { margin: 0; font-size: 1rem; }
.link-btn { color: var(--accent-color, #c9a84c); font-size: 0.85rem; font-weight: 600; text-decoration: none; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid #f1f5f9; font-size: 0.875rem; }
.data-table th { color: #64748b; font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
.badge { padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: capitalize; }
.badge.pending { background: #fef9c3; color: #713f12; }
.badge.confirmed { background: #dcfce7; color: #166534; }
.badge.cancelled { background: #fee2e2; color: #991b1b; }
.badge.completed { background: #dbeafe; color: #1e40af; }
.empty-state { text-align: center; color: #94a3b8; padding: 3rem; }
small { color: #94a3b8; font-size: 0.75rem; }
</style>
