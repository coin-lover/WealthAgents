"""Mentor registry for loading and managing investor personas."""

from typing import Dict, List, Type, Optional

from wealthagents.mentors.base import MentorPersona
from wealthagents.mentors.personalities import (
    WarrenBuffett,
    BenjaminGraham,
    PeterLynch,
    JohnBogle,
    RayDalio,
    CathieWood,
    PaulTudorJones,
)


class MentorRegistry:
    """Registry of available mentor personas.
    
    Provides lookup by ID and listing of all available mentors.
    New mentors can be registered dynamically.
    """
    
    _mentors: Dict[str, Type[MentorPersona]] = {}
    
    @classmethod
    def register(cls, mentor_class: Type[MentorPersona]) -> None:
        """Register a new mentor persona."""
        instance = mentor_class()
        cls._mentors[instance.mentor_id] = mentor_class
    
    @classmethod
    def get(cls, mentor_id: str) -> Optional[MentorPersona]:
        """Get a mentor instance by ID.
        
        Returns:
            MentorPersona instance, or None if not found.
        """
        mentor_class = cls._mentors.get(mentor_id)
        if mentor_class:
            return mentor_class()
        return None
    
    @classmethod
    def list_mentors(cls) -> List[dict]:
        """List all registered mentors with metadata.
        
        Returns:
            List of dicts with mentor metadata.
        """
        result = []
        for mentor_id, mentor_class in cls._mentors.items():
            instance = mentor_class()
            result.append({
                "id": instance.mentor_id,
                "name": instance.name,
                "era": instance.era,
                "style": instance.style,
                "risk_posture": instance.risk_posture,
                "time_horizon": instance.time_horizon_preference,
                "suitable_for": instance.suitable_for,
                "description": instance.philosophy_core[:150] + "...",
            })
        return result
    
    @classmethod
    def get_default(cls) -> MentorPersona:
        """Get the default mentor (Warren Buffett)."""
        return WarrenBuffett()
    
    @classmethod
    def _load_defaults(cls) -> None:
        """Load default mentors into registry."""
        defaults = [
            WarrenBuffett,
            BenjaminGraham,
            PeterLynch,
            JohnBogle,
            RayDalio,
            CathieWood,
            PaulTudorJones,
        ]
        for mentor_class in defaults:
            cls.register(mentor_class)


# Auto-load defaults on import
MentorRegistry._load_defaults()
