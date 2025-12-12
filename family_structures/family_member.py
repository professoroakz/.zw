"""
FamilyMember Entity

Represents an individual member within the family structure system.
"""

from datetime import datetime
from typing import Optional, Dict, Any, Set
from uuid import uuid4


class FamilyMember:
    """
    Represents a family member with unique identification and status tracking.
    
    Attributes:
        member_id: Unique identifier for the member
        name: Name of the family member
        status: Current connection status (active, inactive, needs_attention)
        last_checked: Timestamp of last check-in
        metadata: Additional member information
        connections: Set of member IDs this member is connected to
    """
    
    def __init__(
        self,
        name: str,
        member_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a family member.
        
        Args:
            name: Name of the family member
            member_id: Optional unique identifier (auto-generated if not provided)
            metadata: Optional additional member information
        """
        self.member_id = member_id or str(uuid4())
        self.name = name
        self.status = "active"
        self.last_checked = datetime.now()
        self.metadata = metadata or {}
        self.connections: Set[str] = set()
        self.communication_log: list = []
        
    def update_status(self, status: str) -> None:
        """
        Update the member's connection status.
        
        Args:
            status: New status (active, inactive, needs_attention)
        """
        if status not in ["active", "inactive", "needs_attention"]:
            raise ValueError(f"Invalid status: {status}")
        self.status = status
        self.last_checked = datetime.now()
        
    def add_connection(self, member_id: str) -> None:
        """
        Add a connection to another family member.
        
        Args:
            member_id: ID of the member to connect with
        """
        self.connections.add(member_id)
        
    def remove_connection(self, member_id: str) -> None:
        """
        Remove a connection to another family member.
        
        Args:
            member_id: ID of the member to disconnect from
        """
        self.connections.discard(member_id)
        
    def log_communication(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """
        Log a communication event for this member.
        
        Args:
            message: Description of the communication
            timestamp: Optional timestamp (defaults to now)
        """
        self.communication_log.append({
            "message": message,
            "timestamp": timestamp or datetime.now()
        })
        
    def get_connection_count(self) -> int:
        """Get the number of connections this member has."""
        return len(self.connections)
        
    def is_isolated(self) -> bool:
        """Check if the member has no connections."""
        return len(self.connections) == 0
        
    def __repr__(self) -> str:
        return f"FamilyMember(id={self.member_id}, name={self.name}, status={self.status})"
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert member to dictionary representation."""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "status": self.status,
            "last_checked": self.last_checked.isoformat(),
            "metadata": self.metadata,
            "connections": list(self.connections),
            "connection_count": self.get_connection_count(),
            "is_isolated": self.is_isolated()
        }
