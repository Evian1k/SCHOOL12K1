import base64
import datetime
import requests
from typing import Optional, Tuple
from flask import current_app


class DarajaService:
    def __init__(self):
        self.base_url = current_app.config["DARAJA_BASE_URL"].rstrip("/")
        self.consumer_key = current_app.config["DARAJA_CONSUMER_KEY"]
        self.consumer_secret = current_app.config["DARAJA_CONSUMER_SECRET"]
        self.short_code = current_app.config["DARAJA_SHORT_CODE"]
        self.passkey = current_app.config["DARAJA_PASSKEY"]
        self.callback_url = current_app.config["DARAJA_CALLBACK_URL"]

    def _get_access_token(self) -> str:
        resp = requests.get(
            f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
            auth=(self.consumer_key, self.consumer_secret),
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    def initiate_stk_push(self, amount: float, phone_number: str, account_reference: str, description: str) -> dict:
        token = self._get_access_token()
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        payload = f"{self.short_code}{self.passkey}{timestamp}".encode()
        password = base64.b64encode(payload).decode()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        body = {
            "BusinessShortCode": self.short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": description,
        }
        resp = requests.post(f"{self.base_url}/mpesa/stkpush/v1/processrequest", json=body, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def parse_callback(data: dict) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[int], str]:
        result_code = None
        result_desc = None
        merchant_request_id = None
        checkout_request_id = None
        mpesa_receipt = None

        stk_callback = data.get("Body", {}).get("stkCallback", {})
        result_code = stk_callback.get("ResultCode")
        result_desc = stk_callback.get("ResultDesc")
        merchant_request_id = stk_callback.get("MerchantRequestID")
        checkout_request_id = stk_callback.get("CheckoutRequestID")

        callback_metadata = stk_callback.get("CallbackMetadata", {})
        if callback_metadata:
            for item in callback_metadata.get("Item", []):
                if item.get("Name") == "MpesaReceiptNumber":
                    mpesa_receipt = item.get("Value")

        return merchant_request_id, checkout_request_id, mpesa_receipt, result_desc, result_code, "success" if result_code == 0 or result_code == "0" else "failed"