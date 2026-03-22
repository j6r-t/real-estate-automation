<template>
  <div class="layout">
    <header class="header">
      <div class="container nav">
        <NuxtLink to="/" class="logo">LUXE ESTATE</NuxtLink>
        <nav>
          <ul class="nav-links">
            <li><NuxtLink to="/">Properties</NuxtLink></li>
            <li><NuxtLink to="/about">Our Story</NuxtLink></li>
            
            <li v-if="!auth.isAuthenticated">
              <NuxtLink to="/auth/login" class="btn btn-outline">Sign In</NuxtLink>
            </li>
            <li v-else class="user-menu">
              <span>Hi, {{ auth.user?.name }}</span>
              <button @click="auth.logout" class="btn-text">Logout</button>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <slot />
    </main>

    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-col">
            <h3>LUXE ESTATE</h3>
            <p>Elevating the real estate experience through technology and personalized service.</p>
          </div>
          <div class="footer-col">
            <h3>Quick Links</h3>
            <ul class="footer-links">
              <li><NuxtLink to="/">Properties</NuxtLink></li>
              <li><NuxtLink to="/about">About Us</NuxtLink></li>
              <li><NuxtLink to="/contact">Contact</NuxtLink></li>
            </ul>
          </div>
          <div class="footer-col">
            <h3>Contact</h3>
            <ul class="footer-links">
              <li>123 Luxury Blvd, City</li>
              <li>contact@luxeestate.com</li>
              <li>+1 (555) 123-4567</li>
            </ul>
          </div>
        </div>
        <div class="copyright">
          <p>&copy; 2024 Luxe Estate Agency. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const auth = useAuthStore()

onMounted(() => {
  auth.initAuth()
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: var(--primary-color);
  color: white;
  padding: 0.75rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
  letter-spacing: 0.05em;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 2rem;
  margin: 0;
  padding: 0;
  align-items: center;
}

.nav-links a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  font-size: 0.95rem;
}

.nav-links a:hover {
  color: white;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255,255,255,0.1);
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.user-menu span {
  font-size: 0.9rem;
  font-weight: 500;
}

.btn-text {
  background: none;
  border: none;
  color: var(--accent-color);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.btn-text:hover {
  opacity: 0.8;
}

.main-content {
  flex: 1;
}

.footer {
  background-color: var(--primary-color);
  color: white;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-section h4 {
  color: white;
  margin-bottom: 1rem;
}

.footer-section p,
.footer-section a {
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.7);
  font-size: 0.875rem;
}
</style>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}
</style>
