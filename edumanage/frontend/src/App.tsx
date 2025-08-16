import { Routes, Route, Link, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import StudentsPage from './pages/StudentsPage'
import TeachersPage from './pages/TeachersPage'
import FeesPage from './pages/FeesPage'
import AttendancePage from './pages/AttendancePage'
import { AuthProvider, useAuth } from './context/AuthContext'

function PrivateRoute({ children }: { children: JSX.Element }) {
  const { token } = useAuth()
  return token ? children : <Navigate to="/login" />
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <nav className="bg-white shadow px-4 py-3 flex gap-4">
          <Link to="/" className="font-semibold">EduManage</Link>
          <Link to="/students">Students</Link>
          <Link to="/teachers">Teachers</Link>
          <Link to="/fees">Fees</Link>
          <Link to="/attendance">Attendance</Link>
        </nav>
        <main className="p-4">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
            <Route path="/students" element={<PrivateRoute><StudentsPage /></PrivateRoute>} />
            <Route path="/teachers" element={<PrivateRoute><TeachersPage /></PrivateRoute>} />
            <Route path="/fees" element={<PrivateRoute><FeesPage /></PrivateRoute>} />
            <Route path="/attendance" element={<PrivateRoute><AttendancePage /></PrivateRoute>} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  )
}