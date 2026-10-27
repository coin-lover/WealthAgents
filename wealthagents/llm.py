"""LLM provider registry for WealthAgents.

Follows the TradingAgents provider convention: set one API-key environment
variable and the framework auto-detects the provider:

    export OPENAI_API_KEY=...          # OpenAI (GPT)
    export GOOGLE_API_KEY=...          # Google (Gemini)
    export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
    export XAI_API_KEY=...             # xAI (Grok)
    export DEEPSEEK_API_KEY=...        # DeepSeek
    export DASHSCOPE_API_KEY=...       # Qwen (international)
    export DASHSCOPE_CN_API_KEY=...    # Qwen (China)
    export ZHIPU_API_KEY=...           # GLM via Z.AI (international)
    export ZHIPU_CN_API_KEY=...        # GLM via BigModel (China)
    export MINIMAX_API_KEY=...         # MiniMax (global)
    export MINIMAX_CN_API_KEY=...      # MiniMax (China)
    export OPENROUTER_API_KEY=...      # OpenRouter
    export MISTRAL_API_KEY=...         # Mistral
    export MOONSHOT_API_KEY=...        # Kimi (Moonshot)
    export GROQ_API_KEY=...            # Groq
    export NVIDIA_API_KEY=...          # NVIDIA NIM

Usage:
    from wealthagents.llm import get_llm

    llm = get_llm()                    # auto-detect from environment
    llm = get_llm("deepseek")          # explicit provider
    llm = get_llm("openai", model="gpt-4o")

The framework works fully without an LLM (heuristic mode) — an LLM only
enhances outputs. Providers marked sdk="openai" speak the OpenAI chat API
(includes every provider with an OpenAI-compatible endpoint); Anthropic
uses its native SDK. Both client packages are optional and imported lazily.

Optional dependency:
    pip install "wealthagents[llm]"    # installs openai + anthropic clients
"""

import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000


@dataclass(frozen=True)
class Provider:
    """Static connection details for one LLM provider."""

    name: str
    env_var: str                      # API-key environment variable
    default_model: str
    base_url: Optional[str] = None    # None = provider SDK default (OpenAI)
    sdk: str = "openai"               # "openai" (OpenAI-compatible) or "anthropic"
    headers: Dict[str, str] = field(default_factory=dict)


# Order matters: get_llm() auto-detects the first provider with a key set.
PROVIDERS: Dict[str, Provider] = {
    p.name: p
    for p in [
        Provider("openai", "OPENAI_API_KEY", "gpt-4o-mini"),
        Provider("google", "GOOGLE_API_KEY", "gemini-2.5-flash",
                 base_url="https://generativelanguage.googleapis.com/v1beta/openai/"),
        Provider("anthropic", "ANTHROPIC_API_KEY", "claude-sonnet-4-5", sdk="anthropic"),
        Provider("xai", "XAI_API_KEY", "grok-4",
                 base_url="https://api.x.ai/v1"),
        Provider("deepseek", "DEEPSEEK_API_KEY", "deepseek-chat",
                 base_url="https://api.deepseek.com/v1"),
        Provider("qwen", "DASHSCOPE_API_KEY", "qwen-plus",
                 base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
        Provider("qwen_cn", "DASHSCOPE_CN_API_KEY", "qwen-plus",
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"),
        Provider("zhipu", "ZHIPU_API_KEY", "glm-4.5",
                 base_url="https://api.z.ai/api/paas/v4"),
        Provider("zhipu_cn", "ZHIPU_CN_API_KEY", "glm-4.5",
                 base_url="https://open.bigmodel.cn/api/paas/v4"),
        Provider("minimax", "MINIMAX_API_KEY", "MiniMax-M2",
                 base_url="https://api.minimax.io/v1"),
        Provider("minimax_cn", "MINIMAX_CN_API_KEY", "MiniMax-M2",
                 base_url="https://api.minimaxi.com/v1"),
        Provider("openrouter", "OPENROUTER_API_KEY", "openai/gpt-4o-mini",
                 base_url="https://openrouter.ai/api/v1"),
        Provider("mistral", "MISTRAL_API_KEY", "mistral-large-latest",
                 base_url="https://api.mistral.ai/v1"),
        Provider("moonshot", "MOONSHOT_API_KEY", "moonshot-v1-8k",
                 base_url="https://api.moonshot.ai/v1"),
        Provider("groq", "GROQ_API_KEY", "llama-3.3-70b-versatile",
                 base_url="https://api.groq.com/openai/v1"),
        Provider("nvidia", "NVIDIA_API_KEY", "nvidia/llama-3.3-70b-instruct",
                 base_url="https://integrate.api.nvidia.com/v1"),
    ]
}


def list_providers() -> List[dict]:
    """List all registered providers with their env var and default model."""
    return [
        {"name": p.name, "env_var": p.env_var, "default_model": p.default_model}
        for p in PROVIDERS.values()
    ]


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


class LLMClient:
    """Unified chat client over the provider registry.

    OpenAI-compatible providers use the `openai` package; Anthropic uses
    its native SDK. Both are optional dependencies, imported lazily, so
    the rest of the framework keeps working when they are not installed.
    """

    def __init__(
        self,
        provider: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ):
        if provider not in PROVIDERS:
            available = ", ".join(sorted(PROVIDERS))
            raise ValueError(f"Unknown provider '{provider}'. Available: {available}")
        self.provider = PROVIDERS[provider]
        self.api_key = api_key or os.environ.get(self.provider.env_var)
        self.model = model or self.provider.default_model
        self.base_url = base_url or self.provider.base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    def is_available(self) -> bool:
        """True when the required SDK is installed and an API key is set."""
        return self._get_client() is not None

    def _get_client(self):
        if self._client is not None:
            return self._client
        if not self.api_key:
            return None
        try:
            if self.provider.sdk == "anthropic":
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key)
            else:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,  # None = api.openai.com default
                    default_headers=self.provider.headers or None,
                )
        except ImportError:
            return None
        return self._client

    def chat(self, system_prompt: str, user_message: str) -> Optional[str]:
        """Send a chat request. Returns the reply text, or None when the
        LLM is unavailable or the request fails (callers fall back to
        heuristic output).
        """
        client = self._get_client()
        if client is None:
            return None
        try:
            if self.provider.sdk == "anthropic":
                response = client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}],
                )
                return "".join(
                    block.text for block in response.content
                    if getattr(block, "type", None) == "text"
                ) or None

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except Exception:
            # Network/auth errors degrade gracefully to heuristic output
            return None

        choice = response.choices[0] if response.choices else None
        return choice.message.content if choice else None

    def __repr__(self) -> str:
        state = "ready" if self.is_available() else f"unavailable (set {self.provider.env_var})"
        return f"LLMClient(provider={self.provider.name}, model={self.model}, {state})"


class MiniMaxLLM(LLMClient):
    """Backward-compatible alias defaulting to the MiniMax provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None,
                 base_url: Optional[str] = None, **kwargs):
        super().__init__(
            provider="minimax_cn" if os.environ.get("MINIMAX_CN_API_KEY") else "minimax",
            api_key=api_key,
            model=model,
            base_url=base_url,
            **kwargs,
        )


def get_llm(provider: Optional[str] = None, model: Optional[str] = None,
            **kwargs) -> Optional[LLMClient]:
    """Create an LLM client.

    Args:
        provider: Provider name from list_providers(). When None, the first
                  provider with its API-key environment variable set is used.
        model:    Override the provider's default model.
        **kwargs: Passed to LLMClient (temperature, max_tokens, ...).

    Returns:
        An LLMClient, or None when no provider key is set in the environment.
    """
    if provider is not None:
        return LLMClient(provider, model=model, **kwargs)

    for p in PROVIDERS.values():
        if os.environ.get(p.env_var):
            return LLMClient(p.name, model=model, **kwargs)
    return None
