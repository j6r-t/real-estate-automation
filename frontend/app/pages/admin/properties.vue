<template>
  <div class="admin-page">
    <div class="page-header">
      <h2>Property Management</h2>
      <button @click="showAddModal = true" class="btn btn-primary">+ Add Property</button>
    </div>

    <!-- Properties Table -->
    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Location</th>
            <th>Price (TND)</th>
            <th>Type</th>
            <th>Surface (m²)</th>
            <th>Beds / Baths</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="property in properties" :key="property.id">
            <td><strong>{{ property.title }}</strong></td>
            <td>{{ property.location }}</td>
            <td>{{ property.price.toLocaleString() }} TND</td>
            <td><span class="type-badge">{{ property.type }}</span></td>
            <td>{{ property.surface ?? '—' }} m²</td>
            <td>{{ property.bedrooms ?? '—' }} 🛏 / {{ property.bathrooms ?? '—' }} 🚿</td>
            <td>
              <button @click="editProperty(property)" class="btn-icon">✏️</button>
              <button @click="deletePropertyConfirm(property.id)" class="btn-icon danger">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click.self="closeModals">
      <div class="modal">
        <h3>{{ showEditModal ? 'Edit Property' : 'Add New Property' }}</h3>
        <form @submit.prevent="saveProperty">
          <div class="form-group">
            <label>Title</label>
            <input type="text" v-model="form.title" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Price (TND)</label>
              <input type="number" v-model="form.price" required />
            </div>
            <div class="form-group">
              <label>Surface (m²)</label>
              <input type="number" v-model="form.surface" />
            </div>
          </div>
          <div class="form-group">
            <label>Location</label>
            <input type="text" v-model="form.location" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Type</label>
              <select v-model="form.type">
                <option value="apartment">Apartment</option>
                <option value="villa">Villa</option>
                <option value="house">House</option>
                <option value="land">Land</option>
              </select>
            </div>
            <div class="form-group">
              <label>Bedrooms</label>
              <input type="number" v-model="form.bedrooms" />
            </div>
            <div class="form-group">
              <label>Bathrooms</label>
              <input type="number" v-model="form.bathrooms" />
            </div>
          </div>
          <div class="form-group">
            <label>Image URL</label>
            <input type="url" v-model="form.image_url" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModals" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const properties = ref([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingId = ref(null)

const form = ref({
  title: '',
  description: '',
  price: 0,
  location: '',
  surface: 0,
  type: 'apartment',
  bedrooms: 0,
  bathrooms: 0,
  image_url: ''
})

const fetchProperties = async () => {
  const data = await $fetch('http://localhost:8000/properties/')
  properties.value = data
}

const editProperty = (property) => {
  editingId.value = property.id
  form.value = { ...property }
  showEditModal.value = true
}

const saveProperty = async () => {
  try {
    if (showEditModal.value) {
      // Update
      await $fetch(`http://localhost:8000/properties/${editingId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    } else {
      // Create
      await $fetch('http://localhost:8000/properties/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    }
    closeModals()
    fetchProperties()
  } catch (e) {
    alert('Failed to save property')
  }
}

const deletePropertyConfirm = async (id) => {
  if (confirm('Are you sure you want to delete this property?')) {
    await $fetch(`http://localhost:8000/properties/${id}`, { method: 'DELETE' })
    fetchProperties()
  }
}

const closeModals = () => {
  showAddModal.value = false
  showEditModal.value = false
  form.value = { title: '', description: '', price: 0, location: '', surface: 0, type: 'apartment', bedrooms: 0, bathrooms: 0, image_url: '' }
}

onMounted(() => {
  fetchProperties()
})
</script>

<style scoped>
.admin-page {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  font-weight: 600;
  color: var(--text-light);
  font-size: 0.875rem;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  margin: 0 0.25rem;
}

.btn-icon.danger:hover {
  opacity: 0.7;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: var(--font-body);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  
}
</style>
