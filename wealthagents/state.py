"""State schema for WealthAgents framework.

Defines all data structures that flow through the LangGraph workflow.
Inspired by TradingAgents' structured output approach, adapted for
personal wealth evaluation.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RiskTolerance(str, Enum):
    """Risk tolerance levels."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class GoalPriority(str, Enum):
    """Goal priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GoalCategory(str, Enum):
    """Categories of financial goals."""
    EMERGENCY_FUND = "emergency_fund"
    DEBT_PAYOFF = "debt_payoff"
    HOME_PURCHASE = "home_purchase"
    RETIREMENT = "retirement"
    EDUCATION = "education"
    SHORT_TERM = "short_term"
    OTHER = "other"


class DebtType(str, Enum):
    """Types of debt."""
    CREDIT_CARD = "credit_card"
    STUDENT_LOAN = "student_loan"
    MORTGAGE = "mortgage"
    AUTO_LOAN = "auto_loan"
    PERSONAL_LOAN = "personal_loan"
    OTHER = "other"


class AssetType(str, Enum):
    """Types of assets."""
    CASH = "cash"
    CHECKING = "checking"
    SAVINGS = "savings"
    BROKERAGE = "brokerage"
    RETIREMENT_401K = "retirement_401k"
    RETIREMENT_IRA = "retirement_ira"
    RETIREMENT_ROTH = "retirement_roth"
    REAL_ESTATE = "real_estate"
    CRYPTO = "crypto"
    OTHER = "other"


# ─── User Input Models ───

class Debt(BaseModel):
    """A single debt obligation."""
    name: str = Field(description="Human-readable name for this debt")
    debt_type: DebtType
    balance: float = Field(ge=0, description="Current outstanding balance")
    interest_rate: float = Field(ge=0, le=1, description="Annual interest rate (0.05 = 5%)")
    minimum_payment: float = Field(ge=0, description="Minimum monthly payment")
    original_amount: Optional[float] = Field(default=None, description="Original loan amount")


class Asset(BaseModel):
    """A single asset holding."""
    name: str = Field(description="Human-readable name for this asset")
    asset_type: AssetType
    value: float = Field(ge=0, description="Current market value")
    cost_basis: Optional[float] = Field(default=None, description="Original cost basis")
    annual_return: Optional[float] = Field(default=None, description="Expected annual return")
    liquidity: str = Field(default="high", description="high/medium/low")


class Goal(BaseModel):
    """A financial goal."""
    name: str
    category: GoalCategory
    target_amount: float = Field(ge=0)
    current_amount: float = Field(default=0, ge=0)
    target_date: Optional[datetime] = None
    timeline_months: Optional[int] = Field(default=None, ge=0)
    priority: GoalPriority = GoalPriority.MEDIUM
    notes: Optional[str] = None


class UserProfile(BaseModel):
    """Core user profile for wealth evaluation.
    
    This is the primary input to the WealthAgents system.
    """
    user_id: str = Field(description="Unique user identifier")
    age: int = Field(ge=18, le=120)
    annual_gross_income: float = Field(ge=0, description="Pre-tax annual income")
    monthly_net_income: Optional[float] = Field(default=None, description="After-tax monthly income")
    
    # Employment
    employment_status: str = Field(default="employed", description="employed/self-employed/unemployed/retired")
    industry: Optional[str] = None
    years_in_current_role: Optional[float] = None
    income_stability: Optional[str] = Field(default="stable", description="stable/moderate/unstable")
    
    # Household
    household_size: int = Field(default=1, ge=1)
    dependents: int = Field(default=0, ge=0)
    location: Optional[str] = None  # City/state for cost-of-living context
    location_country: str = Field(default="US", description="ISO 3166-1 alpha-2 country code (e.g., US, GB, DE)")
    currency: str = Field(default="USD", description="ISO 4217 currency code (e.g., USD, EUR, GBP)")
    tax_filing_status: str = Field(default="single", description="single/married/joint/head_of_household")
    
    # Financials
    monthly_expenses: float = Field(ge=0, description="Total average monthly spending")
    expenses_breakdown: Optional[Dict[str, float]] = Field(default=None, description="Category -> amount")
    
    assets: List[Asset] = Field(default_factory=list)
    liabilities: List[Debt] = Field(default_factory=list)
    goals: List[Goal] = Field(default_factory=list)
    
    # Risk & behavior
    stated_risk_tolerance: RiskTolerance = RiskTolerance.MODERATE
    investment_experience: str = Field(default="beginner", description="beginner/intermediate/advanced")
    previous_market_reaction: Optional[str] = Field(default=None, description="How user reacted in 2008/2020/etc")
    
    # Existing plan
    current_emergency_fund_months: Optional[float] = Field(default=None, ge=0)
    current_monthly_savings: Optional[float] = Field(default=None, ge=0)
    existing_insurance: Optional[Dict[str, Any]] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── Analyst Output Models ───

class IncomeAnalysis(BaseModel):
    """Output from the Income Analyst."""
    income_score: float = Field(ge=0, le=100, description="Overall income health score")
    income_stability_rating: str = Field(description="stable/moderate/fragile")
    growth_trajectory: str = Field(description="growing/stagnant/declining")
    human_capital_value: Optional[float] = Field(default=None, description="Estimated lifetime earnings PV")
    key_risks: List[str] = Field(default_factory=list, description="Income-specific risks")
    recommendations: List[str] = Field(default_factory=list)


class ExpenseAnalysis(BaseModel):
    """Output from the Expense & Cashflow Analyst."""
    savings_rate: float = Field(ge=0, le=1, description="Current savings rate as decimal")
    target_savings_rate: float = Field(ge=0, le=1, description="Recommended savings rate")
    fixed_expense_ratio: float = Field(ge=0, le=1, description="Fixed vs variable split")
    cash_flow_health: str = Field(description="healthy/tight/negative")
    discretionary_opportunities: List[str] = Field(default_factory=list)
    burn_rate_months: Optional[float] = Field(default=None, description="Months of runway")
    recommendations: List[str] = Field(default_factory=list)


class AssetAnalysis(BaseModel):
    """Output from the Asset & Liability Analyst."""
    net_worth: float
    liquid_net_worth: float
    asset_allocation: Dict[str, float] = Field(description="Category -> percentage")
    debt_to_income_ratio: Optional[float] = None
    debt_to_asset_ratio: Optional[float] = None
    weighted_interest_rate: Optional[float] = None
    debt_payoff_priority: List[str] = Field(default_factory=list)
    liquidity_score: float = Field(ge=0, le=100)
    recommendations: List[str] = Field(default_factory=list)


class GoalAnalysis(BaseModel):
    """Output from the Goal Analyst."""
    goal_feasibility: Dict[str, str] = Field(description="Goal name -> feasible/stretch/unlikely")
    funding_gaps: Dict[str, float] = Field(description="Goal name -> monthly shortfall")
    prioritized_goals: List[str] = Field(description="Ordered goal names")
    timeline_conflicts: List[str] = Field(default_factory=list)
    recommended_order: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class RiskAnalysis(BaseModel):
    """Output from the Risk Profile Analyst."""
    risk_capacity_score: float = Field(ge=0, le=100)
    risk_willingness_score: float = Field(ge=0, le=100)
    risk_alignment: str = Field(description="aligned/misaligned-capacity-higher/misaligned-willingness-higher")
    key_stress_events: List[str] = Field(default_factory=list)
    insurance_gaps: List[str] = Field(default_factory=list)
    emergency_fund_recommendation_months: float = Field(ge=0)
    recommendations: List[str] = Field(default_factory=list)


# ─── Debate Models ───

class ResearchView(BaseModel):
    """A researcher's perspective on the wealth plan."""
    perspective: str = Field(description="optimistic/cautious")
    thesis: str = Field(description="Core argument")
    key_points: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class DebateResult(BaseModel):
    """Result of the researcher debate."""
    optimistic_view: ResearchView
    cautious_view: ResearchView
    synthesis: str = Field(description="Synthesized conclusion from debate")
    key_risks_to_monitor: List[str] = Field(default_factory=list)


# ─── Planning Models ───

class ActionItem(BaseModel):
    """A concrete action in the wealth plan."""
    action: str
    priority: int = Field(ge=1, le=10)
    category: str = Field(description="emergency/debt/invest/tax/insurance/goal")
    timeline: str = Field(description="immediate/1_month/3_month/6_month/1_year/ongoing")
    estimated_impact: Optional[str] = None
    rationale: Optional[str] = None


class WealthStrategy(BaseModel):
    """The core wealth strategy."""
    emergency_fund_target: float
    emergency_fund_months: float
    debt_strategy: str = Field(description="avalanche/snowball/consolidation/hybrid")
    monthly_debt_payment: float
    monthly_investment: float
    recommended_allocation: Dict[str, float] = Field(description="Asset class -> percentage")
    account_funding_order: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    strategy_summary: str


class RiskAssessment(BaseModel):
    """Risk manager's stress test results."""
    base_case_projection: Optional[Dict[str, Any]] = None
    bear_case_projection: Optional[Dict[str, Any]] = None
    bull_case_projection: Optional[Dict[str, Any]] = None
    stress_test_results: Dict[str, str] = Field(description="Scenario -> pass/fail/marginal")
    key_vulnerabilities: List[str] = Field(default_factory=list)
    guardrails: List[str] = Field(default_factory=list)
    recommended_insurance: List[str] = Field(default_factory=list)


class TaxPlan(BaseModel):
    """Tax and efficiency recommendations."""
    estimated_marginal_tax_rate: Optional[float] = None
    recommended_accounts: List[str] = Field(default_factory=list)
    tax_loss_harvesting_opportunities: List[str] = Field(default_factory=list)
    retirement_contribution_strategy: Optional[str] = None
    estimated_annual_tax_savings: Optional[float] = None
    fee_analysis: Optional[str] = None


# ─── Mentor Models ───

class MentoredPlan(BaseModel):
    """The final plan after mentor interpretation."""
    mentor_id: str
    mentor_name: str
    philosophy_applied: str
    mentored_strategy: str
    mentor_voice_narrative: str = Field(description="The plan written in mentor's voice")
    key_principles_emphasized: List[str] = Field(default_factory=list)
    mentor_specific_warnings: List[str] = Field(default_factory=list)
    behavioral_coaching: List[str] = Field(default_factory=list)


class PlanDecision(BaseModel):
    """A historical plan decision for the decision log."""
    version: int
    timestamp: datetime
    previous_plan_hash: Optional[str] = None
    trigger: str = Field(description="monthly_review/user_request/market_event/life_event")
    mentor_id: str
    plan_summary: str
    key_changes: List[str] = Field(default_factory=list)
    rationale: str


# ─── Main State ───

class WealthState(BaseModel):
    """The central state object for the WealthAgents graph.
    
    This is persisted across evaluations and serves as the
    single source of truth for a user's financial plan.
    """
    # Identity
    user_id: str
    version: int = Field(default=1, ge=1)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Input
    user_profile: UserProfile
    
    # Analyst outputs (parallel)
    income_analysis: Optional[IncomeAnalysis] = None
    expense_analysis: Optional[ExpenseAnalysis] = None
    asset_analysis: Optional[AssetAnalysis] = None
    goal_analysis: Optional[GoalAnalysis] = None
    risk_analysis: Optional[RiskAnalysis] = None
    analyses_complete: bool = Field(default=False)
    
    # Debate outputs
    debate_result: Optional[DebateResult] = None
    debate_complete: bool = Field(default=False)
    
    # Planning outputs
    strategy: Optional[WealthStrategy] = None
    risk_assessment: Optional[RiskAssessment] = None
    tax_plan: Optional[TaxPlan] = None
    planning_complete: bool = Field(default=False)
    
    # Mentor interpretation
    mentor_id: str = Field(default="warren_buffett")
    mentored_plan: Optional[MentoredPlan] = None
    mentor_complete: bool = Field(default=False)
    
    # Historical
    decision_log: List[PlanDecision] = Field(default_factory=list)
    
    # Metadata
    evaluation_trigger: str = Field(default="user_request")
    errors: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
