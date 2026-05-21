import httpx
from app.config import settings


class OsuService:
    @staticmethod
    async def get_user_data(username: str, mode: str = "osu") -> dict | None:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://osu.ppy.sh/api/get_user",
                params={"k": settings.osu.api_key, "u": username, "m": _mode_to_int(mode)},
            )
            data = response.json()
            if not data:
                return None
            return data[0]

    @staticmethod
    async def get_scoreboard(username: str, mode: str = "osu") -> dict:
        user_data = await OsuService.get_user_data(username, mode)
        if not user_data:
            return {"error": "User not found"}
        return {"user": user_data, "mode": mode, "type": "scoreboard"}

    @staticmethod
    async def get_signature(username: str, mode: str = "osu") -> dict:
        user_data = await OsuService.get_user_data(username, mode)
        if not user_data:
            return {"error": "User not found"}
        return {"user": user_data, "mode": mode, "type": "signature"}


def _mode_to_int(mode: str) -> int:
    return {"osu": 0, "taiko": 1, "ctb": 2, "mania": 3}.get(mode, 0)
