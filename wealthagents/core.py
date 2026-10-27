"""Main WealthAgents API.

User-facing class for running wealth evaluations and switching mentors.
"""

from typing import Optional, List
from datetime import datetime

from wealthagents.state import WealthState, UserProfile
from wealthagents.graph import WealthAgentsGraph
from wealthagents.mentors.registry import MentorRegistry
from wealthagents.connections import AccountConnectionManager, get_connection_mode


class WealthAgents:
    """Personal wealth mentor AI.
    
    The main interface for users. Initialize with a profile and mentor,
    then call evaluate() to generate a wealth plan.
    
    Example:
        agent = WealthAgents(user_profile=profile, mentor="warren_buffett")
        result = agent.evaluate()
        print(result.mentored_plan.mentor_voice_narrative)
        
        # Switch mentors and compare
        result_bogle = agent.with_mentor("john_bogle").evaluate()
    """
    
    def __init__(
        self,
        user_profile: UserProfile,
        mentor: str = "warren_buffett",
        state: Optional[WealthState] = None,
    ):
        """Initialize WealthAgents.
        
        Args:
            user_profile: The user's financial profile
            mentor: Mentor persona ID (default: warren_buffett)
            state: Optional existing WealthState to continue from
        """
        self.user_profile = user_profile
        self.mentor_id = mentor
        
        if state:
            self.state = state
            self.state.user_profile = user_profile
        else:
            self.state = WealthState(
                user_id=user_profile.user_id,
                user_profile=user_profile,
                mentor_id=mentor,
            )
        
        self._graph = WealthAgentsGraph(mentor_id=mentor)
        self._connection_manager = AccountConnectionManager(user_profile)
    
    @property
    def connection_mode(self) -> str:
        """Return the account connection mode for this user.
        
        Returns:
            "plaid_auto" if automatic account syncing is available.
            "manual_input" if the user must enter data manually.
        """
        return self._connection_manager.mode
    
    def get_connection_message(self) -> str:
        """Get a user-facing message about account connections."""
        return self._connection_manager.get_connection_message()
    
    def evaluate(self, trigger: str = "user_request") -> WealthState:
        """Run a full wealth evaluation.
        
        Executes the complete multi-agent pipeline:
        analysts -> debate -> planning -> mentor
        
        Args:
            trigger: What triggered this evaluation
            
        Returns:
            Updated WealthState with all outputs
        """
        self.state.evaluation_trigger = trigger
        self.state.timestamp = datetime.now()
        
        # Run graph
        self.state = self._graph.run(self.state)
        
        # Increment version
        self.state.version += 1
        
        return self.state
    
    def with_mentor(self, mentor_id: str) -> "WealthAgents":
        """Create a new instance with a different mentor.
        
        Preserves user profile and state but changes the mentor persona.
        Useful for comparing different mentor perspectives.
        
        Args:
            mentor_id: New mentor persona ID
            
        Returns:
            New WealthAgents instance
        """
        if not MentorRegistry.get(mentor_id):
            available = [m["id"] for m in MentorRegistry.list_mentors()]
            raise ValueError(f"Unknown mentor '{mentor_id}'. Available: {available}")
        
        new_agent = WealthAgents(
            user_profile=self.user_profile,
            mentor=mentor_id,
            state=self.state,
        )
        new_agent.state.mentor_id = mentor_id
        return new_agent
    
    def get_plan_summary(self) -> str:
        """Get a human-readable summary of the current plan.
        
        Returns:
            Formatted summary string
        """
        if not self.state.mentored_plan:
            return "No plan generated yet. Call evaluate() first."
        
        mp = self.state.mentored_plan
        s = self.state.strategy
        
        lines = [
            f"{'='*60}",
            f"WEALTH PLAN FOR {self.user_profile.user_id}",
            f"Mentor: {mp.mentor_name}",
            f"Version: {self.state.version}",
            f"{'='*60}",
            "",
        ]
        
        if s:
            lines.extend([
                "STRATEGY:",
                f"  Emergency Fund: ${s.emergency_fund_target:,.0f} ({s.emergency_fund_months:.0f} months)",
                f"  Debt Strategy: {s.debt_strategy}",
                f"  Monthly Investment: ${s.monthly_investment:,.0f}",
                f"  Allocation: {', '.join(f'{k}={v:.0%}' for k, v in s.recommended_allocation.items())}",
                "",
                "ACTION ITEMS:",
            ])
            for i, action in enumerate(s.action_items, 1):
                lines.append(f"  {i}. [{action.priority}] {action.action} ({action.timeline})")
        
        lines.extend([
            "",
            "MENTOR'S WORDS:",
            f"  {mp.mentor_voice_narrative[:300]}...",
            "",
            f"{'='*60}",
        ])
        
        return "\n".join(lines)
    
    def compare_mentors(self, mentor_ids: Optional[List[str]] = None) -> dict:
        """Compare plans from multiple mentors.
        
        Runs evaluation with each mentor and returns comparison.
        
        Args:
            mentor_ids: List of mentor IDs to compare (default: all)
            
        Returns:
            Dict mapping mentor_id to plan summary
        """
        if mentor_ids is None:
            mentor_ids = [m["id"] for m in MentorRegistry.list_mentors()]
        
        results = {}
        for mid in mentor_ids:
            agent = self.with_mentor(mid)
            state = agent.evaluate(trigger=f"mentor_comparison_{mid}")
            
            if state.mentored_plan:
                results[mid] = {
                    "mentor_name": state.mentored_plan.mentor_name,
                    "philosophy": state.mentored_plan.philosophy_applied,
                    "strategy_summary": state.strategy.strategy_summary if state.strategy else "N/A",
                    "key_warnings": state.mentored_plan.mentor_specific_warnings,
                    "narrative_preview": state.mentored_plan.mentor_voice_narrative[:200],
                }
        
        return results
    
    @staticmethod
    def list_mentors() -> List[dict]:
        """List all available mentor personas.
        
        Returns:
            List of mentor metadata dicts
        """
        return MentorRegistry.list_mentors()
    
    def __repr__(self) -> str:
        return f"WealthAgents(user={self.user_profile.user_id}, mentor={self.mentor_id}, version={self.state.version})"
