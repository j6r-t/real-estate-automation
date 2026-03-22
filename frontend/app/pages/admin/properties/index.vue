<template>
  <div class="admin-page">
    <header class="page-header">
      <h2>Property Management</h2>
      <button class="btn btn-primary">+ Add New Property</button>
    </header>

    <div class="filters">
      <input type="text" placeholder="Search properties..." class="search-input">
      <select class="filter-select">
        <option>All Statuses</option>
        <option>Active</option>
        <option>Sold</option>
      </select>
    </div>

    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Image</th>
            <th>Title</th>
            <th>Location</th>
            <th>Price</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in 5" :key="i">
            <td><div class="thumb"></div></td>
            <td><strong>Luxury Apt {{ i }}</strong><br><span class="text-sm">Ref: #1234{{i}}</span></td>
            <td>Paris, 16ème</td>
            <td>€450,000</td>
            <td><span class="status active">Active</span></td>
            <td class="actions">
              <button class="icon-btn">✏️</button>
              <button class="icon-btn delete">🗑️</button>
            </td>
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

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-input, .filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
}

.search-input {
  flex: 1;
  max-width: 300px;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  text-align: left;
}

.thumb {
  width: 50px;
  height: 50px;
  background-color: #cbd5e1;
  border-radius: 4px;
}

.status.active {
  background-color: #dcfce7;
  color: #166534;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1.1rem;
}

.icon-btn.delete:hover {
  opacity: 0.7;
}
</style>
