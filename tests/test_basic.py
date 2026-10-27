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


# ─── LLM fallback tests ───

def test_minimax_llm_unavailable_without_key():
    """Without an API key, the LLM degrades gracefully to heuristic mode."""
    from wealthagents.llm import MiniMaxLLM

    llm = MiniMaxLLM(api_key=None)
    llm.api_key = None
    assert llm.is_available() is False
    assert llm.chat("system", "user") is None


def test_evaluate_without_llm_still_works():
    """Heuristic mode: evaluate() works when no LLM is configured."""
    from wealthagents import WealthAgents

    profile = UserProfile(
        user_id="llm_test",
        age=40,
        annual_gross_income=90000,
        monthly_expenses=4000,
        assets=[Asset(name="Savings", asset_type="savings", value=20000)],
    )
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
    state = agent.evaluate()
    assert state.mentored_plan is not None
    assert len(state.mentored_plan.mentor_voice_narrative) > 0


# ─── LLM-path tests (stub MiniMax client) ───

class StubLLM:
    """Mimics MiniMaxLLM's interface, returning canned responses."""

    def __init__(self, reply=None):
        self.reply = reply
        self.calls = []

    def is_available(self):
        return True

    def chat(self, system_prompt, user_message):
        self.calls.append((system_prompt, user_message))
        if callable(self.reply):
            return self.reply(system_prompt, user_message)
        return self.reply


def test_analyst_uses_llm_when_available():
    """Analyst qualitative fields come from the LLM; numbers stay heuristic."""
    from wealthagents.agents.analysts import IncomeAnalyst
    from wealthagents.state import WealthState

    stub = StubLLM(reply='{"growth_trajectory": "accelerating", '
                          '"key_risks": ["AI disruption risk in tech sector"], '
                          '"recommendations": ["Negotiate equity compensation"], '
                          '"income_score": 1}')
    profile = UserProfile(user_id="llm_user", age=32, annual_gross_income=120000,
                          monthly_expenses=5000, industry="tech",
                          assets=[Asset(name="Savings", asset_type="savings", value=20000)])
    state = WealthState(user_id="llm_user", user_profile=profile)

    analyst = IncomeAnalyst(llm=stub)
    result = analyst.run(state)

    assert len(stub.calls) == 1                      # LLM was actually called
    assert result.growth_trajectory == "accelerating"  # LLM field adopted
    assert result.key_risks == ["AI disruption risk in tech sector"]
    assert result.income_score != 1                  # LLM cannot corrupt numeric metrics
    assert result.income_score > 0


def test_llm_debate_produces_synthesis():
    """In LLM mode the researchers debate and a judge synthesizes."""
    from wealthagents.agents.researchers import DebateSynthesizer
    from wealthagents.state import WealthState

    stub = StubLLM(reply=lambda sys, msg: f"LLM RESPONSE to: {msg.splitlines()[-1][:40]}")
    profile = UserProfile(user_id="debate_user", age=32, annual_gross_income=120000,
                          monthly_expenses=5000,
                          assets=[Asset(name="Savings", asset_type="savings", value=30000)])
    state = WealthState(user_id="debate_user", user_profile=profile)

    result = DebateSynthesizer(llm=stub).synthesize(state)
    assert len(stub.calls) == 5        # 2 researcher views + thesis + rebuttal + judge
    assert "LLM RESPONSE" in result.synthesis
    assert "LLM RESPONSE" in result.optimistic_view.thesis


def test_evaluate_with_stub_llm_full_pipeline():
    """Full pipeline runs with LLM wired through WealthAgents."""
    from wealthagents import WealthAgents, MiniMaxLLM

    replies = ['{"recommendations": ["LLM rec"], "key_risks": ["LLM risk"], '
               '"growth_trajectory": "growing", "key_stress_events": ["LLM stress"]}',
               "thesis", "rebuttal", "synthesis", "summary"]
    stub = StubLLM(reply=lambda sys, msg: replies[min(len(stub.calls) - 1, len(replies) - 1)]
                   if False else (replies.pop(0) if replies else "ok"))

    profile = UserProfile(user_id="pipe_user", age=35, annual_gross_income=100000,
                          monthly_expenses=4000,
                          assets=[Asset(name="Savings", asset_type="savings", value=25000)])
    agent = WealthAgents(user_profile=profile, mentor="warren_buffett", llm=stub)
    state = agent.evaluate()
    assert state.strategy is not None
    assert state.mentored_plan is not None
    assert len(stub.calls) > 5         # analysts + debate + strategist used the LLM
