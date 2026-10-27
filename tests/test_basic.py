"""Basic tests for WealthAgents framework."""

import pytest
from wealthagents import WealthAgents
from wealthagents.state import UserProfile, Asset, Debt, Goal


def create_test_profile():
    """Create a minimal test profile."""
    return UserProfile(
        user_id="test_user",
        age=30,
        annual_gross_income=80000,
        monthly_expenses=4000,
        assets=[
            Asset(name="Savings", asset_type="savings", value=10000),
            Asset(name="401k", asset_type="retirement_401k", value=50000),
        ],
        liabilities=[
            Debt(name="Student Loan", debt_type="student_loan", balance=20000, interest_rate=0.05, minimum_payment=200),
        ],
        goals=[
            Goal(name="Emergency Fund", category="emergency_fund", target_amount=12000, current_amount=10000, timeline_months=6, priority="critical"),
        ],
        stated_risk_tolerance="moderate",
    )


def test_initialization():
    profile = create_test_profile()
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    
    assert agent.user_profile.user_id == "test_user"
    assert agent.mentor_id == "warren_buffett"
    assert agent.state.version == 1


def test_evaluation():
    profile = create_test_profile()
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    
    state = agent.evaluate()
    
    assert state.analyses_complete
    assert state.income_analysis is not None
    assert state.expense_analysis is not None
    assert state.asset_analysis is not None
    assert state.goal_analysis is not None
    assert state.risk_analysis is not None
    assert state.debate_complete
    assert state.planning_complete
    assert state.mentor_complete
    assert state.mentored_plan is not None


def test_mentor_switching():
    profile = create_test_profile()
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    
    agent.evaluate()
    
    bogle_agent = agent.with_mentor("john_bogle")
    state = bogle_agent.evaluate()
    
    assert state.mentored_plan.mentor_id == "john_bogle"
    assert state.mentored_plan.mentor_name == "John Bogle"


def test_list_mentors():
    mentors = WealthAgents.list_mentors()
    assert len(mentors) >= 7
    
    ids = [m["id"] for m in mentors]
    assert "warren_buffett" in ids
    assert "john_bogle" in ids
    assert "ray_dalio" in ids


def test_plan_summary():
    profile = create_test_profile()
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    agent.evaluate()
    
    summary = agent.get_plan_summary()
    assert "WEALTH PLAN" in summary
    assert "Warren Buffett" in summary


def test_mentor_comparison():
    profile = create_test_profile()
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    
    comparison = agent.compare_mentors(["warren_buffett", "john_bogle"])
    
    assert "warren_buffett" in comparison
    assert "john_bogle" in comparison
    assert comparison["warren_buffett"]["mentor_name"] == "Warren Buffett"
    assert comparison["john_bogle"]["mentor_name"] == "John Bogle"


def test_invalid_mentor():
    profile = create_test_profile()
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    
    with pytest.raises(ValueError):
        agent.with_mentor("nonexistent_mentor")


def test_error_handling():
    """Test that individual agent failures don't crash the pipeline."""
    profile = create_test_profile()
    # Remove some data to trigger edge cases
    profile.assets = []
    profile.liabilities = []
    
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    state = agent.evaluate()
    
    # Should still complete even with edge case data
    assert state.mentor_complete or len(state.errors) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
