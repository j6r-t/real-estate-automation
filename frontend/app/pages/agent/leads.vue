<template>
  <div>
    <div class="page-header">
      <h2>Leads</h2>
      <div class="filter-tabs">
        <button v-for="s in statuses" :key="s" :class="['tab', { active: filter === s }]" @click="filter = s">{{ s }}</button>
      </div>
    </div>

    <div class="card">
      <table class="data-table" v-if="filtered.length > 0">
        <thead>
          <tr>
            <th>Visitor</th>
            <th>Contact</th>
            <th>Property</th>
            <th>Inquiry</th>
            <th>Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lead in filtered" :key="lead.id">
            <td><strong>{{ lead.visitor_name || 'Anonymous' }}</strong></td>
            <td>
              <div>{{ lead.visitor_email || '—' }}</div>
              <small>{{ lead.visitor_phone || '—' }}</small>
            </td>
            <td>{{ lead.property?.title || `Property #${lead.property_id}` }}</td>
            <td class="inquiry-cell">{{ lead.inquiry_text || '—' }}</td>
            <td>{{ formatDate(lead.created_at) }}</td>
            <td>
              <select :value="lead.status" @change="updateStatus(lead.id, $event.target.value)" class="status-select" :class="lead.status">
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="lost">Lost</option>
              </select>
            </td>
            <td>
              <a v-if="lead.visitor_email" :href="`mailto:${lead.visitor_email}`" class="btn-icon" title="Send Email">📧</a>
              <a v-if="lead.visitor_phone" :href="`tel:${lead.visitor_phone}`" class="btn-icon" title="Call">📞</a>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">No {{ filter === 'all' ? '' : filter }} leads found</div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'agent' })
const leads = ref([])
const filter = ref('all')
const statuses = ['all', 'new', 'contacted', 'lost']

const filtered = computed(() =>
  filter.value === 'all' ? leads.value : leads.value.filter(l => l.status === filter.value)
)

const formatDate = (d) => new Date(d).toLocaleDateString('en-GB')

const fetchLeads = async () => {
  const token = localStorage.getItem('auth_token')
  try {
    leads.value = await $fetch('http://localhost:8000/leads/', { headers: { Authorization: `Bearer ${token}` } })
  } catch(e) { console.error(e) }
}

const updateStatus = async (id, status) => {
  const token = localStorage.getItem('auth_token')
  await $fetch(`http://localhost:8000/leads/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ status })
  })
  fetchLeads()
}

onMounted(fetchLeads)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; }
.page-header h2 { margin: 0; }
.filter-tabs { display: flex; gap: 0.5rem; }
.tab { padding: 0.4rem 1rem; border-radius: 20px; border: 1.5px solid #e2e8f0; background: white; cursor: pointer; font-size: 0.8rem; font-weight: 600; text-transform: capitalize; transition: all 0.15s; }
.tab.active { background: #0f172a; color: white; border-color: #0f172a; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid #f1f5f9; font-size: 0.875rem; }
.data-table th { color: #64748b; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.inquiry-cell { max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
small { color: #94a3b8; font-size: 0.75rem; }
.status-select { padding: 0.3rem 0.6rem; border-radius: 20px; border: 1.5px solid #e2e8f0; font-size: 0.75rem; font-weight: 600; cursor: pointer; }
.status-select.new { background: #dbeafe; color: #1e40af; border-color: #bfdbfe; }
.status-select.contacted { background: #d1fae5; color: #065f46; border-color: #a7f3d0; }
.status-select.lost { background: #fee2e2; color: #991b1b; border-color: #fecaca; }
.btn-icon { font-size: 1.1rem; text-decoration: none; margin: 0 0.2rem; }
.empty-state { text-align: center; color: #94a3b8; padding: 3rem; }
</style>
