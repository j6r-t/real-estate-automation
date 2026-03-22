<template>
  <div>
    <!-- Metric cards -->
    <div class="stats-grid">
      <div class="metric-card">
        <div class="metric-label">Visits Managed</div>
        <div class="metric-value">{{ stats.total_appointments }}</div>
      </div>
      <div class="metric-card highlight">
        <div class="metric-label">Completed Visits</div>
        <div class="metric-value green">{{ stats.completed }}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Client No-Shows</div>
        <div class="metric-value orange">{{ stats.no_shows }}</div>
      </div>
      <div class="metric-card highlight">
        <div class="metric-label">Attendance Rate</div>
        <div class="metric-value blue">{{ stats.attendance_rate }}%</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Active Leads</div>
        <div class="metric-value">{{ stats.leads }}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Assigned Properties</div>
        <div class="metric-value">{{ stats.assigned_properties }}</div>
      </div>
    </div>

    <!-- Attendance gauge -->
    <div class="card mt">
      <h3>Attendance Rate</h3>
      <div class="gauge-wrap">
        <div class="gauge-bar">
          <div class="gauge-fill" :style="{ width: stats.attendance_rate + '%', background: rateColor }"></div>
        </div>
        <span class="gauge-label" :style="{ color: rateColor }">{{ stats.attendance_rate }}%</span>
      </div>
      <p class="gauge-hint" v-if="stats.attendance_rate >= 80">🌟 Excellent attendance! Keep up the great work.</p>
      <p class="gauge-hint warn" v-else-if="stats.attendance_rate >= 50">⚡ Good performance — room to improve attendance rate.</p>
      <p class="gauge-hint danger" v-else>⚠️ Low attendance rate. Review your lead qualification process.</p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'agent' })
const stats = ref({ total_appointments: 0, completed: 0, no_shows: 0, attendance_rate: 0, leads: 0, assigned_properties: 0 })

const rateColor = computed(() => {
  if (stats.value.attendance_rate >= 80) return '#16a34a'
  if (stats.value.attendance_rate >= 50) return '#d97706'
  return '#dc2626'
})

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  try {
    const me = await $fetch('http://localhost:8000/users/me', { headers: { Authorization: `Bearer ${token}` } })
    stats.value = await $fetch(`http://localhost:8000/analytics/agent/${me.id}`)
  } catch(e) { console.error(e) }
})
</script>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1.25rem; }
.metric-card { background: white; border-radius: 12px; padding: 1.5rem 1.25rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); text-align: center; }
.metric-card.highlight { border-top: 3px solid var(--accent-color, #c9a84c); }
.metric-label { font-size: 0.78rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.metric-value { font-size: 2rem; font-weight: 800; color: #0f172a; line-height: 1; }
.metric-value.green { color: #16a34a; }
.metric-value.orange { color: #d97706; }
.metric-value.blue { color: #2563eb; }
.mt { margin-top: 2rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 1.25rem; }
.gauge-wrap { display: flex; align-items: center; gap: 1rem; }
.gauge-bar { flex: 1; height: 18px; background: #f1f5f9; border-radius: 9px; overflow: hidden; }
.gauge-fill { height: 100%; border-radius: 9px; transition: width 0.5s ease; }
.gauge-label { font-size: 1.2rem; font-weight: 800; min-width: 60px; text-align: right; }
.gauge-hint { margin-top: 1rem; font-size: 0.875rem; color: #475569; }
.gauge-hint.warn { color: #d97706; }
.gauge-hint.danger { color: #dc2626; }
</style>
