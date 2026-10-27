"""Planning Team agents.

Sequential agents that draft, stress-test, and optimize the wealth plan.
"""

from typing import List, Dict

from wealthagents.agents.base import BaseWealthAgent
from wealthagents.state import (
    WealthState,
    WealthStrategy,
    RiskAssessment,
    TaxPlan,
    ActionItem,
)


class Strategist(BaseWealthAgent):
    """Drafts the core wealth strategy.
    
    Like the Trader in TradingAgents, proposes concrete actions:
    - Emergency fund target
    - Debt payoff strategy
    - Monthly investment allocation
    - Account funding order
    """
    
    def __init__(self):
        super().__init__("Strategist")
    
    def run(self, state: WealthState) -> WealthStrategy:
        profile = state.user_profile
        analyses = {
            "income": state.income_analysis,
            "expense": state.expense_analysis,
            "asset": state.asset_analysis,
            "goal": state.goal_analysis,
            "risk": state.risk_analysis,
            "debate": state.debate_result,
        }
        
        # Emergency fund
        ef_months = state.risk_analysis.emergency_fund_recommendation_months if state.risk_analysis else 6
        ef_target = profile.monthly_expenses * ef_months
        
        # Debt strategy
        debt_strategy, monthly_debt = self._design_debt_strategy(profile, state)
        
        # Investment amount
        monthly_net = profile.monthly_net_income or (profile.annual_gross_income * 0.75 / 12)
        monthly_investment = max(0, monthly_net - profile.monthly_expenses - monthly_debt)
        
        # Adjust for savings rate target
        expense = state.expense_analysis
        if expense and expense.target_savings_rate:
            target_savings = monthly_net * expense.target_savings_rate
            current_savings = monthly_net - profile.monthly_expenses
            if current_savings < target_savings:
                # Need to either reduce expenses or it's a stretch goal
                pass
        
        # Asset allocation based on risk profile
        allocation = self._design_allocation(profile, state)
        
        # Account funding order
        funding_order = self._funding_order(profile, state)
        
        # Action items
        actions = self._build_actions(profile, state, ef_target, debt_strategy, monthly_investment)
        
        summary = self._build_summary(ef_months, debt_strategy, monthly_investment, allocation)
        
        return WealthStrategy(
            emergency_fund_target=ef_target,
            emergency_fund_months=ef_months,
            debt_strategy=debt_strategy,
            monthly_debt_payment=monthly_debt,
            monthly_investment=monthly_investment,
            recommended_allocation=allocation,
            account_funding_order=funding_order,
            action_items=actions,
            strategy_summary=summary,
        )
    
    def _design_debt_strategy(self, profile, state) -> tuple:
        asset = state.asset_analysis
        
        if not asset or not profile.liabilities:
            return "none", 0
        
        # If any debt > 8%, avalanche (highest rate first)
        high_interest = any(d.interest_rate > 0.08 for d in profile.liabilities)
        
        # If low interest and behavioral benefit, snowball (lowest balance first)
        low_interest = all(d.interest_rate < 0.06 for d in profile.liabilities)
        
        if high_interest:
            strategy = "avalanche"
        elif low_interest and len(profile.liabilities) > 2:
            strategy = "snowball"
        else:
            strategy = "hybrid"
        
        # Calculate aggressive debt payment
        monthly_net = profile.monthly_net_income or (profile.annual_gross_income * 0.75 / 12)
        available = monthly_net - profile.monthly_expenses
        
        # Cap at 50% of available cash flow for debt, rest for goals
        max_debt_payment = available * 0.5 if available > 0 else 0
        
        # Minimum of all minimums
        min_total = sum(d.minimum_payment for d in profile.liabilities)
        
        # Pay extra toward priority debt
        debt_payment = max(min_total, min(max_debt_payment, min_total * 1.5))
        
        return strategy, debt_payment
    
    def _design_allocation(self, profile, state) -> Dict[str, float]:
        risk = state.risk_analysis
        
        if not risk:
            # Default moderate
            return {"stocks": 0.60, "bonds": 0.30, "cash": 0.10}
        
        age = profile.age
        risk_score = (risk.risk_capacity_score + risk.risk_willingness_score) / 2
        
        # Base: age-based rule of thumb
        stock_base = max(0.20, min(0.90, (100 - age) / 100))
        
        # Adjust for risk score
        if risk_score > 75:
            stock_base += 0.10
        elif risk_score < 40:
            stock_base -= 0.15
        
        stock_base = max(0.20, min(0.95, stock_base))
        
        # Cash based on emergency fund status
        ef_months = profile.current_emergency_fund_months or 0
        target_ef = state.risk_analysis.emergency_fund_recommendation_months if state.risk_analysis else 6
        
        if ef_months < target_ef * 0.5:
            cash = 0.15  # Building emergency fund
        elif ef_months < target_ef:
            cash = 0.10
        else:
            cash = 0.05
        
        bonds = 1 - stock_base - cash
        if bonds < 0:
            bonds = 0
            stock_base = 1 - cash
        
        return {
            "stocks": round(stock_base, 2),
            "bonds": round(bonds, 2),
            "cash": round(cash, 2),
        }
    
    def _funding_order(self, profile, state) -> List[str]:
        """Determine optimal account funding order."""
        order = []
        
        # 1. 401k match (free money)
        order.append("401(k) up to employer match")
        
        # 2. HSA if available (triple tax advantaged)
        order.append("HSA (if eligible)")
        
        # 3. Roth IRA / Traditional IRA
        order.append("Roth IRA or Traditional IRA")
        
        # 4. Max 401k
        order.append("Max 401(k)")
        
        # 5. Taxable brokerage
        order.append("Taxable brokerage account")
        
        return order
    
    def _build_actions(self, profile, state, ef_target, debt_strategy, monthly_investment) -> List[ActionItem]:
        actions = []
        
        # Emergency fund
        ef_current = sum(a.value for a in profile.assets if a.asset_type.value in ["cash", "checking", "savings"])
        if ef_current < ef_target:
            gap = ef_target - ef_current
            actions.append(ActionItem(
                action=f"Build emergency fund to ${ef_target:,.0f} ({state.risk_analysis.emergency_fund_recommendation_months if state.risk_analysis else 6} months expenses)",
                priority=1,
                category="emergency",
                timeline="immediate",
                estimated_impact=f"Reduces bankruptcy risk by ~80%; gap is ${gap:,.0f}",
                rationale="Foundation of all financial plans; prevents debt spiral during emergencies",
            ))
        
        # High interest debt
        high_interest_debts = [d for d in profile.liabilities if d.interest_rate > 0.08]
        if high_interest_debts:
            actions.append(ActionItem(
                action=f"Pay off high-interest debt: {', '.join(d.name for d in high_interest_debts)}",
                priority=2,
                category="debt",
                timeline="immediate",
                estimated_impact=f"Guaranteed return of {max(d.interest_rate for d in high_interest_debts):.1%}",
                rationale="Debt at >8% is a negative-return guarantee; payoff is risk-free return",
            ))
        
        # Investment setup
        if monthly_investment > 500:
            actions.append(ActionItem(
                action=f"Automate monthly investment of ${monthly_investment:,.0f}",
                priority=3,
                category="invest",
                timeline="1_month",
                estimated_impact=f"~${monthly_investment * 12 * 20 * 1.5:,.0f} in 20 years (assumed 7% return)",
                rationale="Automation removes behavioral friction and ensures consistency",
            ))
        
        return actions
    
    def _build_summary(self, ef_months, debt_strategy, monthly_investment, allocation) -> str:
        return (
            f"Build {ef_months}-month emergency fund, use {debt_strategy} debt payoff, "
            f"invest ${monthly_investment:,.0f}/month with {allocation['stocks']:.0%} stocks / "
            f"{allocation['bonds']:.0%} bonds / {allocation['cash']:.0%} cash."
        )


class RiskManager(BaseWealthAgent):
    """Stress tests the wealth plan.
    
    Like the Risk Management Team in TradingAgents, evaluates what
    breaks the plan under adverse scenarios.
    """
    
    def __init__(self):
        super().__init__("Risk Manager")
    
    def run(self, state: WealthState) -> RiskAssessment:
        profile = state.user_profile
        strategy = state.strategy
        
        if not strategy:
            return RiskAssessment()
        
        # Stress tests
        stress_results = {}
        
        # Scenario 1: Job loss for 6 months
        runway = self._calculate_runway(profile, strategy, income_drop=1.0)
        stress_results["6_month_unemployment"] = "pass" if runway >= 6 else "fail"
        
        # Scenario 2: Market crash (-30%)
        portfolio_impact = self._simulate_market_drop(profile, strategy, drop=0.30)
        stress_results["30_percent_market_decline"] = "pass" if portfolio_impact > 0 else "marginal"
        
        # Scenario 3: Emergency expense ($10k)
        ef_coverage = self._emergency_fund_coverage(profile, strategy, expense=10000)
        stress_results["10k_emergency_expense"] = "pass" if ef_coverage else "fail"
        
        # Scenario 4: Interest rate spike (+3%)
        rate_impact = self._interest_rate_spike(profile, strategy, increase=0.03)
        stress_results["3_percent_rate_increase"] = rate_impact
        
        # Key vulnerabilities
        vulnerabilities = []
        if stress_results["6_month_unemployment"] == "fail":
            vulnerabilities.append("Insufficient emergency fund for job loss scenario")
        if stress_results["30_percent_market_decline"] != "pass":
            vulnerabilities.append("Portfolio too concentrated; would suffer significant drawdown")
        if any(d.interest_rate > 0.10 for d in profile.liabilities):
            vulnerabilities.append("High-interest debt vulnerable to rate increases")
        
        # Guardrails
        guardrails = [
            f"Never let emergency fund drop below {strategy.emergency_fund_months} months expenses",
            f"Monthly investment capped at {strategy.monthly_investment * 1.2:,.0f} (20% buffer)",
            "Rebalance allocation annually or after 5% drift",
            "Review plan if income drops >20% or expenses rise >15%",
        ]
        
        # Insurance recommendations
        insurance = []
        if profile.dependents > 0:
            insurance.append("Term life insurance: 10x annual income")
        if profile.employment_status == "employed":
            insurance.append("Disability insurance: 60% income replacement")
        insurance.append("Umbrella liability: $1M minimum if net worth > $500k")
        
        return RiskAssessment(
            stress_test_results=stress_results,
            key_vulnerabilities=vulnerabilities,
            guardrails=guardrails,
            recommended_insurance=insurance,
        )
    
    def _calculate_runway(self, profile, strategy, income_drop: float) -> float:
        """Calculate months of survival with reduced/no income."""
        liquid = sum(a.value for a in profile.assets if a.asset_type.value in ["cash", "checking", "savings"])
        monthly_burn = profile.monthly_expenses + strategy.monthly_debt_payment
        return liquid / monthly_burn if monthly_burn > 0 else 999
    
    def _simulate_market_drop(self, profile, strategy, drop: float) -> float:
        """Simulate portfolio value after market drop."""
        invested = sum(a.value for a in profile.assets if a.asset_type.value in ["brokerage", "retirement_401k", "retirement_ira"])
        stock_allocation = strategy.recommended_allocation.get("stocks", 0.60)
        return invested * (1 - drop * stock_allocation)
    
    def _emergency_fund_coverage(self, profile, strategy, expense: float) -> bool:
        """Check if emergency fund covers unexpected expense."""
        ef = sum(a.value for a in profile.assets if a.asset_type.value in ["cash", "checking", "savings"])
        return ef >= expense
    
    def _interest_rate_spike(self, profile, strategy, increase: float) -> str:
        """Assess impact of rate increase on debt."""
        variable_debts = [d for d in profile.liabilities if d.debt_type.value in ["credit_card", "personal_loan", "auto_loan"]]
        if not variable_debts:
            return "pass"
        
        new_payments = sum(d.minimum_payment * (1 + increase / d.interest_rate) if d.interest_rate > 0 else d.minimum_payment for d in variable_debts)
        old_payments = sum(d.minimum_payment for d in variable_debts)
        
        monthly_net = profile.monthly_net_income or (profile.annual_gross_income * 0.75 / 12)
        if new_payments > monthly_net * 0.30:
            return "fail"
        elif new_payments > old_payments * 1.2:
            return "marginal"
        return "pass"


class TaxEfficiencyAnalyst(BaseWealthAgent):
    """Optimizes tax strategy and account ordering.
    
    Ensures the user keeps more of what they earn through
    tax-advantaged accounts and efficient placement.
    """
    
    def __init__(self):
        super().__init__("Tax & Efficiency Analyst")
    
    def run(self, state: WealthState) -> TaxPlan:
        profile = state.user_profile
        strategy = state.strategy
        
        # Estimate marginal tax rate (simplified US brackets)
        income = profile.annual_gross_income
        if income > 609350:  # 2024 single 37% bracket
            marginal_rate = 0.37
        elif income > 243725:
            marginal_rate = 0.35
        elif income > 191950:
            marginal_rate = 0.32
        elif income > 100525:
            marginal_rate = 0.24
        elif income > 47150:
            marginal_rate = 0.22
        elif income > 11600:
            marginal_rate = 0.12
        else:
            marginal_rate = 0.10
        
        # Recommended accounts based on profile
        accounts = []
        
        if profile.employment_status == "employed":
            accounts.append("401(k) - pre-tax contributions reduce current taxable income")
            if marginal_rate > 0.22:
                accounts.append("Traditional 401(k) preferred over Roth given high marginal rate")
            else:
                accounts.append("Roth 401(k) or Roth IRA - pay taxes now while rate is low")
        
        accounts.append("Roth IRA - tax-free growth; income limits may apply")
        
        if strategy and strategy.emergency_fund_months >= 3:
            accounts.append("HSA (if HDHP eligible) - triple tax advantage")
        
        if any(a.asset_type.value == "brokerage" for a in profile.assets):
            accounts.append("Taxable brokerage - use tax-efficient index funds")
        
        # Tax loss harvesting
        tlh_opps = []
        for asset in profile.assets:
            if asset.cost_basis and asset.value < asset.cost_basis:
                loss = asset.cost_basis - asset.value
                tlh_opps.append(f"{asset.name}: ${loss:,.0f} loss available for harvesting")
        
        # Retirement contribution strategy
        retirement_strategy = None
        if profile.age >= 50:
            retirement_strategy = "Maximize catch-up contributions ($7,500 additional for 401k, $1,000 for IRA)"
        elif strategy:
            retirement_strategy = f"Target {strategy.monthly_investment * 0.5:,.0f}/month to tax-advantaged accounts first"
        
        # Fee analysis
        fee_analysis = None
        if any(a.asset_type.value in ["brokerage", "retirement_401k"] for a in profile.assets):
            fee_analysis = (
                "Review expense ratios: target <0.20% for index funds, <0.50% for active. "
                "A 1% fee difference compounds to ~$100k+ over 30 years."
            )
        
        # Estimate tax savings
        estimated_savings = None
        if strategy and marginal_rate > 0:
            pre_tax_contribution = min(strategy.monthly_investment * 0.5, 23000 / 12)  # 401k limit
            estimated_savings = pre_tax_contribution * 12 * marginal_rate
        
        return TaxPlan(
            estimated_marginal_tax_rate=marginal_rate,
            recommended_accounts=accounts,
            tax_loss_harvesting_opportunities=tlh_opps,
            retirement_contribution_strategy=retirement_strategy,
            estimated_annual_tax_savings=estimated_savings,
            fee_analysis=fee_analysis,
        )
