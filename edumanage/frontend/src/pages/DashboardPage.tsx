import { useAuth } from '../context/AuthContext'

export default function DashboardPage() {
  const { user, logout } = useAuth()
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <button className="bg-gray-800 text-white px-3 py-1 rounded" onClick={logout}>Logout</button>
      </div>
      <div className="bg-white shadow rounded p-4">
        <div><span className="font-medium">User:</span> {user?.first_name} {user?.last_name}</div>
        <div><span className="font-medium">Email:</span> {user?.email}</div>
        <div><span className="font-medium">Role:</span> {user?.role}</div>
      </div>
    </div>
  )
}