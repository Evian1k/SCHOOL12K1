### Payments (M-Pesa STK Push) Example

- Enter `Student ID`, `Phone` (format 2547XXXXXXXX), and `Amount` on the Fees page.
- Click "Pay (STK)" to call `POST /api/payments/stk-push`.
- Backend calls Daraja, returns `MerchantRequestID` and `CheckoutRequestID` and stores a `payments` row.
- When Safaricom posts to `/api/payments/callback`, the backend updates the `payments` row and increments the student's latest `fee_records.amount_paid` and status.
- Refresh the Fees page to see updated status.