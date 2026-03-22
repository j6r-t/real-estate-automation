<template>
  <div>
    <div class="page-header">
      <h2>Property Inventory</h2>
      <button @click="showAdd = true" class="btn btn-primary">+ Add Property</button>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <select v-model="statusFilter" class="filter-select">
        <option value="">All Status</option>
        <option value="unassigned">Unassigned</option>
        <option value="active">Active</option>
        <option value="sold">Sold</option>
      </select>
    </div>

    <div class="card">
      <table class="data-table" v-if="filtered.length > 0">
        <thead>
          <tr>
            <th>Title</th>
            <th>Location</th>
            <th>Price</th>
            <th>Type</th>
            <th>Status</th>
            <th>Assigned Agent</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prop in filtered" :key="prop.id">
            <td><strong>{{ prop.title }}</strong></td>
            <td>{{ prop.location }}</td>
            <td>{{ prop.price.toLocaleString() }} TND</td>
            <td>{{ prop.type }}</td>
            <td><span :class="['badge', prop.status]">{{ prop.status }}</span></td>
            <td>
              <span v-if="prop.agent">{{ prop.agent.full_name }}</span>
              <span v-else class="unassigned-text">— Unassigned</span>
            </td>
            <td class="actions-cell">
              <button @click="openAssign(prop)" class="btn-sm btn-outline" :disabled="prop.status === 'sold'">Assign</button>
              <button @click="unassign(prop.id)" class="btn-sm btn-danger" v-if="prop.agent_id">Unassign</button>
              <button @click="deleteProp(prop.id)" class="btn-sm btn-ghost">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">No properties found</div>
    </div>

    <!-- Assign Modal -->
    <div v-if="assignModal" class="modal-overlay" @click.self="assignModal = false">
      <div class="modal">
        <h3>Assign "{{ assigningProp?.title }}"</h3>
        <div class="form-group">
          <label>Select Sub-Agent</label>
          <select v-model="selectedAgent">
            <option value="">Choose agent...</option>
            <option v-for="a in agents" :key="a.id" :value="a.id">{{ a.full_name }} ({{ a.email }})</option>
          </select>
        </div>
        <div class="modal-actions">
          <button @click="assignModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="doAssign" class="btn btn-primary" :disabled="!selectedAgent">Assign Property</button>
        </div>
      </div>
    </div>

    <!-- Add Property Modal -->
    <div v-if="showAdd" class="modal-overlay" @click.self="showAdd = false">
      <div class="modal">
        <h3>Add New Property</h3>
        <form @submit.prevent="addProperty">
          <div class="form-group"><label>Title</label><input v-model="addForm.title" required /></div>
          <div class="form-group"><label>Location</label><input v-model="addForm.location" required /></div>
          <div class="form-row">
            <div class="form-group"><label>Price (TND)</label><input v-model="addForm.price" type="number" required /></div>
            <div class="form-group"><label>Surface (m²)</label><input v-model="addForm.surface" type="number" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Bedrooms</label><input v-model="addForm.bedrooms" type="number" /></div>
            <div class="form-group"><label>Bathrooms</label><input v-model="addForm.bathrooms" type="number" /></div>
          </div>
          <div class="form-group">
            <label>Type</label>
            <select v-model="addForm.type">
              <option value="apartment">Apartment</option>
              <option value="villa">Villa</option>
              <option value="house">House</option>
              <option value="studio">Studio</option>
              <option value="commercial">Commercial</option>
              <option value="land">Land</option>
            </select>
          </div>
          <div class="form-group"><label>Image URL</label><input v-model="addForm.image_url" type="url" /></div>
          <div class="modal-actions">
            <button type="button" @click="showAdd = false" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary">Add Property</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'head-agent' })
const properties = ref([])
const agents = ref([])
const statusFilter = ref('')
const assignModal = ref(false)
const assigningProp = ref(null)
const selectedAgent = ref('')
const showAdd = ref(false)
const addForm = ref({ title: '', location: '', price: 0, surface: null, bedrooms: null, bathrooms: null, type: 'apartment', image_url: '' })

const filtered = computed(() => statusFilter.value ? properties.value.filter(p => p.status === statusFilter.value) : properties.value)

const fetchData = async () => {
  const [props, users] = await Promise.all([
    $fetch('http://localhost:8000/properties/'),
    $fetch('http://localhost:8000/users/')
  ])
  properties.value = props
  agents.value = users.filter(u => u.role === 'sub_agent')
}

const openAssign = (prop) => { assigningProp.value = prop; selectedAgent.value = ''; assignModal.value = true }

const doAssign = async () => {
  await $fetch(`http://localhost:8000/properties/${assigningProp.value.id}/assign`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent_id: Number(selectedAgent.value) })
  })
  assignModal.value = false; fetchData()
}

const unassign = async (id) => {
  await $fetch(`http://localhost:8000/properties/${id}/unassign`, { method: 'PUT' })
  fetchData()
}

const deleteProp = async (id) => {
  if (confirm('Delete this property?')) {
    await $fetch(`http://localhost:8000/properties/${id}`, { method: 'DELETE' })
    fetchData()
  }
}

const addProperty = async () => {
  await $fetch('http://localhost:8000/properties/', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(addForm.value)
  })
  showAdd.value = false
  addForm.value = { title: '', location: '', price: 0, surface: null, bedrooms: null, bathrooms: null, type: 'apartment', image_url: '' }
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.page-header h2 { margin: 0; }
.filter-bar { margin-bottom: 1.25rem; }
.filter-select { padding: 0.5rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid #f1f5f9; font-size: 0.875rem; }
.data-table th { color: #64748b; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.badge { padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: capitalize; }
.badge.active { background: #dcfce7; color: #166534; }
.badge.unassigned { background: #fef9c3; color: #713f12; }
.badge.sold { background: #fee2e2; color: #991b1b; }
.unassigned-text { color: #94a3b8; font-style: italic; }
.actions-cell { display: flex; gap: 0.5rem; align-items: center; }
.btn-sm { padding: 0.35rem 0.75rem; border-radius: 6px; border: none; font-size: 0.78rem; font-weight: 600; cursor: pointer; }
.btn-outline { background: white; border: 1.5px solid #e2e8f0; color: #0f172a; }
.btn-outline:hover { border-color: #8b5cf6; color: #5b21b6; }
.btn-danger { background: #fee2e2; color: #dc2626; }
.btn-ghost { background: none; color: #94a3b8; font-size: 1rem; }
.btn-ghost:hover { color: #dc2626; }
.empty-state { text-align: center; color: #94a3b8; padding: 3rem; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 90%; max-width: 520px; max-height: 85vh; overflow-y: auto; }
.modal h3 { margin: 0 0 1.5rem; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; }
.form-group input, .form-group select { width: 100%; padding: 0.7rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-family: inherit; box-sizing: border-box; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>
