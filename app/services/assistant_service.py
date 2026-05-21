import httpx
from app.config import settings

class AssistantService:
    @staticmethod
    async def chat_deepseek(message: str, model: str = "deepseek-chat") -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.deepseek.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {settings.deepseek.api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": message}],
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return {"content": content, "model": model}

    @staticmethod
    async def chat_qwen(message: str, system_prompt: str | None = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.qwen.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {settings.qwen.api_key}"},
                json={"model": "qwen-plus", "messages": messages},
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return {"content": content}
