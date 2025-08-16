import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function AttendancePage() {
  const [studentId, setStudentId] = useState<string>('')
  const [records, setRecords] = useState<any[]>([])
  const [message, setMessage] = useState<string | null>(null)

  const load = async () => {
    if (!studentId) return
    const res = await api.get(`/attendance/student/${studentId}`)
    setRecords(res.data.records)
  }

  const checkIn = async () => {
    setMessage(null)
    await api.post('/attendance/check-in', { student_id: Number(studentId) })
    setMessage('Checked in')
    await load()
  }

  const checkOut = async () => {
    setMessage(null)
    await api.post('/attendance/check-out', { student_id: Number(studentId) })
    setMessage('Checked out')
    await load()
  }

  useEffect(() => { if (studentId) load() }, [studentId])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Attendance</h1>

      <div className="bg-white shadow rounded p-4 space-y-3">
        <div className="flex gap-2">
          <input className="border px-3 py-2 rounded" placeholder="Student ID" value={studentId} onChange={e => setStudentId(e.target.value)} />
          <button className="bg-blue-600 text-white px-3 py-2 rounded" onClick={load}>Load</button>
          <button className="bg-green-600 text-white px-3 py-2 rounded" onClick={checkIn}>Check In</button>
          <button className="bg-yellow-600 text-white px-3 py-2 rounded" onClick={checkOut}>Check Out</button>
        </div>
        {message && <div className="text-sm">{message}</div>}
      </div>

      <div className="bg-white shadow rounded">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-2">Date</th>
              <th className="text-left p-2">Check In</th>
              <th className="text-left p-2">Check Out</th>
              <th className="text-left p-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {records.map(r => (
              <tr key={r.id} className="border-t">
                <td className="p-2">{r.date}</td>
                <td className="p-2">{r.check_in || '-'}</td>
                <td className="p-2">{r.check_out || '-'}</td>
                <td className="p-2">{r.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}