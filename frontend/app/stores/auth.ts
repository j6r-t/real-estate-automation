import { defineStore } from 'pinia'

type Role = 'client' | 'sub_agent' | 'head_agent' | 'admin'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as { name: string; email: string; role: Role; id?: number; agency_id?: number } | null,
        token: null as string | null,
        isAuthenticated: false
    }),
    actions: {
        async login(email: string, password: string) {
            try {
                const data = await $fetch<{ access_token: string; token_type: string; role: Role }>('http://localhost:8000/token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                })
                this.token = data.access_token
                this.user = { name: email.split('@')[0], email, role: data.role }
                this.isAuthenticated = true

                if (typeof window !== 'undefined') {
                    localStorage.setItem('user_session', JSON.stringify(this.user))
                    localStorage.setItem('auth_token', data.access_token)
                }
            } catch (error) {
                throw error
            }
        },
        async register(email: string, password: string, fullName: string, phone: string) {
            try {
                await $fetch('http://localhost:8000/users/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, full_name: fullName, phone, role: 'client' })
                })
                await this.login(email, password)
            } catch (error) {
                throw error
            }
        },
        logout() {
            this.user = null
            this.token = null
            this.isAuthenticated = false
            if (typeof window !== 'undefined') {
                localStorage.removeItem('user_session')
                localStorage.removeItem('auth_token')
            }
            window.location.href = '/auth/login'
        },
        initAuth() {
            if (typeof window !== 'undefined') {
                const session = localStorage.getItem('user_session')
                const token = localStorage.getItem('auth_token')
                if (session) {
                    this.user = JSON.parse(session)
                    this.token = token
                    this.isAuthenticated = true
                }
            }
        },
        getAuthHeader() {
            const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
            return token ? { Authorization: `Bearer ${token}` } : {}
        }
    }
})
