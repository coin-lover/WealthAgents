"""WealthAgents agent definitions."""

from wealthagents.agents.analysts import (
    IncomeAnalyst,
    ExpenseAnalyst,
    AssetLiabilityAnalyst,
    GoalAnalyst,
    RiskProfileAnalyst,
)
from wealthagents.agents.researchers import (
    OptimisticResearcher,
    CautiousResearcher,
)
from wealthagents.agents.planning import (
    Strategist,
    RiskManager,
    TaxEfficiencyAnalyst,
)
from wealthagents.agents.base import BaseWealthAgent

__all__ = [
    "BaseWealthAgent",
    "IncomeAnalyst",
    "ExpenseAnalyst",
    "AssetLiabilityAnalyst",
    "GoalAnalyst",
    "RiskProfileAnalyst",
    "OptimisticResearcher",
    "CautiousResearcher",
    "Strategist",
    "RiskManager",
    "TaxEfficiencyAnalyst",
]
