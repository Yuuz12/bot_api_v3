import httpx
from typing import Any

_http_client: httpx.AsyncClient | None = None


async def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
    return _http_client


async def close_http_client() -> None:
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        _http_client = None


async def async_get(url: str, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None) -> Any:
    client = await get_http_client()
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


async def async_get_raw(url: str, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None) -> bytes:
    client = await get_http_client()
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.content


async def async_post(url: str, data: dict[str, Any] | None = None, json: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> Any:
    client = await get_http_client()
    response = await client.post(url, data=data, json=json, headers=headers)
    response.raise_for_status()
    return response.json()


async def async_post_raw(url: str, data: dict[str, Any] | None = None, json: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> bytes:
    client = await get_http_client()
    response = await client.post(url, data=data, json=json, headers=headers)
    response.raise_for_status()
    return response.content
