<template>
  <div class="dashboard">
    <div class="page-header">
      <h2>Dashboard Overview</h2>
      <NuxtLink to="/admin/properties" class="btn btn-primary">+ New Property</NuxtLink>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Active Listings</h3>
        <p class="number">{{ stats.totalProperties }}</p>
        <span class="trend neutral">Total properties</span>
      </div>
      <div class="stat-card">
        <h3>Total Users</h3>
        <p class="number">{{ stats.totalUsers }}</p>
        <span class="trend neutral">Registered users</span>
      </div>
      <div class="stat-card">
        <h3>Agents</h3>
        <p class="number">{{ stats.agentUsers }}</p>
        <span class="trend neutral">Agency staff</span>
      </div>
      <div class="stat-card">
        <h3>Clients</h3>
        <p class="number">{{ stats.clientUsers }}</p>
        <span class="trend neutral">Client accounts</span>
      </div>
    </div>

    <div class="recent-activity">
      <h3>Recent Properties</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Location</th>
            <th>Price (TND)</th>
            <th>Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="property in recentProperties" :key="property.id">
            <td>{{ property.title }}</td>
            <td>{{ property.location }}</td>
            <td>{{ property.price.toLocaleString() }}</td>
            <td><span class="status confirmed">{{ property.type }}</span></td>
            <td>
              <NuxtLink :to="`/properties/${property.id}`" class="btn btn-outline btn-sm">View</NuxtLink>
            </td>
          </tr>
          <tr v-if="recentProperties.length === 0">
            <td colspan="5" style="text-align: center; color: #94a3b8;">No properties yet</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const stats = ref({
  totalProperties: 0,
  totalUsers: 0,
  agentUsers: 0,
  clientUsers: 0
})

const recentProperties = ref([])

const fetchDashboardData = async () => {
  try {
    // Fetch properties
    const properties = await $fetch('http://localhost:8000/properties/')
    stats.value.totalProperties = properties.length
    recentProperties.value = properties.slice(0, 5) // Latest 5
    
    // Fetch users
    const users = await $fetch('http://localhost:8000/users/')
    stats.value.totalUsers = users.length
    stats.value.adminUsers = users.filter(u => u.role === 'admin').length
    stats.value.clientUsers = users.filter(u => u.role === 'client').length
  } catch (e) {
    console.error('Failed to fetch dashboard data', e)
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: calc(100vh - 60px);
}

.sidebar {
  width: 260px;
  background-color: var(--primary-color);
  color: white;
  padding: 1rem 0;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 0 1.5rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 1rem;
}

.sidebar-header h3 {
  color: white;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.7;
  font-weight: 600;
}

.nav-item {
  display: block;
  padding: 0.75rem 1.5rem;
  color: #94a3b8;
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s;
}

.nav-item:hover, .nav-item.active {
  background-color: rgba(255,255,255,0.05);
  color: white;
}

.nav-item.active {
  border-left-color: var(--accent-color);
}

.content {
  flex: 1;
  padding: 2rem;
  background-color: #f1f5f9;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.stat-card h3 {
  color: var(--text-light);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0 0 0.5rem;
}

.trend {
  font-size: 0.8rem;
}
.trend.up { color: green; }
.trend.down { color: red; }
.trend.neutral { color: #64748b; }

/* Table */
.recent-activity {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.data-table th, .data-table td {
  text-align: left;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  font-weight: 600;
  color: var(--text-light);
  font-size: 0.875rem;
}

.status.confirmed {
  background-color: #dcfce7;
  color: #166534;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}


</style>
