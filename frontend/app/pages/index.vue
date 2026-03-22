<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <div class="container hero-content">
        <h1>Discover Your Dream Sanctuary</h1>
        <p>Exclusive properties for the discerning client. Automation meets elegance.</p>
        
        <!-- Search Filter Bar -->
        <div class="search-bar">
          <div class="filter-group">
            <label>Location (Region)</label>
            <select v-model="filters.location">
              <option value="">All Regions</option>
              <option>Tunis</option>
              <option>Carthage</option>
              <option>Les Berges du Lac</option>
              <option>La Marsa</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Type</label>
            <select v-model="filters.type">
              <option value="">All Types</option>
              <option value="apartment">Apartment</option>
              <option value="villa">Villa</option>
              <option value="house">House</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Price Range (TND)</label>
            <select v-model="filters.priceRange">
              <option value="">Any Price</option>
              <option value="0-300000">0 - 300k DT</option>
              <option value="300000-600000">300k - 600k DT</option>
              <option value="600000-999999999">600k+ DT</option>
            </select>
          </div>
          <button @click="searchProperties" class="btn btn-primary search-btn">Search Properties</button>
        </div>
      </div>
    </section>

    <!-- Listings Section -->
    <section class="container section-padding">
      <div class="section-header">
        <h2>{{ filteredProperties.length > 0 ? 'Available Properties' : 'No Properties Found' }}</h2>
      </div>

      <div v-if="filteredProperties.length > 0" class="properties-grid">
        <div class="property-card" v-for="property in filteredProperties" :key="property.id">
          <div class="card-image" :style="{ backgroundImage: `url(${property.image_url || 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750'})` }">
            <span class="badge">For Sale</span>
          </div>
          <div class="card-content">
            <div class="card-header">
              <span class="price">{{ property.price.toLocaleString() }} DT</span>
              <span class="type">{{ property.type }}</span>
            </div>
            <h3>{{ property.title }}</h3>
            <p class="location">{{ property.location }}</p>
            <div class="card-features">
              <span><i class="icon">🛏</i> {{ property.bedrooms }} Beds</span>
              <span><i class="icon">🚿</i> {{ property.bathrooms }} Baths</span>
              <span><i class="icon">📏</i> {{ property.surface }} m²</span>
            </div>
            <div class="card-actions">
               <NuxtLink :to="`/properties/${property.id}`" class="btn btn-outline full-width">View Details</NuxtLink>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-results">
        <p>No properties match your search criteria.</p>
      </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
         <h2>Ready to visit?</h2>
         <p>Our AI Assistant is available 24/7 to schedule your private viewing instantly.</p>
         <a href="https://t.me/YourBotUsername" class="btn btn-secondary">Chat on Telegram</a>
      </div>
    </section>
  </div>
</template>

<script setup>
const properties = ref([])
const filters = ref({
  location: '',
  type: '',
  priceRange: ''
})

const filteredProperties = computed(() => {
  let result = properties.value
  
  if (filters.value.location) {
    result = result.filter(p => p.location.includes(filters.value.location))
  }
  
  if (filters.value.type) {
    result = result.filter(p => p.type === filters.value.type)
  }
  
  if (filters.value.priceRange) {
    const [min, max] = filters.value.priceRange.split('-').map(Number)
    result = result.filter(p => p.price >= min && p.price <= max)
  }
  
  return result
})

const fetchProperties = async () => {
  try {
    const data = await $fetch('http://localhost:8000/properties/')
    properties.value = data
  } catch (e) {
    console.error('Failed to fetch properties', e)
  }
}

const searchProperties = () => {
  // Filtering is reactive, so this just triggers any additional behavior
}

onMounted(() => {
  fetchProperties()
})
</script>

<style scoped>
.hero {
  background: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.7)), url('https://images.unsplash.com/photo-1600596542815-2a4d04774c13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 8rem 0 10rem;
  text-align: center;
  position: relative;
}

.hero-content h1 {
  font-size: 3.5rem;
  color: white;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 3rem;
  opacity: 0.9;
}

/* Search Bar */
.search-bar {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  display: flex;
  gap: 1rem;
  max-width: 900px;
  margin: 0 auto;
  box-shadow: var(--shadow-lg);
  align-items: flex-end;
  transform: translateY(3rem); /* Overlap hero */
}

.filter-group {
  flex: 1;
  text-align: left;
}

.filter-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.filter-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: var(--font-body);
  color: var(--secondary-color);
}

.search-btn {
  height: 48px; /* Match input height roughly */
}

/* Properties Grid */
.section-padding {
  padding-top: 6rem;
  padding-bottom: 6rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2.5rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.view-all {
  color: var(--accent-color);
  font-weight: 600;
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
}

.property-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
}

.property-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.card-image {
  height: 250px;
  background-color: #cbd5e1;
  position: relative;
  background-size: cover;
  background-position: center;
}

.badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: var(--accent-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.price {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}

.type {
  font-size: 0.875rem;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.location {
  color: var(--text-light);
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.card-features {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  padding: 1rem 0;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: var(--secondary-color);
}

.card-actions {
  margin-top: auto;
  padding-top: 1.25rem;
}

.full-width {
  width: 100%;
  text-align: center;
}

.cta-section {
  background-color: var(--primary-color);
  color: white;
  padding: 5rem 0;
  text-align: center;
}

.cta-section h2 {
    color: white;
}

.no-results {
  text-align: center;
  padding: 4rem 0;
  color: var(--text-light);
}
</style>
