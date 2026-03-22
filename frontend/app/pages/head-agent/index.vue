<template>
  <div>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon blue">🏠</div>
        <div><div class="stat-value">{{ stats.total_properties }}</div><div class="stat-label">Total Properties</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">✅</div>
        <div><div class="stat-value">{{ stats.active_properties }}</div><div class="stat-label">Active Listings</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon yellow">👥</div>
        <div><div class="stat-value">{{ stats.sub_agents }}</div><div class="stat-label">Sub-Agents</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange">📅</div>
        <div><div class="stat-value">{{ stats.total_appointments }}</div><div class="stat-label">Total Appointments</div></div>
      </div>
    </div>

    <div class="cards-row mt">
      <div class="card">
        <h3>Quick Actions</h3>
        <div class="action-list">
          <NuxtLink to="/head-agent/properties" class="action-item">🏠 Manage Inventory</NuxtLink>
          <NuxtLink to="/head-agent/team" class="action-item">👥 Manage Team</NuxtLink>
          <NuxtLink to="/head-agent/schedule" class="action-item">📅 View All Appointments</NuxtLink>
          <NuxtLink to="/head-agent/analytics" class="action-item">📈 View Analytics</NuxtLink>
          <NuxtLink to="/head-agent/agency-profile" class="action-item">🏢 Agency Profile</NuxtLink>
        </div>
      </div>
      <div class="card">
        <h3>Pending Appointments</h3>
        <div v-if="pendingAppts.length > 0">
          <div v-for="a in pendingAppts" :key="a.id" class="appt-row">
            <div>
              <strong>{{ a.client?.full_name || '—' }}</strong>
              <span class="appt-prop">{{ a.property?.title }}</span>
            </div>
            <span class="badge pending">{{ formatDate(a.date_time) }}</span>
          </div>
        </div>
        <div v-else class="empty-state">No pending appointments</div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'head-agent' })
const stats = ref({ total_properties: 0, active_properties: 0, sub_agents: 0, total_appointments: 0 })
const pendingAppts = ref([])
const formatDate = (d) => new Date(d).toLocaleDateString('en-GB')

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  const h = { Authorization: `Bearer ${token}` }
  try {
    const [s, appts] = await Promise.all([
      $fetch('http://localhost:8000/analytics/platform'),
      $fetch('http://localhost:8000/appointments/', { headers: h })
    ])
    stats.value = s
    pendingAppts.value = appts.filter(a => a.status === 'pending').slice(0, 6)
  } catch(e) { console.error(e) }
})
</script>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.25rem; }
.stat-card { background: white; border-radius: 12px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.stat-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }
.stat-icon.blue { background: #dbeafe; }
.stat-icon.green { background: #dcfce7; }
.stat-icon.yellow { background: #fef9c3; }
.stat-icon.orange { background: #ffedd5; }
.stat-value { font-size: 1.6rem; font-weight: 800; color: #0f172a; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #64748b; margin-top: 0.2rem; }
.mt { margin-top: 2rem; }
.cards-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 1.25rem; font-size: 1rem; }
.action-list { display: flex; flex-direction: column; gap: 0.5rem; }
.action-item { display: block; text-decoration: none; padding: 0.65rem 1rem; border-radius: 8px; background: #f8fafc; color: #0f172a; font-size: 0.875rem; font-weight: 500; border: 1.5px solid #e2e8f0; transition: all 0.15s; }
.action-item:hover { background: #f1f5f9; border-color: #8b5cf6; color: #5b21b6; }
.appt-row { display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0; border-bottom: 1px solid #f1f5f9; font-size: 0.875rem; }
.appt-prop { display: block; color: #64748b; font-size: 0.78rem; }
.badge { padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
.badge.pending { background: #fef9c3; color: #713f12; }
.empty-state { text-align: center; color: #94a3b8; padding: 2rem; }
</style>
