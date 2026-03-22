<template>
  <div class="admin-layout">
    <!-- Top Header -->
    <header class="admin-header">
      <div class="header-content">
        <div class="brand">
          <span class="logo-text">LUXE ESTATE</span>
          <span class="badge-admin">Admin Panel</span>
        </div>
        <div class="user-section">
          <span class="user-name">{{ auth.user?.name || 'Admin' }}</span>
          <button @click="auth.logout()" class="btn-logout">Logout</button>
        </div>
      </div>
    </header>

    <!-- Body: Sidebar + Content -->
    <div class="admin-body">
      <!-- Persistent Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-label">Navigation</div>
        <nav>
          <NuxtLink to="/admin" class="nav-item" exact-active-class="active">
            <span class="nav-icon">📊</span> Dashboard
          </NuxtLink>
          <NuxtLink to="/admin/properties" class="nav-item" active-class="active">
            <span class="nav-icon">🏠</span> Properties
          </NuxtLink>
          <NuxtLink to="/admin/users" class="nav-item" active-class="active">
            <span class="nav-icon">👥</span> Users
          </NuxtLink>
          <NuxtLink to="/admin/appointments" class="nav-item" active-class="active">
            <span class="nav-icon">📅</span> Appointments
          </NuxtLink>
          <NuxtLink to="/admin/agencies" class="nav-item" active-class="active">
            <span class="nav-icon">🏢</span> Agencies
          </NuxtLink>
          <div class="nav-divider"></div>
          <NuxtLink to="/" class="nav-item view-site">
            <span class="nav-icon">🏡</span> View Site
          </NuxtLink>
        </nav>
      </aside>

      <!-- Page Content -->
      <main class="admin-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
const auth = useAuthStore()
onMounted(() => auth.initAuth())
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f1f5f9;
  display: flex;
  flex-direction: column;
}

/* ---- Header ---- */
.admin-header {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
  color: white;
  padding: 0 2rem;
  height: 60px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  position: sticky;
  top: 0;
  z-index: 200;
  flex-shrink: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: white;
}

.badge-admin {
  background: var(--accent-color, #c9a84c);
  color: white;
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.user-name {
  font-size: 0.875rem;
  opacity: 0.85;
}

.btn-logout {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  padding: 0.4rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s;
}
.btn-logout:hover { background: rgba(255,255,255,0.2); }

/* ---- Body ---- */
.admin-body {
  display: flex;
  flex: 1;
  min-height: 0;
}

/* ---- Sidebar ---- */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: linear-gradient(180deg, #0f172a 0%, #1e2d4a 100%);
  min-height: calc(100vh - 60px);
  padding: 1.5rem 0;
  position: sticky;
  top: 60px;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.sidebar-label {
  color: rgba(255,255,255,0.4);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0 1.25rem 0.75rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  margin-bottom: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 1.25rem;
  color: rgba(255,255,255,0.65);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255,255,255,0.07);
  color: white;
}

.nav-item.active {
  background: rgba(255,255,255,0.1);
  color: white;
  border-left-color: var(--accent-color, #c9a84c);
}

.nav-icon { font-size: 1rem; width: 1.25rem; text-align: center; }

.nav-divider {
  height: 1px;
  background: rgba(255,255,255,0.08);
  margin: 0.75rem 1.25rem;
}

.view-site { opacity: 0.6; }
.view-site:hover { opacity: 1; }

/* ---- Content ---- */
.admin-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
