<template>
  <div class="admin-page">
    <div class="page-header">
      <h2>User Management</h2>
      <button @click="showAddModal = true" class="btn btn-primary">+ Add User</button>
    </div>

    <!-- Users Table -->
    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Member Since</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td><strong>{{ user.full_name || '—' }}</strong></td>
            <td>{{ user.email }}</td>
            <td><span :class="['badge', user.role]">{{ user.role }}</span></td>
            <td>{{ user.phone || '—' }}</td>
            <td><span :class="['status', user.is_active ? 'active' : 'inactive']">{{ user.is_active ? 'Active' : 'Inactive' }}</span></td>
            <td>{{ new Date(user.created_at).toLocaleDateString('en-GB') }}</td>
            <td>
              <button @click="editUser(user)" class="btn-icon">✏️</button>
              <button @click="deleteUserConfirm(user.id)" class="btn-icon danger">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click.self="closeModals">
      <div class="modal">
        <h3>{{ showEditModal ? 'Edit User' : 'Add New User' }}</h3>
        <form @submit.prevent="saveUser">
          <div class="form-group">
            <label>Full Name</label>
            <input type="text" v-model="form.full_name" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input type="email" v-model="form.email" required />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" v-model="form.password" :placeholder="showEditModal ? 'Leave blank to keep current' : 'Enter password'" :required="!showEditModal" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Role</label>
              <select v-model="form.role">
                <option value="client">Client</option>
                <option value="sub_agent">Sub-Agent</option>
                <option value="head_agent">Head Agent</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="form-group">
              <label>Phone</label>
              <input type="tel" v-model="form.phone" />
            </div>
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

const users = ref([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingId = ref(null)

const form = ref({
  email: '',
  password: '',
  full_name: '',
  phone: '',
  role: 'client'
})

const fetchUsers = async () => {
  const data = await $fetch('http://localhost:8000/users/')
  users.value = data
}

const editUser = (user) => {
  editingId.value = user.id
  form.value = { ...user, password: '' } // Don't populate password
  showEditModal.value = true
}

const saveUser = async () => {
  try {
    const payload = { ...form.value }
    
    // Remove password field if empty (for edit)
    if (showEditModal.value && !payload.password) {
      delete payload.password
    }
    
    if (showEditModal.value) {
      // Update
      await $fetch(`http://localhost:8000/users/${editingId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    } else {
      // Create
      await $fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    }
    closeModals()
    fetchUsers()
  } catch (e) {
    alert('Failed to save user: ' + e.message)
  }
}

const deleteUserConfirm = async (id) => {
  if (confirm('Are you sure you want to delete this user?')) {
    await $fetch(`http://localhost:8000/users/${id}`, { method: 'DELETE' })
    fetchUsers()
  }
}

const closeModals = () => {
  showAddModal.value = false
  showEditModal.value = false
  form.value = { email: '', password: '', full_name: '', phone: '', role: 'client' }
}

onMounted(() => {
  fetchUsers()
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

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.admin {
  background: #fef3c7;
  color: #92400e;
}

.badge.agent {
  background: #d1fae5;
  color: #065f46;
}

.badge.client {
  background: #dbeafe;
  color: #1e40af;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status.active {
  background: #dcfce7;
  color: #166534;
}

.status.inactive {
  background: #fee2e2;
  color: #991b1b;
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
  max-width: 500px;
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
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: var(--font-body);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style>
