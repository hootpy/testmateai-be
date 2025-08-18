from __future__ import annotations

from typing import Protocol

from openai import AsyncOpenAI

from app.core.config import SETTINGS


class LLMProvider(Protocol):
    async def generate_text(self, prompt: str) -> str:  # pragma: no cover - interface
        ...


class FakeLLMProvider:
    async def generate_text(self, prompt: str) -> str:
        return f"Echo: {prompt}"  # Deterministic placeholder so the API works without external keys


class OpenAILLMProvider:
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def generate_text(self, prompt: str) -> str:
        # Use the Responses API for a simple text output
        resp = await self._client.responses.create(model=self._model, input=prompt)
        # Extract first text segment
        for item in resp.output or []:
            if getattr(item, "type", None) == "output_text":
                return getattr(item, "text", "")
        # Fallback for older SDKs / different structures
        try:
            return resp.output_text  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover - defensive
            return ""


def get_llm_provider() -> LLMProvider:
    provider_name = SETTINGS.LLM_PROVIDER.lower()

    if provider_name == "openai":
        api_key = SETTINGS.OPENAI_API_KEY
        if api_key:
            try:
                return OpenAILLMProvider(api_key, SETTINGS.OPENAI_MODEL)
            except Exception:
                # If OpenAI SDK is not installed or fails to initialize, fall back to fake
                return FakeLLMProvider()
        return FakeLLMProvider()

    # Default: a deterministic fake provider so the system runs without external dependencies
    return FakeLLMProvider()
