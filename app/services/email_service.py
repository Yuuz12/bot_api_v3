import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailService:
    @staticmethod
    def _get_smtp_config(sender: str):
        if sender == "shiruku":
            return settings.smtp_shiruku
        return settings.smtp_kirino

    @staticmethod
    async def send_email(to: str, subject: str, body: str, sender: str = "kirino") -> dict:
        config = EmailService._get_smtp_config(sender)

        msg = MIMEMultipart()
        msg["From"] = f"{config.display_name} <{config.email}>"
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        await aiosmtplib.send(
            msg,
            hostname=config.host,
            port=config.port,
            username=config.email,
            password=config.password,
            use_tls=True,
        )
        return {"to": to, "subject": subject, "sender": sender, "status": "sent"}
