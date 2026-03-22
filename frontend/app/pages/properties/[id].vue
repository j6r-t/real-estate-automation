<template>
  <div class="container property-details">
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <NuxtLink to="/">Home</NuxtLink> / <span>Properties</span> / <span>{{ property?.title || 'Loading...' }}</span>
    </div>

    <div v-if="property" class="details-header">
      <div>
        <span class="status-badge" :class="property.status">{{ property.status === 'sold' ? 'Sold' : 'For Sale' }}</span>
        <h1>{{ property.title }}</h1>
        <p class="location">📍 {{ property.location }}</p>
      </div>
      <div class="price-box">
        <span class="price">{{ property.price.toLocaleString() }} TND</span>
      </div>
    </div>

    <!-- Gallery -->
    <div v-if="property" class="gallery">
      <div class="main-image" :style="{ backgroundImage: `url(${property.image_url || 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750'})` }"></div>
    </div>

    <div v-if="property" class="content-grid">
      <div class="main-info">
        <section class="section">
          <h2>About this property</h2>
          <p>{{ property.description || 'No description available.' }}</p>
        </section>

        <section class="section">
          <h3>Key Features</h3>
          <ul class="features-list">
            <li><span class="label">Type:</span> {{ property.type }}</li>
            <li><span class="label">Area:</span> {{ property.surface }} m²</li>
            <li><span class="label">Bedrooms:</span> {{ property.bedrooms || '—' }}</li>
            <li><span class="label">Bathrooms:</span> {{ property.bathrooms || '—' }}</li>
            <li><span class="label">Price:</span> {{ property.price.toLocaleString() }} TND</li>
          </ul>
        </section>

        <section class="section">
          <h3>Location</h3>
          <div class="map-placeholder">
            <p>📍 {{ property.location }}</p>
            <p style="color: #64748b; font-size: 0.875rem;">Map integration coming soon</p>
          </div>
        </section>
      </div>

      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- Agent Card -->
        <div class="agent-card">
          <div class="agent-header">
            <div class="agent-avatar">{{ initials(property.agent?.full_name) }}</div>
            <div>
              <div class="agent-label">Listing Agent</div>
              <div class="agent-name">{{ property.agent?.full_name || 'Luxe Estate Team' }}</div>
              <div class="agent-contact" v-if="property.agent?.phone">{{ property.agent.phone }}</div>
            </div>
          </div>
          
          <hr class="divider"/>

          <h3>Interested?</h3>
          <p class="cta-text">Contact our agent directly via Telegram to schedule a visit or ask questions.</p>

          <div class="telegram-section">
            <a :href="`https://t.me/YourBotUsername?start=property_${property.id}`" target="_blank" class="btn btn-telegram full-width">
              <span>✈️ Chat on Telegram</span>
            </a>
            <p class="bot-info">Instant response from our AI Assistant</p>
          </div>
        </div>
      </aside>
    </div>

    <div v-else class="loading">
      <p>Loading property details...</p>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const property = ref(null)

const initials = (name) => (name || 'A').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2)

const fetchProperty = async () => {
  try {
    const data = await $fetch(`http://localhost:8000/properties/${route.params.id}`)
    property.value = data
  } catch (e) { console.error(e) }
}

onMounted(() => { fetchProperty() })
</script>

<style scoped>
.property-details { padding: 2rem 0; }
.breadcrumbs { color: #64748b; margin-bottom: 2rem; font-size: 0.875rem; }
.breadcrumbs a { color: var(--accent-color, #c9a84c); text-decoration: none; }
.details-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0; }
.status-badge { background: var(--accent-color, #c9a84c); color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; display: inline-block; margin-bottom: 0.5rem; }
.status-badge.sold { background: #fee2e2; color: #991b1b; }
.property-details h1 { color: #0f172a; margin-bottom: 0.5rem; font-size: 2rem; }
.location { color: #64748b; font-size: 0.95rem; }
.price { font-size: 2rem; font-weight: 800; color: var(--accent-color, #c9a84c); }
.gallery { margin-bottom: 3rem; }
.main-image { height: 500px; background-color: #cbd5e1; border-radius: 12px; background-size: cover; background-position: center; }
.content-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 3rem; }
.section { margin-bottom: 2.5rem; }
.section h2, .section h3 { color: #0f172a; margin-bottom: 1rem; }
.section p { color: #475569; line-height: 1.6; }
.features-list { list-style: none; padding: 0; }
.features-list li { padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; color: #334155; }
.label { font-weight: 600; color: #64748b; }
.map-placeholder { background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 8px; padding: 3rem; text-align: center; color: #94a3b8; }

/* Agent Card Sidebar */
.agent-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); position: sticky; top: 2rem; border: 1px solid #e2e8f0; }
.agent-header { display: flex; gap: 1rem; align-items: center; margin-bottom: 1.5rem; }
.agent-avatar { width: 48px; height: 48px; border-radius: 50%; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; flex-shrink: 0; }
.agent-label { font-size: 0.7rem; color: #64748b; text-transform: uppercase; font-weight: 700; }
.agent-name { font-weight: 700; color: #0f172a; font-size: 1rem; }
.agent-contact { font-size: 0.85rem; color: #475569; }
.divider { border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }

.cta-text { color: #475569; margin-bottom: 1.5rem; line-height: 1.5; font-size: 0.95rem; }

.full-width { width: 100%; }
.btn-telegram { 
  background: #229ED9; color: white; border: none; padding: 1rem; border-radius: 8px; 
  font-weight: 700; text-decoration: none; display: flex; justify-content: center; align-items: center; 
  gap: 0.5rem; transition: all 0.2s; font-size: 1.1rem;
  box-shadow: 0 4px 6px -1px rgba(34, 158, 217, 0.3);
}
.btn-telegram:hover { background: #1e8bbf; transform: translateY(-2px); box-shadow: 0 6px 8px -1px rgba(34, 158, 217, 0.4); }
.bot-info { text-align: center; font-size: 0.8rem; color: #94a3b8; margin-top: 0.75rem; }

.loading { text-align: center; padding: 4rem 0; color: #64748b; }
</style>
