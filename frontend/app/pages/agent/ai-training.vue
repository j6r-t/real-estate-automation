<template>
  <div>
    <div class="page-header">
      <div>
        <h1>🤖 AI Knowledge Base</h1>
        <p>Train the AI assistant by adding Q&A entries. The bot uses this to answer client questions.</p>
      </div>
      <button @click="openAdd" class="btn btn-primary">+ Add Entry</button>
    </div>

    <!-- Category Tabs -->
    <div class="tabs">
      <button v-for="cat in categories" :key="cat.value"
        :class="['tab', { active: activeCategory === cat.value }]"
        @click="activeCategory = cat.value">
        {{ cat.label }}
      </button>
    </div>

    <!-- Knowledge Entries Grid -->
    <div class="entries-grid">
      <div v-for="entry in filteredEntries" :key="entry.id" class="entry-card">
        <div class="entry-header">
          <span :class="['cat-badge', entry.category]">{{ entry.category }}</span>
          <div class="entry-actions">
            <button @click="openEdit(entry)" title="Edit">✏️</button>
            <button @click="deleteEntry(entry.id)" title="Delete">🗑️</button>
          </div>
        </div>
        <h3>{{ entry.question }}</h3>
        <p>{{ entry.answer }}</p>
        <div class="entry-footer">
          <span :class="['active-badge', { inactive: !entry.is_active }]">
            {{ entry.is_active ? '● Active' : '○ Inactive' }}
          </span>
        </div>
      </div>

      <div v-if="filteredEntries.length === 0" class="empty-state">
        <p>No entries in this category. Add one!</p>
      </div>
    </div>

    <!-- Add / Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>{{ editingEntry ? 'Edit Knowledge Entry' : 'Add Knowledge Entry' }}</h3>

        <div class="form-group">
          <label>Topic / Short Label</label>
          <input type="text" v-model="form.topic" placeholder="e.g. Opening Hours" />
        </div>

        <div class="form-group">
          <label>Question (as a client would ask)</label>
          <input type="text" v-model="form.question" placeholder="What are your office hours?" />
        </div>

        <div class="form-group">
          <label>Answer</label>
          <textarea v-model="form.answer" rows="4" placeholder="We are open Monday–Friday from 9am to 6pm..."></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Category</label>
            <select v-model="form.category">
              <option value="general">General</option>
              <option value="pricing">Pricing</option>
              <option value="booking">Booking</option>
              <option value="property">Property</option>
            </select>
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="form.is_active">
              <option :value="true">Active</option>
              <option :value="false">Inactive</option>
            </select>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="btn btn-secondary">Cancel</button>
          <button @click="saveEntry" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Entry' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'agent' })
const auth = useAuthStore()
const entries = ref([])
const showModal = ref(false)
const editingEntry = ref(null)
const saving = ref(false)
const activeCategory = ref('all')

const categories = [
  { value: 'all', label: '📋 All' },
  { value: 'general', label: '💬 General' },
  { value: 'pricing', label: '💰 Pricing' },
  { value: 'booking', label: '📅 Booking' },
  { value: 'property', label: '🏠 Property' },
]

const emptyForm = () => ({ topic: '', question: '', answer: '', category: 'general', is_active: true })
const form = ref(emptyForm())

const filteredEntries = computed(() =>
  activeCategory.value === 'all'
    ? entries.value
    : entries.value.filter(e => e.category === activeCategory.value)
)

const fetchEntries = async () => {
  entries.value = await $fetch('http://localhost:8000/ai-knowledge/')
}

const openAdd = () => {
  editingEntry.value = null
  form.value = emptyForm()
  showModal.value = true
}

const openEdit = (entry) => {
  editingEntry.value = entry
  form.value = { ...entry }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingEntry.value = null
}

const saveEntry = async () => {
  saving.value = true
  try {
    if (editingEntry.value) {
      await $fetch(`http://localhost:8000/ai-knowledge/${editingEntry.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    } else {
      await $fetch('http://localhost:8000/ai-knowledge/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    }
    closeModal()
    await fetchEntries()
  } catch (e) {
    alert('Failed to save entry')
  } finally {
    saving.value = false
  }
}

const deleteEntry = async (id) => {
  if (!confirm('Delete this knowledge entry?')) return
  await $fetch(`http://localhost:8000/ai-knowledge/${id}`, { method: 'DELETE' })
  await fetchEntries()
}

onMounted(() => {
  auth.initAuth()
  fetchEntries()
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.75rem; color: var(--primary-color); margin: 0 0 0.25rem; }
.page-header p { color: #64748b; font-size: 0.9rem; margin: 0; max-width: 500px; }

.tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
.tab { padding: 0.4rem 1rem; border-radius: 20px; border: 1px solid #e2e8f0; background: white; cursor: pointer; font-size: 0.875rem; font-weight: 500; color: #64748b; transition: all 0.2s; }
.tab.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }

.entries-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.25rem; }

.entry-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.08); border: 1px solid #f1f5f9; transition: box-shadow 0.2s; }
.entry-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

.entry-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.cat-badge { padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: capitalize; }
.cat-badge.general  { background: #f1f5f9; color: #475569; }
.cat-badge.pricing   { background: #fef3c7; color: #92400e; }
.cat-badge.booking   { background: #d1fae5; color: #065f46; }
.cat-badge.property  { background: #dbeafe; color: #1e40af; }

.entry-actions { display: flex; gap: 0.25rem; }
.entry-actions button { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0.2rem 0.4rem; border-radius: 4px; }
.entry-actions button:hover { background: #f1f5f9; }

.entry-card h3 { font-size: 0.95rem; color: #1e293b; margin: 0 0 0.5rem; line-height: 1.4; }
.entry-card p { font-size: 0.875rem; color: #64748b; margin: 0 0 1rem; line-height: 1.5; }

.entry-footer { border-top: 1px solid #f1f5f9; padding-top: 0.75rem; }
.active-badge { font-size: 0.75rem; font-weight: 600; color: #10b981; }
.active-badge.inactive { color: #94a3b8; }

.empty-state { grid-column: 1/-1; text-align: center; padding: 3rem; color: #94a3b8; background: white; border-radius: 12px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 16px; width: 90%; max-width: 560px; max-height: 90vh; overflow-y: auto; }
.modal h3 { margin: 0 0 1.5rem; color: var(--primary-color); font-size: 1.25rem; }

.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; color: #374151; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; padding: 0.65rem 0.875rem; border: 1px solid #e2e8f0; border-radius: 8px;
  font-family: var(--font-body); font-size: 0.9rem; box-sizing: border-box;
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>
