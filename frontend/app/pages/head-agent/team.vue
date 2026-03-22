<template>
  <div>
    <div class="page-header">
      <h2>My Team</h2>
      <button @click="showInvite = true" class="btn btn-primary">+ Add Sub-Agent</button>
    </div>

    <div class="team-grid" v-if="agents.length > 0">
      <div class="agent-card" v-for="agent in agents" :key="agent.id">
        <div class="agent-avatar">{{ initials(agent.full_name) }}</div>
        <div class="agent-info">
          <div class="agent-name">{{ agent.full_name }}</div>
          <div class="agent-email">{{ agent.email }}</div>
          <div class="agent-phone">{{ agent.phone || '—' }}</div>
        </div>
        <div class="agent-stats">
          <div class="stat"><strong>{{ propCountForAgent(agent.id) }}</strong><span>Properties</span></div>
          <div class="stat"><strong>{{ apptCountForAgent(agent.id) }}</strong><span>Visits</span></div>
        </div>
        <div class="agent-actions">
          <span :class="['badge', agent.is_active ? 'active' : 'inactive']">{{ agent.is_active ? 'Active' : 'Inactive' }}</span>
        </div>
      </div>
    </div>
    <div v-else class="card empty-state">
      <p>No sub-agents in your team yet.</p>
      <small>Add sub-agents using the button above to start assigning properties.</small>
    </div>

    <!-- Add Sub-Agent Modal -->
    <div v-if="showInvite" class="modal-overlay" @click.self="showInvite = false">
      <div class="modal">
        <h3>Add Sub-Agent to Team</h3>
        <p class="modal-hint">Assign an existing user with sub_agent role to your agency, or create a new one.</p>
        <form @submit.prevent="createAndAdd">
          <div class="form-group"><label>Full Name</label><input v-model="form.full_name" required /></div>
          <div class="form-group"><label>Email</label><input v-model="form.email" type="email" required /></div>
          <div class="form-group"><label>Phone</label><input v-model="form.phone" type="tel" /></div>
          <div class="form-group"><label>Password</label><input v-model="form.password" type="password" required /></div>
          <div class="modal-actions">
            <button type="button" @click="showInvite = false" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary">Create & Add</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'head-agent' })
const auth = useAuthStore()
const agents = ref([])
const properties = ref([])
const appointments = ref([])
const showInvite = ref(false)
const form = ref({ full_name: '', email: '', phone: '', password: '' })

const initials = (name) => (name || 'A').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2)
const propCountForAgent = (id) => properties.value.filter(p => p.agent_id === id).length
const apptCountForAgent = (id) => appointments.value.filter(a => a.agent_id === id).length

const fetchData = async () => {
  const token = localStorage.getItem('auth_token')
  const h = { Authorization: `Bearer ${token}` }
  const [users, props, appts] = await Promise.all([
    $fetch('http://localhost:8000/users/'),
    $fetch('http://localhost:8000/properties/'),
    $fetch('http://localhost:8000/appointments/', { headers: h })
  ])
  agents.value = users.filter(u => u.role === 'sub_agent')
  properties.value = props
  appointments.value = appts
}

const createAndAdd = async () => {
  const token = localStorage.getItem('auth_token')
  const me = await $fetch('http://localhost:8000/users/me', { headers: { Authorization: `Bearer ${token}` } })
  const meDetails = await $fetch(`http://localhost:8000/agencies/`, {})
  const myAgency = meDetails.find(a => a.head_agent_id === me.id)
  
  // Create user
  const newUser = await $fetch('http://localhost:8000/users/', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...form.value, role: 'sub_agent' })
  })
  
  // Add to agency if head agent has one
  if (myAgency) {
    await $fetch(`http://localhost:8000/agencies/${myAgency.id}/agents`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: newUser.id })
    })
  }
  showInvite.value = false
  form.value = { full_name: '', email: '', phone: '', password: '' }
  fetchData()
}

onMounted(() => { auth.initAuth(); fetchData() })
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.page-header h2 { margin: 0; }
.team-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25rem; }
.agent-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); display: flex; flex-direction: column; align-items: center; text-align: center; gap: 1rem; }
.agent-avatar { width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #8b5cf6, #5b21b6); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; }
.agent-name { font-size: 1rem; font-weight: 700; color: #0f172a; }
.agent-email, .agent-phone { font-size: 0.8rem; color: #64748b; }
.agent-stats { display: flex; gap: 1.5rem; }
.stat { text-align: center; }
.stat strong { display: block; font-size: 1.25rem; font-weight: 800; color: #0f172a; }
.stat span { font-size: 0.72rem; color: #64748b; }
.badge { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
.badge.active { background: #dcfce7; color: #166534; }
.badge.inactive { background: #fee2e2; color: #991b1b; }
.card.empty-state { background: white; border-radius: 12px; padding: 3rem; text-align: center; color: #64748b; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card.empty-state small { display: block; margin-top: 0.5rem; color: #94a3b8; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 90%; max-width: 460px; }
.modal h3 { margin: 0 0 0.5rem; }
.modal-hint { font-size: 0.85rem; color: #64748b; margin: 0 0 1.5rem; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; }
.form-group input { width: 100%; padding: 0.7rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-family: inherit; box-sizing: border-box; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>
