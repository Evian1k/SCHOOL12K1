import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function TeachersPage() {
  const [teachers, setTeachers] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const fetchTeachers = async () => {
    try {
      const res = await api.get('/teachers')
      setTeachers(res.data.teachers)
    } catch (err: any) {
      setError(err?.response?.data?.message || 'Failed to load')
    }
  }

  useEffect(() => { fetchTeachers() }, [])

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Teachers</h1>
        <button className="bg-blue-600 text-white px-3 py-1 rounded" onClick={fetchTeachers}>Refresh</button>
      </div>
      {error && <div className="text-red-600">{error}</div>}
      <div className="bg-white shadow rounded">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-2">ID</th>
              <th className="text-left p-2">Name</th>
              <th className="text-left p-2">Staff No.</th>
            </tr>
          </thead>
          <tbody>
            {teachers.map(t => (
              <tr key={t.id} className="border-t">
                <td className="p-2">{t.id}</td>
                <td className="p-2">{t.user?.first_name} {t.user?.last_name}</td>
                <td className="p-2">{t.staff_number || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}