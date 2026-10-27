"""Investor mentor personas for WealthAgents.

Each mentor is a persona that reinterprets the wealth plan through
their philosophy, voice, and decision framework.
"""

from wealthagents.mentors.base import MentorPersona
from wealthagents.mentors.registry import MentorRegistry
from wealthagents.mentors.personalities import (
    WarrenBuffett,
    BenjaminGraham,
    PeterLynch,
    JohnBogle,
    RayDalio,
    CathieWood,
    PaulTudorJones,
)

__all__ = [
    "MentorPersona",
    "MentorRegistry",
    "WarrenBuffett",
    "BenjaminGraham",
    "PeterLynch",
    "JohnBogle",
    "RayDalio",
    "CathieWood",
    "PaulTudorJones",
]
