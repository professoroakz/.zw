"""
Family Structures System

A robust system for managing family structures with features for:
- Regular member check-ins and connection monitoring
- Proactive communication breakdown prevention
- Inclusivity and interconnectedness promotion
- Extensible and maintainable architecture
"""

from .family_member import FamilyMember
from .family_unit import FamilyUnit
from .connection_monitor import ConnectionMonitor
from .communication_hub import CommunicationHub
from .inclusivity_system import InclusivitySystem
from .family_structure_manager import FamilyStructureManager

__version__ = "1.0.0"
__all__ = [
    "FamilyMember",
    "FamilyUnit",
    "ConnectionMonitor",
    "CommunicationHub",
    "InclusivitySystem",
    "FamilyStructureManager",
]
