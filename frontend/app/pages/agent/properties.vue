<template>
  <div>
    <div class="page-header">
      <h2>My Assigned Properties</h2>
    </div>

    <div class="properties-grid" v-if="properties.length > 0">
      <div class="prop-card" v-for="prop in properties" :key="prop.id">
        <div class="prop-img" :style="{ backgroundImage: `url(${prop.image_url || ''})` }">
          <span :class="['status-badge', prop.status]">{{ prop.status }}</span>
          <span class="type-badge">{{ prop.type }}</span>
        </div>
        <div class="prop-body">
          <div class="prop-price">{{ prop.price.toLocaleString() }} <span>TND</span></div>
          <h3>{{ prop.title }}</h3>
          <p class="prop-location">📍 {{ prop.location }}</p>
          <div class="prop-specs">
            <span>🛏 {{ prop.bedrooms ?? '—' }}</span>
            <span>🚿 {{ prop.bathrooms ?? '—' }}</span>
            <span>📏 {{ prop.surface ?? '—' }} m²</span>
          </div>
          <div class="prop-actions">
            <button @click="openEdit(prop)" class="btn btn-outline btn-sm">✏️ Edit Listing</button>
            <NuxtLink :to="`/properties/${prop.id}`" class="btn btn-primary btn-sm">View</NuxtLink>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>No properties assigned to you yet.</p>
      <small>Your head agent will assign properties from the agency inventory.</small>
    </div>

    <!-- Edit Modal -->
    <div v-if="editModal" class="modal-overlay" @click.self="editModal = false">
      <div class="modal">
        <h3>Edit Listing</h3>
        <form @submit.prevent="saveEdit">
          <div class="form-group">
            <label>Title</label>
            <input v-model="form.title" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Price (TND)</label>
              <input v-model="form.price" type="number" />
            </div>
            <div class="form-group">
              <label>Surface (m²)</label>
              <input v-model="form.surface" type="number" />
            </div>
          </div>
          <div class="form-group">
            <label>Image URL</label>
            <input v-model="form.image_url" type="url" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="editModal = false" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'agent' })
const auth = useAuthStore()
const properties = ref([])
const editModal = ref(false)
const editingId = ref(null)
const form = ref({})

const fetchProperties = async () => {
  const token = localStorage.getItem('auth_token')
  const headers = { Authorization: `Bearer ${token}` }
  try {
    const me = await $fetch('http://localhost:8000/users/me', { headers })
    const data = await $fetch(`http://localhost:8000/properties/?agent_id=${me.id}`)
    properties.value = data
  } catch(e) { console.error(e) }
}

const openEdit = (prop) => {
  editingId.value = prop.id
  form.value = { ...prop }
  editModal.value = true
}

const saveEdit = async () => {
  try {
    await $fetch(`http://localhost:8000/properties/${editingId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    editModal.value = false
    fetchProperties()
  } catch(e) { alert('Failed to update') }
}

onMounted(() => { auth.initAuth(); fetchProperties() })
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.page-header h2 { margin: 0; }
.properties-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.prop-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.07); display: flex; flex-direction: column; }
.prop-img { height: 180px; background: #cbd5e1 center/cover; position: relative; display: flex; justify-content: space-between; align-items: flex-start; padding: 0.75rem; }
.status-badge { font-size: 0.7rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 20px; text-transform: capitalize; }
.status-badge.active { background: #dcfce7; color: #166534; }
.status-badge.unassigned { background: #fef9c3; color: #713f12; }
.status-badge.sold { background: #fee2e2; color: #991b1b; }
.type-badge { font-size: 0.7rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 20px; background: rgba(0,0,0,0.5); color: white; text-transform: capitalize; }
.prop-body { padding: 1.25rem; display: flex; flex-direction: column; flex: 1; }
.prop-price { font-size: 1.3rem; font-weight: 800; color: #0f172a; }
.prop-price span { font-size: 0.8rem; color: #64748b; }
.prop-body h3 { margin: 0.25rem 0 0.25rem; font-size: 0.95rem; }
.prop-location { color: #64748b; font-size: 0.85rem; margin: 0 0 0.75rem; }
.prop-specs { display: flex; gap: 1rem; font-size: 0.8rem; color: #475569; border-top: 1px solid #f1f5f9; padding-top: 0.75rem; margin-top: auto; }
.prop-actions { display: flex; gap: 0.75rem; margin-top: 0.75rem; }
.btn-sm { padding: 0.45rem 1rem; font-size: 0.825rem; flex: 1; text-align: center; }
.empty-state { text-align: center; padding: 4rem; color: #64748b; background: white; border-radius: 12px; }
.empty-state small { display: block; margin-top: 0.5rem; color: #94a3b8; }
/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 90%; max-width: 500px; max-height: 85vh; overflow-y: auto; }
.modal h3 { margin: 0 0 1.5rem; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; }
.form-group input, .form-group textarea { width: 100%; padding: 0.7rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-family: inherit; box-sizing: border-box; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>
