from flask import current_app


class NotificationService:
    def __init__(self):
        self.enabled = current_app.config.get("NOTIFICATIONS_ENABLED", True)

    def send_sms(self, phone: str, message: str) -> None:
        if not self.enabled:
            return
        # TODO: Integrate with SMS provider like Twilio/AfricasTalking/Infobip
        current_app.logger.info(f"[SMS] to={phone} message={message}")

    def send_whatsapp(self, phone: str, message: str) -> None:
        if not self.enabled:
            return
        # TODO: Integrate with WhatsApp provider
        current_app.logger.info(f"[WhatsApp] to={phone} message={message}")