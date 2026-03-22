<template>
  <div class="agent-layout">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="brand-logo">LE</div>
        <div>
          <div class="brand-name">LUXE ESTATE</div>
          <div class="brand-role">Sub-Agent Portal</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section-label">Main</div>
        <NuxtLink to="/agent" class="nav-item" exact-active-class="active">
          <span class="nav-icon">📊</span> Dashboard
        </NuxtLink>
        <NuxtLink to="/agent/properties" class="nav-item" active-class="active">
          <span class="nav-icon">🏠</span> My Properties
        </NuxtLink>
        <NuxtLink to="/agent/appointments" class="nav-item" active-class="active">
          <span class="nav-icon">📅</span> Appointments
        </NuxtLink>
        <NuxtLink to="/agent/leads" class="nav-item" active-class="active">
          <span class="nav-icon">🎯</span> Leads
        </NuxtLink>
        <div class="nav-section-label">Insights</div>
        <NuxtLink to="/agent/performance" class="nav-item" active-class="active">
          <span class="nav-icon">📈</span> Performance
        </NuxtLink>
        <NuxtLink to="/agent/ai-training" class="nav-item" active-class="active">
          <span class="nav-icon">🤖</span> AI Knowledge
        </NuxtLink>
        <div class="nav-divider"></div>
        <NuxtLink to="/" class="nav-item muted">
          <span class="nav-icon">🏡</span> View Site
        </NuxtLink>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ initials }}</div>
          <div>
            <div class="user-name">{{ auth.user?.name }}</div>
            <div class="user-role">Sub-Agent</div>
          </div>
        </div>
        <button @click="auth.logout()" class="btn-logout" title="Logout">⎋</button>
      </div>
    </aside>

    <div class="main-area">
      <header class="top-bar">
        <div class="top-bar-title">{{ pageTitle }}</div>
        <div class="top-bar-right">
          <span class="badge-role">Sub-Agent</span>
        </div>
      </header>
      <main class="page-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
const auth = useAuthStore()
const route = useRoute()

const pageTitles = {
  '/agent': 'Dashboard',
  '/agent/properties': 'My Properties',
  '/agent/appointments': 'Appointments',
  '/agent/leads': 'Leads',
  '/agent/performance': 'Performance',
  '/agent/ai-training': 'AI Knowledge Base',
}
const pageTitle = computed(() => pageTitles[route.path] || 'Agent Portal')

const initials = computed(() => {
  const name = auth.user?.name || 'A'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2)
})

onMounted(() => auth.initAuth())
</script>

<style scoped>
.agent-layout {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
}

/* ── Sidebar ── */
.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: linear-gradient(180deg, #0f172a 0%, #1a2744 100%);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}

.brand-logo {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: var(--accent-color, #c9a84c);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
  color: white;
  flex-shrink: 0;
}

.brand-name {
  font-size: 0.8rem;
  font-weight: 800;
  color: white;
  letter-spacing: 0.1em;
}

.brand-role {
  font-size: 0.65rem;
  color: var(--accent-color, #c9a84c);
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-section-label {
  color: rgba(255,255,255,0.3);
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.75rem 1.25rem 0.4rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1.25rem;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.15s;
  border-left: 3px solid transparent;
}

.nav-item:hover { color: white; background: rgba(255,255,255,0.06); }
.nav-item.active { color: white; background: rgba(255,255,255,0.1); border-left-color: var(--accent-color, #c9a84c); }
.nav-item.muted { opacity: 0.5; }
.nav-item.muted:hover { opacity: 0.8; }
.nav-icon { font-size: 1rem; width: 1.2rem; text-align: center; }

.nav-divider { height: 1px; background: rgba(255,255,255,0.07); margin: 0.75rem 1.25rem; }

.sidebar-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(255,255,255,0.07);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-info { display: flex; align-items: center; gap: 0.6rem; flex: 1; min-width: 0; }
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--accent-color, #c9a84c);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 700; color: white; flex-shrink: 0;
}
.user-name { font-size: 0.8rem; font-weight: 600; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 0.65rem; color: rgba(255,255,255,0.4); }
.btn-logout { background: none; border: none; color: rgba(255,255,255,0.4); cursor: pointer; font-size: 1.1rem; padding: 0.25rem; }
.btn-logout:hover { color: #ef4444; }

/* ── Main Area ── */
.main-area { flex: 1; display: flex; flex-direction: column; min-width: 0; }

.top-bar {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 2rem;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 10;
}

.top-bar-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
.badge-role { background: #d1fae5; color: #065f46; font-size: 0.7rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; }
.page-content { flex: 1; padding: 2rem; }
</style>
