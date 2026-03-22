<template>
  <div>
    <div class="page-header"><h2>Agency Analytics</h2></div>

    <div class="stats-grid">
      <div class="metric-card" v-for="m in metrics" :key="m.label">
        <div class="metric-icon">{{ m.icon }}</div>
        <div class="metric-value" :style="{ color: m.color }">{{ m.value }}</div>
        <div class="metric-label">{{ m.label }}</div>
      </div>
    </div>

    <!-- Agent Leaderboard -->
    <div class="card mt">
      <h3>🏆 Agent Performance Leaderboard</h3>
      <table class="data-table" v-if="leaderboard.length > 0">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Agent</th>
            <th>Properties</th>
            <th>Total Visits</th>
            <th>Completed</th>
            <th>Attendance Rate</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(agent, index) in leaderboard" :key="agent.id">
            <td>
              <span class="rank" :class="['rank-' + (index+1)]">{{ index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index+1}` }}</span>
            </td>
            <td><strong>{{ agent.name }}</strong></td>
            <td>{{ agent.stats.assigned_properties }}</td>
            <td>{{ agent.stats.total_appointments }}</td>
            <td>{{ agent.stats.completed }}</td>
            <td>
              <div class="rate-bar">
                <div class="rate-fill" :style="{ width: agent.stats.attendance_rate + '%', background: rateColor(agent.stats.attendance_rate) }"></div>
                <span>{{ agent.stats.attendance_rate }}%</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">No agent data yet</div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'head-agent' })
const platform = ref({})
const leaderboard = ref([])

const metrics = computed(() => [
  { label: 'Total Properties', value: platform.value.total_properties || 0, icon: '🏠', color: '#2563eb' },
  { label: 'Active Listings', value: platform.value.active_properties || 0, icon: '✅', color: '#16a34a' },
  { label: 'Total Visits', value: platform.value.total_appointments || 0, icon: '📅', color: '#d97706' },
  { label: 'Total Leads', value: platform.value.total_leads || 0, icon: '🎯', color: '#8b5cf6' },
])

const rateColor = (rate) => rate >= 80 ? '#16a34a' : rate >= 50 ? '#d97706' : '#dc2626'

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  const [stats, users] = await Promise.all([
    $fetch('http://localhost:8000/analytics/platform'),
    $fetch('http://localhost:8000/users/')
  ])
  platform.value = stats
  const subAgents = users.filter(u => u.role === 'sub_agent')
  const results = await Promise.all(subAgents.map(async a => ({
    id: a.id, name: a.full_name,
    stats: await $fetch(`http://localhost:8000/analytics/agent/${a.id}`)
  })))
  leaderboard.value = results.sort((a, b) => b.stats.attendance_rate - a.stats.attendance_rate)
})
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h2 { margin: 0; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1.25rem; }
.metric-card { background: white; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.metric-icon { font-size: 1.75rem; margin-bottom: 0.5rem; }
.metric-value { font-size: 2rem; font-weight: 800; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #64748b; margin-top: 0.35rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
.mt { margin-top: 2rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 1.25rem; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid #f1f5f9; font-size: 0.875rem; }
.data-table th { color: #64748b; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; }
.rate-bar { display: flex; align-items: center; gap: 0.75rem; }
.rate-bar > div { flex: 1; height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden; }
.rate-fill { height: 100%; border-radius: 5px; transition: width 0.5s ease; }
.rate-bar > span { font-size: 0.8rem; font-weight: 700; min-width: 38px; }
.empty-state { text-align: center; color: #94a3b8; padding: 3rem; }
</style>
