import React, { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../services/api'

type User = {
  id: number
  email: string
  first_name: string
  last_name: string
  role: 'admin' | 'teacher' | 'parent' | 'student'
}

type AuthContextType = {
  token: string | null
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    if (token) {
      api.setToken(token)
      api.get('/auth/me').then(res => setUser(res.data.user)).catch(() => setUser(null))
    }
  }, [token])

  const login = async (email: string, password: string) => {
    const res = await api.post('/auth/login', { email, password })
    const t = res.data.access_token
    setToken(t)
    localStorage.setItem('token', t)
    api.setToken(t)
    setUser(res.data.user)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    api.setToken(null)
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}