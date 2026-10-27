"""Base agent class for WealthAgents.

Provides common infrastructure for all wealth agents, including
structured output generation and error handling.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseWealthAgent(ABC):
    """Base class for all wealth evaluation agents.
    
    Each agent is responsible for one slice of the wealth evaluation
    and produces a structured Pydantic output.
    """
    
    def __init__(self, name: str, model_config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.model_config = model_config or {}
        
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
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
