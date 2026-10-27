"""LLM integration for WealthAgents.

Currently supports MiniMax via its OpenAI-compatible API.

Setup:
    pip install "wealthagents[llm]"     # installs the openai client
    export MINIMAX_API_KEY="your-key-here"

Optional environment variables:
    MINIMAX_MODEL      default: "MiniMax-M2"
    MINIMAX_BASE_URL   default: "https://api.minimaxi.com/v1" (international)
                       China endpoint: "https://api.minimax.chat/v1"

The framework works fully without an LLM (heuristic mode) — the LLM
only enhances outputs, most notably the mentor's voice narrative.
"""

import json
import os
import re
from typing import List, Optional


DEFAULT_BASE_URL = "https://api.minimaxi.com/v1"
DEFAULT_MODEL = "MiniMax-M2"


def extract_json(text: Optional[str]) -> Optional[dict]:
    """Extract the first JSON object from an LLM reply, tolerating prose
    and markdown code fences. Returns None when no valid object is found.
    """
    if not text:
        return None
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


class MiniMaxLLM:
    """Thin wrapper around MiniMax's OpenAI-compatible chat API.

    The `openai` Python package is imported lazily so the rest of the
    framework keeps working when it (or an API key) is not installed.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.model = model or os.environ.get("MINIMAX_MODEL", DEFAULT_MODEL)
        self.base_url = base_url or os.environ.get("MINIMAX_BASE_URL", DEFAULT_BASE_URL)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    def is_available(self) -> bool:
        """True when the openai package is installed and an API key is set."""
        return self._get_client() is not None

    def _get_client(self):
        if self._client is not None:
            return self._client
        if not self.api_key:
            return None
        try:
            from openai import OpenAI
        except ImportError:
            return None
        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client

    def chat(self, system_prompt: str, user_message: str) -> Optional[str]:
        """Send a chat completion request to MiniMax.

        Returns the assistant's reply text, or None if the LLM is not
        available (missing package/key) so callers can fall back to
        heuristic output.
        """
        client = self._get_client()
        if client is None:
            return None

        messages: List[dict] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except Exception:
            # Network/auth errors degrade gracefully to heuristic output
            return None

        choice = response.choices[0] if response.choices else None
        return choice.message.content if choice else None

    def __repr__(self) -> str:
        state = "ready" if self.is_available() else "unavailable (set MINIMAX_API_KEY and pip install openai)"
        return f"MiniMaxLLM(model={self.model}, base_url={self.base_url}, {state})"
