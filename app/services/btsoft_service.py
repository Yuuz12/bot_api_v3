import hashlib
import time
import httpx
from app.config import settings


class BtSoftService:
    @staticmethod
    def _get_key_data() -> dict:
        now = int(time.time())
        request_token = hashlib.md5(f"{now}{hashlib.md5(settings.bt_panel.key.encode()).hexdigest()}".encode()).hexdigest()
        return {"request_token": request_token, "request_time": now}

    @staticmethod
    async def get_system_info() -> dict:
        url = f"{settings.bt_panel.url}/system?action=GetSystemTotal"
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.post(url, data=BtSoftService._get_key_data())
            return response.json()

    @staticmethod
    async def re_memory() -> dict:
        url = f"{settings.bt_panel.url}/system?action=ReMemory"
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.post(url, data=BtSoftService._get_key_data())
            return response.json()
