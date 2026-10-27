"""Basic usage example for WealthAgents.

Demonstrates initializing the framework, running evaluation,
and switching mentors.
"""

from wealthagents import WealthAgents
from wealthagents.state import UserProfile, Asset, Debt, Goal


def create_sample_profile() -> UserProfile:
    """Create a sample user profile for demonstration."""
    return UserProfile(
        user_id="demo_user_001",
        age=32,
        annual_gross_income=120000,
        monthly_net_income=7500,
        employment_status="employed",
        industry="technology",
        years_in_current_role=3.5,
        income_stability="stable",
        household_size=2,
        dependents=0,
        location="San Francisco, CA",
        tax_filing_status="married",
        monthly_expenses=5200,
        expenses_breakdown={
            "rent": 2800,
            "utilities": 200,
            "groceries": 600,
            "transportation": 300,
            "insurance": 400,
            "dining_out": 400,
            "entertainment": 300,
            "subscriptions": 200,
        },
        assets=[
            Asset(name="Checking Account", asset_type="checking", value=8000),
            Asset(name="High-Yield Savings", asset_type="savings", value=15000, annual_return=0.045),
            Asset(name="401(k)", asset_type="retirement_401k", value=85000, cost_basis=60000),
            Asset(name="Brokerage (VTI/VXUS)", asset_type="brokerage", value=32000, cost_basis=28000),
            Asset(name="Car", asset_type="other", value=15000, liquidity="low"),
        ],
        liabilities=[
            Debt(name="Student Loans", debt_type="student_loan", balance=28000, interest_rate=0.045, minimum_payment=320),
            Debt(name="Car Loan", debt_type="auto_loan", balance=8000, interest_rate=0.035, minimum_payment=280),
        ],
        goals=[
            Goal(name="Emergency Fund", category="emergency_fund", target_amount=31200, current_amount=23000, timeline_months=6, priority="critical"),
            Goal(name="House Down Payment", category="home_purchase", target_amount=120000, current_amount=15000, timeline_months=60, priority="high"),
            Goal(name="Retirement", category="retirement", target_amount=2500000, current_amount=85000, timeline_months=360, priority="high"),
        ],
        stated_risk_tolerance="moderate",
        investment_experience="intermediate",
        previous_market_reaction="held steady during 2020, rebalanced into dip",
        current_emergency_fund_months=4.4,
        current_monthly_savings=2300,
    )


def main():
    print("=" * 70)
    print("WEALTHAGENTS DEMO: Personal Wealth Mentor")
    print("=" * 70)
    print()
    
    # Create profile
    profile = create_sample_profile()
    print(f"Created profile for {profile.user_id}")
    print(f"  Age: {profile.age}, Income: ${profile.annual_gross_income:,.0f}")
    print(f"  Net Worth: ${sum(a.value for a in profile.assets) - sum(d.balance for d in profile.liabilities):,.0f}")
    print()
    
    # List available mentors
    print("Available Mentors:")
    for mentor in WealthAgents.list_mentors():
        print(f"  • {mentor['name']} ({mentor['id']}) — {mentor['style']}")
    print()
    
    # Evaluate with Warren Buffett
    print("-" * 70)
    print("EVALUATION 1: Warren Buffett")
    print("-" * 70)
    
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    state = agent.evaluate()
    
    print(agent.get_plan_summary())
    print()
    
    # Evaluate with John Bogle
    print("-" * 70)
    print("EVALUATION 2: John Bogle (Compare)")
    print("-" * 70)
    
    agent_bogle = agent.with_mentor("john_bogle")
    state_bogle = agent_bogle.evaluate()
    
    print(agent_bogle.get_plan_summary())
    print()
    
    # Quick compare
    print("-" * 70)
    print("MENTOR COMPARISON")
    print("-" * 70)
    
    comparison = agent.compare_mentors(["warren_buffett", "john_bogle", "ray_dalio"])
    for mentor_id, data in comparison.items():
        print(f"\n{data['mentor_name']}:")
        print(f"  Philosophy: {data['philosophy']}")
        print(f"  Strategy: {data['strategy_summary']}")
        if data['key_warnings']:
            print(f"  Warnings: {', '.join(data['key_warnings'])}")
    
    print()
    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
