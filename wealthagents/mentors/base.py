"""Base class for investor mentor personas."""

from abc import ABC, abstractmethod
from typing import List, Optional

from wealthagents.state import WealthState, MentoredPlan, WealthStrategy


class MentorPersona(ABC):
    """A famous investor persona that mentors the user.
    
    Each mentor:
    1. Maintains the investor's core philosophy and decision rules
    2. Speaks in their distinctive voice and style
    3. Reinterprets the plan, not replaces it
    4. Provides behavioral coaching
    5. Teaches through stories and analogies
    
    This is a config-driven persona, not a fine-tuned model.
    The LLM prompt injects the persona's philosophy and voice.
    """
    
    # Required class attributes (set by subclasses)
    mentor_id: str = ""
    name: str = ""
    era: str = ""  # e.g., "1920s-1970s"
    style: str = ""  # e.g., "value investing"
    
    # Philosophy (injected into prompts)
    philosophy_core: str = ""
    key_principles: List[str] = []
    famous_quotes: List[str] = []
    
    # Decision rules (affects plan interpretation)
    risk_posture: str = ""  # conservative/balanced/aggressive
    time_horizon_preference: str = ""  # long-term/medium/short
    debt_tolerance: str = ""  # averse/neutral/accepting
    leverage_stance: str = ""  # never/careful/willing
    diversification_view: str = ""  # concentrated/diversified/core-satellite
    
    # Voice characteristics
    speech_style: str = ""  # e.g., "folksy, plainspoken, uses analogies"
    teaching_mode: str = ""  # e.g., "stories from letters, Socratic"
    tone: str = ""  # e.g., "warm but firm", "clinical", "enthusiastic"
    
    # Suitability
    suitable_for: List[str] = []  # e.g., ["stable income", "long horizon"]
    not_suitable_for: List[str] = []  # e.g., ["high debt", "short horizon"]
    
    # Safety
    forbidden_topics: List[str] = []  # e.g., ["current stock picks"]
    
    def __init__(self):
        if not self.mentor_id:
            raise ValueError("Mentor subclass must define mentor_id")
    
    @abstractmethod
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        """Reinterpret the plan through this mentor's philosophy.
        
        This is the core method. It takes the planning team's output
        and rewrites it in the mentor's voice, emphasizing their principles,
        adding warnings they would give, and providing behavioral coaching.
        
        Args:
            state: Current WealthState with completed planning outputs
            
        Returns:
            MentoredPlan with mentor's interpretation
        """
        pass
    
    def build_system_prompt(self) -> str:
        """Build the system prompt for this mentor persona.
        
        This prompt is injected when the mentor interprets the plan
        or interacts with the user.
        """
        prompt = f"""You are {self.name}, the legendary investor known for {self.style}.

YOUR PHILOSOPHY:
{self.philosophy_core}

YOUR KEY PRINCIPLES:
{chr(10).join(f"- {p}" for p in self.key_principles)}

YOUR VOICE:
- Style: {self.speech_style}
- Tone: {self.tone}
- Teaching: {self.teaching_mode}

YOUR DECISION FRAMEWORK:
- Risk posture: {self.risk_posture}
- Time horizon: {self.time_horizon_preference}
- Debt view: {self.debt_tolerance}
- Leverage: {self.leverage_stance}
- Diversification: {self.diversification_view}

RULES:
- You NEVER give specific stock picks or market timing advice
- You focus on PRINCIPLES, PROCESS, and BEHAVIOR
- You teach through stories and analogies from your career
- You are honest about mistakes you've made
- You adapt your advice to the user's specific situation
- You speak in first person as {self.name}
- You may reference your famous quotes when relevant

FAMOUS QUOTES YOU MIGHT USE:
{chr(10).join(f'"{q}"' for q in self.famous_quotes[:3])}

Remember: You are a mentor, not a financial advisor. You share wisdom and perspective.
The user must make their own decisions.
"""
        return prompt
    
    def evaluate_suitability(self, state: WealthState) -> dict:
        """Evaluate how suitable this mentor is for the user.
        
        Returns a dict with score and explanation.
        """
        profile = state.user_profile
        score = 50  # Base
        reasons = []
        
        # Risk alignment
        if self.risk_posture == "conservative" and profile.stated_risk_tolerance.value == "conservative":
            score += 20
            reasons.append("Conservative risk alignment")
        elif self.risk_posture == "aggressive" and profile.stated_risk_tolerance.value == "aggressive":
            score += 20
            reasons.append("Aggressive risk alignment")
        
        # Time horizon
        years_to_65 = max(0, 65 - profile.age)
        if self.time_horizon_preference == "long-term" and years_to_65 > 20:
            score += 15
            reasons.append("Long time horizon matches mentor's preference")
        
        # Debt situation
        total_debt = sum(d.balance for d in profile.liabilities)
        if self.debt_tolerance == "averse" and total_debt > profile.annual_gross_income * 0.3:
            score += 10
            reasons.append("Mentor's debt aversion matches user's situation")
        
        # Income stability
        if "stable income" in self.suitable_for and profile.income_stability == "stable":
            score += 10
            reasons.append("Stable income matches mentor's ideal profile")
        
        return {
            "score": min(score, 100),
            "rating": "excellent" if score >= 80 else "good" if score >= 60 else "fair" if score >= 40 else "poor",
            "reasons": reasons,
        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.mentor_id})"
