"""LangGraph workflow definition for WealthAgents.

Defines the multi-agent graph that orchestrates:
1. Parallel analyst execution
2. Researcher debate
3. Sequential planning
4. Mentor interpretation

Modeled after TradingAgents' graph structure but adapted for
personal wealth evaluation.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from wealthagents.state import WealthState, UserProfile, PlanDecision
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
    DebateSynthesizer,
)
from wealthagents.agents.planning import (
    Strategist,
    RiskManager,
    TaxEfficiencyAnalyst,
)
from wealthagents.mentors.registry import MentorRegistry


class WealthAgentsGraph:
    """The main WealthAgents workflow graph.
    
    This class can be used directly (without LangGraph dependency)
    as a sequential executor, or adapted to LangGraph nodes.
    """
    
    def __init__(self, mentor_id: str = "warren_buffett"):
        self.mentor_id = mentor_id
        
        # Analyst team
        self.income_analyst = IncomeAnalyst()
        self.expense_analyst = ExpenseAnalyst()
        self.asset_analyst = AssetLiabilityAnalyst()
        self.goal_analyst = GoalAnalyst()
        self.risk_analyst = RiskProfileAnalyst()
        
        # Researcher team
        self.optimistic_researcher = OptimisticResearcher()
        self.cautious_researcher = CautiousResearcher()
        self.debate_synthesizer = DebateSynthesizer()
        
        # Planning team
        self.strategist = Strategist()
        self.risk_manager = RiskManager()
        self.tax_analyst = TaxEfficiencyAnalyst()
    
    def run(self, state: WealthState) -> WealthState:
        """Execute the full wealth evaluation workflow.
        
        This runs the complete pipeline:
        1. Analyst team (parallel in concept, sequential here for simplicity)
        2. Researcher debate
        3. Planning team
        4. Mentor interpretation
        
        For true parallel execution, adapt to LangGraph with
        parallel node execution.
        """
        print(f"Starting WealthAgents evaluation for user {state.user_id}")
        
        # Step 1: Analyst Team (parallel)
        state = self._run_analysts(state)
        
        # Step 2: Researcher Debate
        state = self._run_debate(state)
        
        # Step 3: Planning Team
        state = self._run_planning(state)
        
        # Step 4: Mentor Interpretation
        state = self._run_mentor(state)
        
        # Step 5: Log decision
        state = self._log_decision(state)
        
        print(f"Evaluation complete. Version {state.version}")
        return state
    
    def _run_analysts(self, state: WealthState) -> WealthState:
        """Execute all five analysts.
        
        In LangGraph, these would be parallel nodes.
        """
        print("Running Analyst Team...")
        
        try:
            state.income_analysis = self.income_analyst.run(state)
            print(f"  Income Analyst: score={state.income_analysis.income_score:.1f}")
        except Exception as e:
            state.errors.append(f"Income Analyst failed: {e}")
        
        try:
            state.expense_analysis = self.expense_analyst.run(state)
            print(f"  Expense Analyst: savings_rate={state.expense_analysis.savings_rate:.1%}")
        except Exception as e:
            state.errors.append(f"Expense Analyst failed: {e}")
        
        try:
            state.asset_analysis = self.asset_analyst.run(state)
            print(f"  Asset Analyst: net_worth=${state.asset_analysis.net_worth:,.0f}")
        except Exception as e:
            state.errors.append(f"Asset Analyst failed: {e}")
        
        try:
            state.goal_analysis = self.goal_analyst.run(state)
            print(f"  Goal Analyst: {len(state.goal_analysis.prioritized_goals)} goals prioritized")
        except Exception as e:
            state.errors.append(f"Goal Analyst failed: {e}")
        
        try:
            state.risk_analysis = self.risk_analyst.run(state)
            print(f"  Risk Analyst: capacity={state.risk_analysis.risk_capacity_score:.0f}, willingness={state.risk_analysis.risk_willingness_score:.0f}")
        except Exception as e:
            state.errors.append(f"Risk Analyst failed: {e}")
        
        state.analyses_complete = True
        return state
    
    def _run_debate(self, state: WealthState) -> WealthState:
        """Run the researcher debate."""
        print("Running Researcher Debate...")
        
        try:
            state.debate_result = self.debate_synthesizer.synthesize(state)
            print(f"  Optimistic confidence: {state.debate_result.optimistic_view.confidence:.2f}")
            print(f"  Cautious confidence: {state.debate_result.cautious_view.confidence:.2f}")
            print(f"  Synthesis: {state.debate_result.synthesis[:80]}...")
        except Exception as e:
            state.errors.append(f"Debate failed: {e}")
        
        state.debate_complete = True
        return state
    
    def _run_planning(self, state: WealthState) -> WealthState:
        """Run the planning team sequentially."""
        print("Running Planning Team...")
        
        try:
            state.strategy = self.strategist.run(state)
            print(f"  Strategist: {state.strategy.strategy_summary[:80]}...")
        except Exception as e:
            state.errors.append(f"Strategist failed: {e}")
        
        try:
            state.risk_assessment = self.risk_manager.run(state)
            print(f"  Risk Manager: {len(state.risk_assessment.stress_test_results)} stress tests run")
        except Exception as e:
            state.errors.append(f"Risk Manager failed: {e}")
        
        try:
            state.tax_plan = self.tax_analyst.run(state)
            print(f"  Tax Analyst: marginal_rate={state.tax_plan.estimated_marginal_tax_rate:.1%}")
        except Exception as e:
            state.errors.append(f"Tax Analyst failed: {e}")
        
        state.planning_complete = True
        return state
    
    def _run_mentor(self, state: WealthState) -> WealthState:
        """Run the mentor interpretation."""
        print(f"Running Mentor Interpretation ({self.mentor_id})...")
        
        mentor = MentorRegistry.get(self.mentor_id)
        if not mentor:
            state.errors.append(f"Mentor {self.mentor_id} not found, using default")
            mentor = MentorRegistry.get_default()
        
        try:
            state.mentored_plan = mentor.interpret_plan(state)
            print(f"  Mentor: {state.mentored_plan.mentor_name}")
            print(f"  Principles emphasized: {len(state.mentored_plan.key_principles_emphasized)}")
        except Exception as e:
            state.errors.append(f"Mentor interpretation failed: {e}")
        
        state.mentor_complete = True
        return state
    
    def _log_decision(self, state: WealthState) -> WealthState:
        """Log this plan decision to history."""
        decision = PlanDecision(
            version=state.version,
            timestamp=datetime.now(),
            trigger=state.evaluation_trigger,
            mentor_id=self.mentor_id,
            plan_summary=state.strategy.strategy_summary if state.strategy else "No strategy generated",
            key_changes=[],
            rationale=state.debate_result.synthesis if state.debate_result else "No debate result",
        )
        state.decision_log.append(decision)
        return state
    
    def with_mentor(self, mentor_id: str) -> "WealthAgentsGraph":
        """Create a new graph instance with a different mentor."""
        new_graph = WealthAgentsGraph(mentor_id=mentor_id)
        return new_graph


# ─── LangGraph Adapter (optional) ───

def build_langgraph_workflow(mentor_id: str = "warren_buffett"):
    """Build a LangGraph StateGraph for WealthAgents.
    
    This is the advanced version that uses LangGraph for
    parallel analyst execution and proper state management.
    
    Requires: pip install langgraph
    
    Usage:
        graph = build_langgraph_workflow()
        result = graph.invoke(initial_state)
    """
    try:
        from langgraph.graph import StateGraph, END
    except ImportError:
        raise ImportError("langgraph is required for build_langgraph_workflow. Install with: pip install langgraph")
    
    # Define state type
    from typing import TypedDict
    
    class GraphState(TypedDict):
        wealth_state: WealthState
    
    # Initialize agents
    graph = WealthAgentsGraph(mentor_id=mentor_id)
    
    # Node functions
    def analyst_node(state: GraphState) -> GraphState:
        ws = state["wealth_state"]
        ws = graph._run_analysts(ws)
        return {"wealth_state": ws}
    
    def debate_node(state: GraphState) -> GraphState:
        ws = state["wealth_state"]
        ws = graph._run_debate(ws)
        return {"wealth_state": ws}
    
    def planning_node(state: GraphState) -> GraphState:
        ws = state["wealth_state"]
        ws = graph._run_planning(ws)
        return {"wealth_state": ws}
    
    def mentor_node(state: GraphState) -> GraphState:
        ws = state["wealth_state"]
        ws = graph._run_mentor(ws)
        return {"wealth_state": ws}
    
    def log_node(state: GraphState) -> GraphState:
        ws = state["wealth_state"]
        ws = graph._log_decision(ws)
        return {"wealth_state": ws}
    
    # Build graph
    workflow = StateGraph(GraphState)
    
    workflow.add_node("analysts", analyst_node)
    workflow.add_node("debate", debate_node)
    workflow.add_node("planning", planning_node)
    workflow.add_node("mentor", mentor_node)
    workflow.add_node("log", log_node)
    
    workflow.set_entry_point("analysts")
    workflow.add_edge("analysts", "debate")
    workflow.add_edge("debate", "planning")
    workflow.add_edge("planning", "mentor")
    workflow.add_edge("mentor", "log")
    workflow.add_edge("log", END)
    
    return workflow.compile()
