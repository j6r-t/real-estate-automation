<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">LUXE ESTATE</div>
      <h2>Welcome Back</h2>
      <p class="auth-subtitle">Sign in to your account</p>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email Address</label>
          <input type="email" v-model="email" placeholder="you@example.com" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <button type="submit" class="btn btn-primary full-width" :disabled="loading">
          {{ loading ? 'Signing In...' : 'Sign In' }}
        </button>
        <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
      </form>

      <p class="auth-footer">
        Don't have an account? <NuxtLink to="/auth/register">Sign Up</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')
const authStore = useAuthStore()

const handleLogin = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    await authStore.login(email.value, password.value)
    const role = authStore.user?.role
    if (role === 'admin') {
      navigateTo('/admin')
    } else if (role === 'sub_agent') {
      navigateTo('/agent')
    } else if (role === 'head_agent') {
      navigateTo('/head-agent')
    } else {
      navigateTo('/')
    }
  } catch (e) {
    errorMsg.value = "Invalid email or password"
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #0f172a 100%);
  padding: 2rem;
}

.auth-card {
  background: white;
  padding: 3rem 2.5rem;
  border-radius: 16px;
  box-shadow: 0 25px 60px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.auth-logo {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: var(--accent-color, #c9a84c);
  margin-bottom: 1.5rem;
  text-transform: uppercase;
}

.auth-card h2 {
  color: var(--primary-color);
  font-size: 1.75rem;
  margin-bottom: 0.25rem;
}

.auth-subtitle {
  color: #64748b;
  font-size: 0.95rem;
  margin-bottom: 0;
}

.auth-form {
  margin: 2rem 0 1.5rem;
  text-align: left;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 0.95rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.full-width {
  width: 100%;
  padding: 0.85rem;
  font-size: 1rem;
}

.error-text {
  color: #ef4444;
  margin-top: 0.75rem;
  font-size: 0.875rem;
  text-align: center;
}

.auth-footer {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.auth-footer a {
  color: var(--accent-color);
  font-weight: 700;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
