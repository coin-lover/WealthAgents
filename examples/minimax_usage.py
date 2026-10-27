"""Using WealthAgents with the MiniMax API.

Setup:
    pip install -e ".[llm]"
    export MINIMAX_API_KEY="your-key-here"

Optional overrides:
    export MINIMAX_MODEL="MiniMax-M2"          # any MiniMax chat model
    export MINIMAX_BASE_URL="https://api.minimaxi.com/v1"   # international
    # or for China: https://api.minimax.chat/v1

Run:
    python examples/minimax_usage.py
"""

import os
import sys

from wealthagents import WealthAgents, MiniMaxLLM
from wealthagents.state import UserProfile, Asset, Debt, Goal


def create_sample_profile() -> UserProfile:
    return UserProfile(
        user_id="demo_user_001",
        age=32,
        annual_gross_income=120000,
        monthly_expenses=5200,
        location="San Francisco, CA",
        location_country="US",
        currency="USD",
        income_stability="stable",
        assets=[
            Asset(name="High-Yield Savings", asset_type="savings", value=23000),
            Asset(name="401(k)", asset_type="retirement_401k", value=85000),
            Asset(name="Brokerage", asset_type="brokerage", value=25000),
        ],
        liabilities=[
            Debt(name="Student Loans", debt_type="student_loan", balance=40000,
                 interest_rate=0.045, minimum_payment=400),
        ],
        goals=[
            Goal(name="Emergency Fund", category="emergency_fund", target_amount=30000,
                 current_amount=23000, timeline_months=12, priority="critical"),
            Goal(name="Retirement", category="retirement", target_amount=2000000,
                 current_amount=85000, timeline_months=360, priority="high"),
        ],
    )


def main() -> None:
    if not os.environ.get("MINIMAX_API_KEY"):
        sys.exit("Set MINIMAX_API_KEY first: export MINIMAX_API_KEY='your-key-here'")

    llm = MiniMaxLLM()  # reads MINIMAX_API_KEY / MINIMAX_MODEL / MINIMAX_BASE_URL
    print(f"LLM: {llm!r}")

    agent = WealthAgents(user_profile=create_sample_profile(), mentor="warren_buffett", llm=llm)

    state = agent.evaluate()
    print(agent.get_plan_summary())
    print("\n" + "=" * 60)
    print("MENTOR'S FULL LETTER (MiniMax-generated):")
    print("=" * 60)
    print(state.mentored_plan.mentor_voice_narrative)

    # Compare mentors — each gets their own LLM-generated letter
    comparison = agent.compare_mentors(["warren_buffett", "john_bogle"])
    for mentor_id, result in comparison.items():
        print(f"\n--- {result['mentor_name']} ---")
        print(result["narrative_preview"])


if __name__ == "__main__":
    main()
