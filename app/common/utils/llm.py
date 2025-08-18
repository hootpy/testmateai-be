from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import Settings


async def generate_text_response(
    settings: Settings,
    user_prompt: str,
    system_prompt: str | None = None,
) -> dict[str, Any]:
    if not settings.LLM_API_URL or not settings.LLM_API_KEY:
        raise RuntimeError("LLM API URL or API KEY is not configured")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LLM_API_KEY}",
        "User-Agent": "Enlight/1.4 (com.lightricks.Apollo; build:123; iOS 18.5.0) Alamofire/5.8.0",
    }

    sys_prompt = system_prompt if system_prompt is not None else "You are a helpful assistant."

    payload: dict[str, Any] = {
        "temperature": 0,
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": sys_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
        ],
        "model": settings.LLM_MODEL,
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(settings.LLM_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    # Try to parse out a JSON string from choices[0].message.content
    try:
        raw_content = data["choices"][0]["message"]["content"]
        if isinstance(raw_content, str):
            return json.loads(raw_content)
        # If already a JSON object
        return raw_content
    except Exception:
        # Fallback: return entire response in a wrapper
        return {"raw": data}
