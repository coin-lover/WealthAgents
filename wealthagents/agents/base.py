"""Base agent class for WealthAgents.

Provides common infrastructure for all wealth agents, including
structured output generation and error handling.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel

from wealthagents.llm import MiniMaxLLM, extract_json

T = TypeVar("T", bound=BaseModel)


class BaseWealthAgent(ABC):
    """Base class for all wealth evaluation agents.
    
    Each agent is responsible for one slice of the wealth evaluation
    and produces a structured Pydantic output.
    """
    
    def __init__(
        self,
        name: str,
        model_config: Optional[Dict[str, Any]] = None,
        llm: Optional[MiniMaxLLM] = None,
    ):
        self.name = name
        self.model_config = model_config or {}
        self.llm = llm
        
    @abstractmethod
    def run(self, state) -> BaseModel:
        """Execute the agent's analysis.
        
        Args:
            state: The current WealthState
            
        Returns:
            Structured output model specific to this agent
        """
        pass
    
    def _build_context(self, state) -> str:
        """Build a rich text context from the wealth state for LLM prompting.
        
        This is a shared utility for all agents to format state into
        a consistent context string.
        """
        profile = state.user_profile
        
        context = f"""=== USER FINANCIAL PROFILE ===
User ID: {profile.user_id}
Age: {profile.age}
Household: {profile.household_size} (Dependents: {profile.dependents})
Location: {profile.location or 'Not specified'}

EMPLOYMENT:
- Status: {profile.employment_status}
- Annual Gross Income: ${profile.annual_gross_income:,.2f}
- Monthly Net Income: ${profile.monthly_net_income or 'Not specified'}
- Industry: {profile.industry or 'Not specified'}
- Years in Role: {profile.years_in_current_role or 'Not specified'}
- Income Stability: {profile.income_stability}

CASH FLOW:
- Monthly Expenses: ${profile.monthly_expenses:,.2f}
- Current Monthly Savings: ${profile.current_monthly_savings or 'Not specified'}
- Emergency Fund: {profile.current_emergency_fund_months or 'Not specified'} months

ASSETS ({len(profile.assets)} items):
"""
        for asset in profile.assets:
            context += f"- {asset.name} ({asset.asset_type.value}): ${asset.value:,.2f}\n"
            
        context += f"\nLIABILITIES ({len(profile.liabilities)} items):\n"
        for debt in profile.liabilities:
            context += f"- {debt.name} ({debt.debt_type.value}): ${debt.balance:,.2f} @ {debt.interest_rate:.1%}, min ${debt.minimum_payment:,.2f}/mo\n"
        
        context += f"\nGOALS ({len(profile.goals)} items):\n"
        for goal in profile.goals:
            timeline = goal.target_date.strftime("%Y-%m") if goal.target_date else f"{goal.timeline_months} months"
            context += f"- {goal.name} ({goal.category.value}, {goal.priority.value}): ${goal.current_amount:,.0f}/${goal.target_amount:,.0f} by {timeline}\n"
        
        context += f"""
RISK PROFILE:
- Stated Tolerance: {profile.stated_risk_tolerance.value}
- Investment Experience: {profile.investment_experience}
- Previous Market Reaction: {profile.previous_market_reaction or 'Not specified'}
"""
        return context

    # ─── LLM helpers (TradingAgents-style: tools compute, LLM reasons) ───

    def _llm_available(self) -> bool:
        """True when an LLM client is configured and reachable."""
        return self.llm is not None and self.llm.is_available()

    def _llm_json(self, system_prompt: str, user_message: str) -> Optional[dict]:
        """Ask the LLM for a JSON object and return it parsed.

        Returns None when the LLM is unavailable or the reply is not
        valid JSON, so callers can fall back to heuristic output.
        """
        if not self._llm_available():
            return None
        return extract_json(self.llm.chat(system_prompt, user_message))

    def _enhance_qualitative(self, state, result: T, fields: List[str], role: str) -> T:
        """Ask the LLM to improve qualitative fields of a heuristic result.

        Numeric/scored fields are always kept from the heuristic pass
        (deterministic math); the LLM rewrites the qualitative ones
        (theses, risks, recommendations) with user-specific reasoning.
        Falls back to the heuristic result on any failure.
        """
        if not self._llm_available():
            return result

        metrics = result.model_dump()
        system_prompt = (
            f"You are the {self.name} in a multi-agent personal wealth "
            f"framework, modeled on trading-desk research teams. {role}\n\n"
            "Reply with ONLY a JSON object containing the requested fields. "
            "No markdown, no commentary."
        )
        user_message = (
            f"{self._build_context(state)}\n\n"
            f"HEURISTIC ANALYSIS (numeric metrics are authoritative, do not change them):\n"
            f"{metrics}\n\n"
            f"Rewrite ONLY these fields to be specific, insightful, and tailored "
            f"to this user (same JSON types, 3-6 items for lists): {', '.join(fields)}"
        )

        data = self._llm_json(system_prompt, user_message)
        if not data:
            return result

        update = {}
        for f in fields:
            value = data.get(f)
            if value is not None and isinstance(value, type(getattr(result, f))):
                update[f] = value
        return result.model_copy(update=update) if update else result
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
