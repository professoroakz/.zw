"""
FamilyUnit Entity

Manages a collection of family members and their relationships.
"""

from typing import Dict, List, Optional, Set
from .family_member import FamilyMember


class FamilyUnit:
    """
    Manages a family unit containing multiple members and their relationships.
    
    Attributes:
        unit_id: Unique identifier for this family unit
        name: Name of the family unit
        members: Dictionary of member_id to FamilyMember objects
        unit_metadata: Additional unit information
    """
    
    def __init__(self, unit_id: str, name: str, metadata: Optional[Dict] = None):
        """
        Initialize a family unit.
        
        Args:
            unit_id: Unique identifier for the unit
            name: Name of the family unit
            metadata: Optional additional unit information
        """
        self.unit_id = unit_id
        self.name = name
        self.members: Dict[str, FamilyMember] = {}
        self.unit_metadata = metadata or {}
        
    def add_member(self, member: FamilyMember) -> None:
        """
        Add a member to the family unit.
        
        Args:
            member: FamilyMember object to add
        """
        if member.member_id in self.members:
            raise ValueError(f"Member {member.member_id} already exists in unit")
        self.members[member.member_id] = member
        
    def remove_member(self, member_id: str) -> Optional[FamilyMember]:
        """
        Remove a member from the family unit.
        
        Args:
            member_id: ID of the member to remove
            
        Returns:
            The removed FamilyMember object, or None if not found
        """
        # Remove all connections to this member
        if member_id in self.members:
            for other_member in self.members.values():
                other_member.remove_connection(member_id)
            return self.members.pop(member_id)
        return None
        
    def get_member(self, member_id: str) -> Optional[FamilyMember]:
        """
        Get a member by ID.
        
        Args:
            member_id: ID of the member to retrieve
            
        Returns:
            FamilyMember object or None if not found
        """
        return self.members.get(member_id)
        
    def connect_members(self, member_id1: str, member_id2: str, bidirectional: bool = True) -> bool:
        """
        Create a connection between two members.
        
        Args:
            member_id1: ID of first member
            member_id2: ID of second member
            bidirectional: Whether to create connection in both directions
            
        Returns:
            True if connection was successful, False otherwise
        """
        member1 = self.members.get(member_id1)
        member2 = self.members.get(member_id2)
        
        if not member1 or not member2:
            return False
            
        member1.add_connection(member_id2)
        if bidirectional:
            member2.add_connection(member_id1)
        return True
        
    def get_all_members(self) -> List[FamilyMember]:
        """Get all members in the unit."""
        return list(self.members.values())
        
    def get_member_count(self) -> int:
        """Get the total number of members."""
        return len(self.members)
        
    def get_isolated_members(self) -> List[FamilyMember]:
        """Get all members with no connections."""
        return [member for member in self.members.values() if member.is_isolated()]
        
    def get_well_connected_members(self, threshold: int = 3) -> List[FamilyMember]:
        """
        Get members with connections above a threshold.
        
        Args:
            threshold: Minimum number of connections
            
        Returns:
            List of well-connected members
        """
        return [
            member for member in self.members.values()
            if member.get_connection_count() >= threshold
        ]
        
    def get_average_connections(self) -> float:
        """Calculate the average number of connections per member."""
        if not self.members:
            return 0.0
        total_connections = sum(member.get_connection_count() for member in self.members.values())
        return total_connections / len(self.members)
        
    def __repr__(self) -> str:
        return f"FamilyUnit(id={self.unit_id}, name={self.name}, members={self.get_member_count()})"
        
    def to_dict(self) -> Dict:
        """Convert unit to dictionary representation."""
        return {
            "unit_id": self.unit_id,
            "name": self.name,
            "member_count": self.get_member_count(),
            "average_connections": self.get_average_connections(),
            "isolated_members": len(self.get_isolated_members()),
            "metadata": self.unit_metadata,
            "members": [member.to_dict() for member in self.members.values()]
        }
