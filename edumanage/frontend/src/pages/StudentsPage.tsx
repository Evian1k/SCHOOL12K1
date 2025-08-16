import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function StudentsPage() {
  const [students, setStudents] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const fetchStudents = async () => {
    try {
      const res = await api.get('/students')
      setStudents(res.data.students)
    } catch (err: any) {
      setError(err?.response?.data?.message || 'Failed to load')
    }
  }

  useEffect(() => { fetchStudents() }, [])

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Students</h1>
        <button className="bg-blue-600 text-white px-3 py-1 rounded" onClick={fetchStudents}>Refresh</button>
      </div>
      {error && <div className="text-red-600">{error}</div>}
      <div className="bg-white shadow rounded">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-2">ID</th>
              <th className="text-left p-2">Name</th>
              <th className="text-left p-2">Admission</th>
              <th className="text-left p-2">Class</th>
            </tr>
          </thead>
          <tbody>
            {students.map(s => (
              <tr key={s.id} className="border-t">
                <td className="p-2">{s.id}</td>
                <td className="p-2">{s.user?.first_name} {s.user?.last_name}</td>
                <td className="p-2">{s.admission_number || '-'}</td>
                <td className="p-2">{s.classroom?.name || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}