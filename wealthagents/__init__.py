"""WealthAgents: Multi-Agent Personal Wealth Framework."""

from wealthagents.core import WealthAgents
from wealthagents.state import WealthState, UserProfile
from wealthagents.mentors.registry import MentorRegistry
from wealthagents.connections import (
    is_plaid_supported,
    get_connection_mode,
    get_supported_countries,
    AccountConnectionManager,
)
from wealthagents.manual_input import ManualInputGuide, get_manual_input_guide
from wealthagents.llm import LLMClient, MiniMaxLLM, get_llm, list_providers

__all__ = [
    "WealthAgents",
    "WealthState",
    "UserProfile",
    "MentorRegistry",
    "is_plaid_supported",
    "get_connection_mode",
    "get_supported_countries",
    "AccountConnectionManager",
    "ManualInputGuide",
    "get_manual_input_guide",
    "MiniMaxLLM",
    "LLMClient",
    "get_llm",
    "list_providers",
]
__version__ = "0.1.0"
