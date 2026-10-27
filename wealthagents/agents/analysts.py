"""Analyst Team agents.

Five specialized agents that run in parallel to evaluate different
dimensions of a user's financial life.
"""

from typing import Optional

from wealthagents.agents.base import BaseWealthAgent
from wealthagents.state import (
    IncomeAnalysis,
    ExpenseAnalysis,
    AssetAnalysis,
    GoalAnalysis,
    RiskAnalysis,
    WealthState,
)


class IncomeAnalyst(BaseWealthAgent):
    """Evaluates income stability, trajectory, and risks.
    
    Like the Fundamentals Analyst in TradingAgents, but focused on
    human capital rather than company financials.
    """
    
    def __init__(self, llm=None):
        super().__init__("Income Analyst", llm=llm)
    
    def run(self, state: WealthState) -> IncomeAnalysis:
        profile = state.user_profile
        
        # Score income stability
        stability_score = self._assess_stability(profile)
        
        # Assess growth trajectory
        trajectory = self._assess_trajectory(profile)
        
        # Calculate income score
        income_score = self._calculate_income_score(profile, stability_score)
        
        # Identify risks
        risks = self._identify_risks(profile)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(profile, stability_score)
        
        return self._enhance_qualitative(
            state,
            IncomeAnalysis(
                income_score=income_score,
                income_stability_rating=stability_score,
                growth_trajectory=trajectory,
                key_risks=risks,
                recommendations=recommendations,
            ),
            fields=["growth_trajectory", "key_risks", "recommendations"],
            role="You evaluate income stability, career trajectory, and human-capital risks.",
        )
    
    def _assess_stability(self, profile) -> str:
        if profile.income_stability == "stable" and profile.years_in_current_role and profile.years_in_current_role >= 2:
            return "stable"
        elif profile.income_stability in ["stable", "moderate"]:
            return "moderate"
        return "fragile"
    
    def _assess_trajectory(self, profile) -> str:
        # Simplified heuristic
        if profile.industry in ["tech", "healthcare", "finance"]:
            return "growing"
        elif profile.years_in_current_role and profile.years_in_current_role < 1:
            return "uncertain"
        return "stable"
    
    def _calculate_income_score(self, profile, stability) -> float:
        score = 50.0
        
        # Income level (relative to US median ~$75k)
        if profile.annual_gross_income >= 150000:
            score += 20
        elif profile.annual_gross_income >= 100000:
            score += 15
        elif profile.annual_gross_income >= 75000:
            score += 10
        
        # Stability
        if stability == "stable":
            score += 20
        elif stability == "moderate":
            score += 10
        
        # Experience
        if profile.investment_experience == "advanced":
            score += 5
        
        return min(score, 100)
    
    def _identify_risks(self, profile) -> list:
        risks = []
        if profile.income_stability == "unstable":
            risks.append("Unstable income source requires larger emergency fund")
        if not profile.years_in_current_role or profile.years_in_current_role < 1:
            risks.append("Short tenure increases job transition risk")
        if profile.dependents > 0 and profile.household_size > 1:
            risks.append("Family obligations reduce income flexibility")
        if profile.employment_status == "self-employed":
            risks.append("Self-employment income is variable and benefits are self-funded")
        return risks
    
    def _generate_recommendations(self, profile, stability) -> list:
        recs = []
        if stability != "stable":
            recs.append("Prioritize building a larger emergency fund (6-12 months)")
        if profile.annual_gross_income > 100000 and not profile.monthly_net_income:
            recs.append("Optimize tax withholding or estimated payments")
        if profile.investment_experience == "beginner":
            recs.append("Consider income protection insurance or disability coverage")
        return recs


class ExpenseAnalyst(BaseWealthAgent):
    """Analyzes spending patterns, savings rate, and cash flow health."""
    
    def __init__(self, llm=None):
        super().__init__("Expense & Cashflow Analyst", llm=llm)
    
    def run(self, state: WealthState) -> ExpenseAnalysis:
        profile = state.user_profile
        
        monthly_net = profile.monthly_net_income or (profile.annual_gross_income * 0.75 / 12)
        savings_rate = (monthly_net - profile.monthly_expenses) / monthly_net if monthly_net > 0 else 0
        
        # Determine cash flow health
        if savings_rate >= 0.20:
            health = "healthy"
        elif savings_rate >= 0.05:
            health = "tight"
        else:
            health = "negative" if savings_rate < 0 else "tight"
        
        # Fixed vs variable (simplified)
        fixed_ratio = 0.6  # Default assumption
        if profile.expenses_breakdown:
            fixed_categories = ["rent", "mortgage", "utilities", "insurance", "debt_payments"]
            fixed = sum(v for k, v in profile.expenses_breakdown.items() 
                       if any(fc in k.lower() for fc in fixed_categories))
            fixed_ratio = fixed / profile.monthly_expenses if profile.monthly_expenses > 0 else 0
        
        # Recommendations
        recommendations = []
        if savings_rate < 0.15:
            recommendations.append(f"Increase savings rate from {savings_rate:.1%} to at least 15%")
        if fixed_ratio > 0.7:
            recommendations.append("High fixed expense ratio reduces flexibility; consider reducing fixed obligations")
        
        return self._enhance_qualitative(
            state,
            ExpenseAnalysis(
                savings_rate=max(0, savings_rate),
                target_savings_rate=0.20,
                fixed_expense_ratio=fixed_ratio,
                cash_flow_health=health,
                burn_rate_months=profile.current_emergency_fund_months,
                recommendations=recommendations,
            ),
            fields=["recommendations"],
            role="You analyze spending patterns, savings rate, and cash-flow health.",
        )


class AssetLiabilityAnalyst(BaseWealthAgent):
    """Evaluates net worth, asset allocation, and debt health."""
    
    def __init__(self, llm=None):
        super().__init__("Asset & Liability Analyst", llm=llm)
    
    def run(self, state: WealthState) -> AssetAnalysis:
        profile = state.user_profile
        
        total_assets = sum(a.value for a in profile.assets)
        total_liabilities = sum(d.balance for d in profile.liabilities)
        net_worth = total_assets - total_liabilities
        
        # Liquid assets
        liquid_types = ["cash", "checking", "savings", "brokerage"]
        liquid_net_worth = sum(a.value for a in profile.assets 
                              if a.asset_type.value in liquid_types)
        
        # Asset allocation
        allocation = {}
        for asset in profile.assets:
            cat = asset.asset_type.value
            allocation[cat] = allocation.get(cat, 0) + asset.value
        if total_assets > 0:
            allocation = {k: v/total_assets for k, v in allocation.items()}
        
        # Debt metrics
        dti = None
        if profile.annual_gross_income > 0:
            annual_debt_payments = sum(d.minimum_payment * 12 for d in profile.liabilities)
            dti = annual_debt_payments / profile.annual_gross_income
        
        weighted_rate = None
        if total_liabilities > 0:
            weighted_rate = sum(d.balance * d.interest_rate for d in profile.liabilities) / total_liabilities
        
        # Debt payoff priority (avalanche method default)
        debt_priority = sorted(
            profile.liabilities,
            key=lambda d: d.interest_rate,
            reverse=True
        )
        
        recommendations = []
        if weighted_rate and weighted_rate > 0.07:
            recommendations.append(f"High average debt rate ({weighted_rate:.1%}); prioritize debt payoff")
        if dti and dti > 0.36:
            recommendations.append(f"Debt-to-income ({dti:.1%}) exceeds 36%; reduce debt before investing")
        
        return self._enhance_qualitative(
            state,
            AssetAnalysis(
                net_worth=net_worth,
                liquid_net_worth=liquid_net_worth,
                asset_allocation=allocation,
                debt_to_income_ratio=dti,
                debt_to_asset_ratio=total_liabilities / total_assets if total_assets > 0 else None,
                weighted_interest_rate=weighted_rate,
                debt_payoff_priority=[d.name for d in debt_priority],
                liquidity_score=min(100, (liquid_net_worth / max(profile.monthly_expenses * 3, 1)) * 25),
                recommendations=recommendations,
            ),
            fields=["recommendations"],
            role="You evaluate net worth, asset allocation, liquidity, and debt health.",
        )


class GoalAnalyst(BaseWealthAgent):
    """Evaluates goal feasibility, funding gaps, and prioritization."""
    
    def __init__(self, llm=None):
        super().__init__("Goal Analyst", llm=llm)
    
    def run(self, state: WealthState) -> GoalAnalysis:
        profile = state.user_profile
        
        feasibility = {}
        gaps = {}
        
        monthly_savings = profile.current_monthly_savings or 0
        
        for goal in profile.goals:
            gap = goal.target_amount - goal.current_amount
            months = goal.timeline_months or 60
            
            if months > 0:
                required_monthly = gap / months
                gaps[goal.name] = max(0, required_monthly - monthly_savings)
                
                if required_monthly <= monthly_savings * 0.5:
                    feasibility[goal.name] = "feasible"
                elif required_monthly <= monthly_savings * 1.0:
                    feasibility[goal.name] = "stretch"
                else:
                    feasibility[goal.name] = "unlikely"
            else:
                feasibility[goal.name] = "unknown"
                gaps[goal.name] = 0
        
        # Priority sort: critical first, then by timeline
        sorted_goals = sorted(
            profile.goals,
            key=lambda g: (
                0 if g.priority == "critical" else 1 if g.priority == "high" else 2 if g.priority == "medium" else 3,
                g.timeline_months or 999
            )
        )
        
        recommendations = []
        if any(f == "unlikely" for f in feasibility.values()):
            recommendations.append("Some goals require more savings or longer timelines; consider prioritization")
        if not any(g.category.value == "emergency_fund" for g in profile.goals):
            recommendations.append("Add an explicit emergency fund goal if not already covered")
        
        return self._enhance_qualitative(
            state,
            GoalAnalysis(
                goal_feasibility=feasibility,
                funding_gaps=gaps,
                prioritized_goals=[g.name for g in sorted_goals],
                recommended_order=[g.name for g in sorted_goals],
                recommendations=recommendations,
            ),
            fields=["recommendations"],
            role="You evaluate goal feasibility, funding gaps, and prioritization.",
        )


class RiskProfileAnalyst(BaseWealthAgent):
    """Evaluates risk capacity vs willingness and identifies insurance gaps."""
    
    def __init__(self, llm=None):
        super().__init__("Risk Profile Analyst", llm=llm)
    
    def run(self, state: WealthState) -> RiskAnalysis:
        profile = state.user_profile
        
        # Capacity score (can they afford risk?)
        capacity = 50.0
        if profile.dependents == 0:
            capacity += 15
        if profile.current_emergency_fund_months and profile.current_emergency_fund_months >= 6:
            capacity += 15
        if profile.employment_status == "employed" and profile.income_stability == "stable":
            capacity += 10
        if profile.age < 40:
            capacity += 10
        capacity = min(capacity, 100)
        
        # Willingness score (do they want risk?)
        willingness_map = {
            "conservative": 30,
            "moderate": 60,
            "aggressive": 90,
        }
        willingness = willingness_map.get(profile.stated_risk_tolerance.value, 50)
        
        # Alignment
        if abs(capacity - willingness) <= 15:
            alignment = "aligned"
        elif capacity > willingness:
            alignment = "misaligned-capacity-higher"
        else:
            alignment = "misaligned-willingness-higher"
        
        # Stress events
        stress_events = []
        if profile.dependents > 0:
            stress_events.append("Loss of income with dependents")
        if any(d.debt_type.value == "mortgage" for d in profile.liabilities):
            stress_events.append("Housing market downturn with mortgage")
        if profile.age > 50:
            stress_events.append("Sequence of returns risk near retirement")
        
        # Insurance gaps
        insurance_gaps = []
        if profile.dependents > 0 and not (profile.existing_insurance and profile.existing_insurance.get("life")):
            insurance_gaps.append("Life insurance recommended with dependents")
        if not (profile.existing_insurance and profile.existing_insurance.get("disability")):
            insurance_gaps.append("Disability income insurance")
        if not (profile.existing_insurance and profile.existing_insurance.get("health")):
            insurance_gaps.append("Health insurance coverage")
        
        # Emergency fund recommendation
        if profile.dependents > 0 or profile.income_stability != "stable":
            ef_months = 6.0
        else:
            ef_months = 3.0
        
        recommendations = []
        if alignment != "aligned":
            recommendations.append(f"Risk capacity ({capacity:.0f}) and willingness ({willingness:.0f}) are misaligned")
        if insurance_gaps:
            recommendations.append(f"Address insurance gaps: {', '.join(insurance_gaps)}")
        
        return self._enhance_qualitative(
            state,
            RiskAnalysis(
                risk_capacity_score=capacity,
                risk_willingness_score=willingness,
                risk_alignment=alignment,
                key_stress_events=stress_events,
                insurance_gaps=insurance_gaps,
                emergency_fund_recommendation_months=ef_months,
                recommendations=recommendations,
            ),
            fields=["key_stress_events", "recommendations"],
            role="You evaluate risk capacity vs. willingness and identify insurance gaps.",
        )
