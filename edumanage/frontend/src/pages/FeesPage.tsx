import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function FeesPage() {
  const [studentId, setStudentId] = useState<string>('')
  const [phone, setPhone] = useState<string>('')
  const [amount, setAmount] = useState<string>('')
  const [records, setRecords] = useState<any[]>([])
  const [message, setMessage] = useState<string | null>(null)

  const loadFees = async () => {
    if (!studentId) return
    const res = await api.get(`/fees/student/${studentId}`)
    setRecords(res.data.fee_records)
  }

  const initiatePayment = async () => {
    setMessage(null)
    try {
      const res = await api.post('/payments/stk-push', {
        student_id: Number(studentId),
        phone_number: phone,
        amount: Number(amount),
      })
      setMessage('STK push initiated. Check your phone to complete payment.')
      await loadFees()
    } catch (err: any) {
      setMessage(err?.response?.data?.message || 'Failed to initiate payment')
    }
  }

  useEffect(() => { if (studentId) loadFees() }, [studentId])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Fees</h1>

      <div className="bg-white shadow rounded p-4 space-y-3">
        <div className="flex gap-2">
          <input className="border px-3 py-2 rounded" placeholder="Student ID" value={studentId} onChange={e => setStudentId(e.target.value)} />
          <button className="bg-blue-600 text-white px-3 py-2 rounded" onClick={loadFees}>Load</button>
        </div>
        <div className="flex gap-2">
          <input className="border px-3 py-2 rounded" placeholder="Phone (2547...)" value={phone} onChange={e => setPhone(e.target.value)} />
          <input className="border px-3 py-2 rounded" placeholder="Amount" value={amount} onChange={e => setAmount(e.target.value)} />
          <button className="bg-green-600 text-white px-3 py-2 rounded" onClick={initiatePayment}>Pay (STK)</button>
        </div>
        {message && <div className="text-sm">{message}</div>}
      </div>

      <div className="bg-white shadow rounded">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-2">Term</th>
              <th className="text-left p-2">Amount Due</th>
              <th className="text-left p-2">Amount Paid</th>
              <th className="text-left p-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {records.map(r => (
              <tr key={r.id} className="border-t">
                <td className="p-2">{r.term}</td>
                <td className="p-2">{r.amount_due}</td>
                <td className="p-2">{r.amount_paid}</td>
                <td className="p-2">{r.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}