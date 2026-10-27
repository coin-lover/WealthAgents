"""Researcher Team agents.

Bullish (optimistic) and bearish (cautious) researchers debate the
wealth plan, mirroring TradingAgents' Researcher Team dynamic.
"""

from wealthagents.agents.base import BaseWealthAgent
from wealthagents.state import (
    ResearchView,
    DebateResult,
    WealthState,
)


class OptimisticResearcher(BaseWealthAgent):
    """Argues for growth, compounding, and opportunity cost of inaction.
    
    The "bullish" voice in the wealth debate. Emphasizes:
    - Power of compounding over long time horizons
    - Opportunity cost of excess cash / delayed investing
    - Human capital growth potential
    - Inflation as a reason to invest, not save
    """
    
    def __init__(self):
        super().__init__("Optimistic Researcher")
    
    def run(self, state: WealthState) -> ResearchView:
        profile = state.user_profile
        analyses = {
            "income": state.income_analysis,
            "expense": state.expense_analysis,
            "asset": state.asset_analysis,
            "goal": state.goal_analysis,
            "risk": state.risk_analysis,
        }
        
        thesis = self._build_thesis(profile, analyses)
        key_points = self._build_key_points(profile, analyses)
        concerns = self._build_concerns(profile, analyses)
        confidence = self._calculate_confidence(analyses)
        
        return ResearchView(
            perspective="optimistic",
            thesis=thesis,
            key_points=key_points,
            concerns=concerns,
            confidence=confidence,
        )
    
    def _build_thesis(self, profile, analyses) -> str:
        age = profile.age
        income = profile.annual_gross_income
        
        if age < 35 and income > 80000:
            return ("This user has time and income on their side. The biggest risk is not market "
                   "volatility, but paralysis and excessive conservatism. They should optimize for "
                   "growth and accept volatility as the price of admission.")
        elif age < 50:
            return ("With a multi-decade horizon, this user can afford to be growth-oriented. "
                   "The power of compounding favors the consistent investor who stays the course.")
        else:
            return ("Even at this stage, longevity risk means maintaining some growth exposure. "
                   "The goal is not to eliminate risk but to manage it intelligently.")
    
    def _build_key_points(self, profile, analyses) -> list:
        points = []
        
        income = analyses.get("income")
        if income and income.growth_trajectory == "growing":
            points.append("Growing income trajectory supports increasing savings rate over time")
        
        expense = analyses.get("expense")
        if expense and expense.savings_rate < 0.15:
            points.append(f"Current savings rate ({expense.savings_rate:.1%}) has room to grow; even small increases compound dramatically")
        
        asset = analyses.get("asset")
        if asset and asset.liquid_net_worth > profile.monthly_expenses * 6:
            points.append("Healthy liquid net worth provides cushion to invest more aggressively")
        
        risk = analyses.get("risk")
        if risk and risk.risk_capacity_score > 70:
            points.append("High risk capacity supports greater equity exposure")
        
        # Time horizon argument
        years_to_65 = max(0, 65 - profile.age)
        if years_to_65 > 20:
            points.append(f"With {years_to_65} years to traditional retirement, equity risk is temporary but regret of under-investing is permanent")
        
        points.append("Historical data: staying invested beats timing the market over virtually all 10+ year periods")
        
        return points
    
    def _build_concerns(self, profile, analyses) -> list:
        # Optimistic researcher acknowledges but downplays risks
        concerns = []
        
        risk = analyses.get("risk")
        if risk and risk.risk_alignment == "misaligned-willingness-higher":
            concerns.append("User's risk willingness exceeds capacity; need guardrails to prevent overreaching")
        
        expense = analyses.get("expense")
        if expense and expense.cash_flow_health == "negative":
            concerns.append("Negative cash flow must be addressed before any investment strategy")
        
        return concerns
    
    def _calculate_confidence(self, analyses) -> float:
        score = 0.7
        if analyses.get("income") and analyses["income"].income_stability_rating == "stable":
            score += 0.15
        if analyses.get("expense") and analyses["expense"].cash_flow_health == "healthy":
            score += 0.10
        return min(score, 0.95)


class CautiousResearcher(BaseWealthAgent):
    """Argues for resilience, sequence-of-returns risk, and plan fragility.
    
    The "bearish" voice in the wealth debate. Emphasizes:
    - What breaks the plan (job loss, health, market crashes)
    - Sequence of returns risk
    - Behavioral risk (will they panic sell?)
    - The cost of being wrong vs cost of being slow
    """
    
    def __init__(self):
        super().__init__("Cautious Researcher")
    
    def run(self, state: WealthState) -> ResearchView:
        profile = state.user_profile
        analyses = {
            "income": state.income_analysis,
            "expense": state.expense_analysis,
            "asset": state.asset_analysis,
            "goal": state.goal_analysis,
            "risk": state.risk_analysis,
        }
        
        thesis = self._build_thesis(profile, analyses)
        key_points = self._build_key_points(profile, analyses)
        concerns = self._build_concerns(profile, analyses)
        confidence = self._calculate_confidence(analyses)
        
        return ResearchView(
            perspective="cautious",
            thesis=thesis,
            key_points=key_points,
            concerns=concerns,
            confidence=confidence,
        )
    
    def _build_thesis(self, profile, analyses) -> str:
        risk = analyses.get("risk")
        
        if risk and risk.risk_alignment == "misaligned-willingness-higher":
            return ("This user is at high risk of behavioral mistakes during drawdowns. "
                   "The plan must prioritize sleeping-well-at-night over theoretical optimization. "
                   "A plan that is abandoned in crisis is worse than a conservative plan that is followed.")
        
        if profile.dependents > 0 and profile.current_emergency_fund_months and profile.current_emergency_fund_months < 6:
            return ("With dependents and limited liquidity, this household is one emergency away from debt. "
                   "Defense comes before offense. Build the moat before deploying capital.")
        
        return ("Wealth preservation and plan resilience matter more than maximization. "
               "The user needs to survive the inevitable bad years to benefit from the good ones.")
    
    def _build_key_points(self, profile, analyses) -> list:
        points = []
        
        # Emergency fund priority
        ef_months = profile.current_emergency_fund_months or 0
        if ef_months < 3:
            points.append(f"Emergency fund at {ef_months:.1f} months is dangerously low; this is the #1 priority")
        elif ef_months < 6:
            points.append(f"Emergency fund at {ef_months:.1f} months below recommended level for profile")
        
        # Debt concerns
        asset = analyses.get("asset")
        if asset and asset.weighted_interest_rate and asset.weighted_interest_rate > 0.08:
            points.append(f"High-interest debt ({asset.weighted_interest_rate:.1%}) creates guaranteed negative returns")
        
        # Sequence risk for older users
        if profile.age > 50:
            points.append(f"At age {profile.age}, sequence-of-returns risk is material; equity exposure should be moderated")
        
        # Behavioral risk
        risk = analyses.get("risk")
        if risk and risk.risk_willingness_score < 40:
            points.append("Low risk willingness suggests user may panic during drawdowns; conservative allocation prevents abandonment")
        
        # Income fragility
        income = analyses.get("income")
        if income and income.income_stability_rating == "fragile":
            points.append("Fragile income source requires larger cash reserves and less market exposure")
        
        points.append("Historical data: the biggest wealth destroyer is not low returns, but selling during crashes")
        
        return points
    
    def _build_concerns(self, profile, analyses) -> list:
        concerns = []
        
        expense = analyses.get("expense")
        if expense and expense.cash_flow_health == "negative":
            concerns.append("NEGATIVE CASH FLOW: User is spending more than earning; this is unsustainable")
        
        asset = analyses.get("asset")
        if asset and asset.debt_to_income_ratio and asset.debt_to_income_ratio > 0.43:
            concerns.append(f"Debt-to-income at {asset.debt_to_income_ratio:.1%} is in dangerous territory")
        
        goal = analyses.get("goal")
        if goal and any(f == "unlikely" for f in goal.goal_feasibility.values()):
            concerns.append("Some goals are mathematically unlikely with current trajectory; expectations need adjustment")
        
        return concerns
    
    def _calculate_confidence(self, analyses) -> float:
        score = 0.7
        if analyses.get("expense") and analyses["expense"].cash_flow_health != "healthy":
            score += 0.15
        if analyses.get("asset") and analyses["asset"].debt_to_income_ratio and analyses["asset"].debt_to_income_ratio > 0.36:
            score += 0.10
        return min(score, 0.95)


class DebateSynthesizer:
    """Synthesizes the debate between optimistic and cautious researchers."""
    
    def synthesize(self, state: WealthState) -> DebateResult:
        optimistic = state.income_analysis  # Placeholder - would be fetched from state
        
        # In real implementation, these would be stored in state
        # For now, we reconstruct
        from wealthagents.agents.researchers import OptimisticResearcher, CautiousResearcher
        
        opt = OptimisticResearcher().run(state)
        caut = CautiousResearcher().run(state)
        
        # Determine synthesis based on which concerns are more urgent
        urgent_concerns = [c for c in caut.concerns if "NEGATIVE" in c or "dangerously" in c.lower()]
        
        if urgent_concerns:
            synthesis = (
                "The cautious view prevails on immediate priorities. The user has structural "
                "issues (cash flow or debt) that must be addressed before growth strategies. "
                "Once stabilized, the optimistic growth trajectory is appropriate."
            )
        elif opt.confidence > caut.confidence + 0.15:
            synthesis = (
                "The optimistic case is stronger. The user has stable fundamentals and time horizon "
                "to absorb volatility. The plan should lean toward growth while maintaining "
                "appropriate guardrails."
            )
        else:
            synthesis = (
                "A balanced approach is warranted. The user can pursue growth but must build "
                "resilience first. The plan should phase in risk as foundations are strengthened."
            )
        
        key_risks = list(set(opt.concerns + caut.concerns))
        
        return DebateResult(
            optimistic_view=opt,
            cautious_view=caut,
            synthesis=synthesis,
            key_risks_to_monitor=key_risks,
        )
