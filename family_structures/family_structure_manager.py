"""
FamilyStructureManager

Main orchestrator for the family structures system.
Coordinates all entities and provides a unified interface.
"""

from datetime import datetime
from typing import Dict, List, Optional
from .family_member import FamilyMember
from .family_unit import FamilyUnit
from .connection_monitor import ConnectionMonitor
from .communication_hub import CommunicationHub
from .inclusivity_system import InclusivitySystem


class FamilyStructureManager:
    """
    Main manager coordinating all aspects of the family structures system.
    
    This class provides a unified interface for managing family units,
    monitoring connections, facilitating communication, and promoting inclusivity.
    """
    
    def __init__(self):
        """Initialize the family structure manager."""
        self.units: Dict[str, FamilyUnit] = {}
        self.connection_monitor = ConnectionMonitor()
        self.communication_hub = CommunicationHub()
        self.inclusivity_system = InclusivitySystem()
        self.initialized = datetime.now()
        
        # Initialize foundational commitments
        self._foundational_commitments = []
        
    def create_unit(self, unit_id: str, name: str, metadata: Optional[Dict] = None) -> FamilyUnit:
        """
        Create a new family unit.
        
        Args:
            unit_id: Unique identifier for the unit
            name: Name of the unit
            metadata: Optional metadata
            
        Returns:
            Created FamilyUnit
        """
        if unit_id in self.units:
            raise ValueError(f"Unit {unit_id} already exists")
            
        unit = FamilyUnit(unit_id, name, metadata)
        self.units[unit_id] = unit
        return unit
        
    def get_unit(self, unit_id: str) -> Optional[FamilyUnit]:
        """
        Get a family unit by ID.
        
        Args:
            unit_id: ID of the unit
            
        Returns:
            FamilyUnit or None if not found
        """
        return self.units.get(unit_id)
        
    def add_member_to_unit(
        self,
        unit_id: str,
        name: str,
        member_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[FamilyMember]:
        """
        Add a member to a unit.
        
        Args:
            unit_id: ID of the unit
            name: Name of the member
            member_id: Optional member ID
            metadata: Optional metadata
            
        Returns:
            Created FamilyMember or None if unit not found
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return None
            
        member = FamilyMember(name, member_id, metadata)
        unit.add_member(member)
        return member
        
    def establish_foundational_commitment(
        self,
        unit_id: str,
        member1_name: str,
        member2_name: str,
        commitment_statement: str,
        member1_metadata: Optional[Dict] = None,
        member2_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Establish a foundational commitment between two core members.
        
        This creates a strong, permanent bond between two members who are
        committed to sticking together and actively working on the family structure.
        
        Args:
            unit_id: ID of the unit
            member1_name: Name of first core member
            member2_name: Name of second core member
            commitment_statement: Statement of commitment
            member1_metadata: Optional metadata for first member
            member2_metadata: Optional metadata for second member
            
        Returns:
            Dictionary with commitment details
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return {"success": False, "reason": "Unit not found"}
            
        # Create or get members
        member1 = None
        member2 = None
        
        for member in unit.get_all_members():
            if member.name.lower() == member1_name.lower():
                member1 = member
            if member.name.lower() == member2_name.lower():
                member2 = member
                
        if not member1:
            member1 = FamilyMember(member1_name, metadata=member1_metadata or {})
            member1.metadata["core_member"] = True
            member1.metadata["foundational"] = True
            unit.add_member(member1)
            
        if not member2:
            member2 = FamilyMember(member2_name, metadata=member2_metadata or {})
            member2.metadata["core_member"] = True
            member2.metadata["foundational"] = True
            unit.add_member(member2)
            
        # Establish strong bidirectional connection
        unit.connect_members(member1.member_id, member2.member_id, bidirectional=True)
        
        # Log the commitment
        commitment_log = f"Foundational commitment: {commitment_statement}"
        member1.log_communication(commitment_log)
        member2.log_communication(commitment_log)
        
        # Store commitment in system
        commitment = {
            "commitment_id": f"commit_{len(self._foundational_commitments)}",
            "unit_id": unit_id,
            "member1": {
                "id": member1.member_id,
                "name": member1.name
            },
            "member2": {
                "id": member2.member_id,
                "name": member2.name
            },
            "statement": commitment_statement,
            "established": datetime.now(),
            "status": "active",
            "type": "foundational"
        }
        
        self._foundational_commitments.append(commitment)
        
        # Create a shared goal for the committed members
        goal = self.inclusivity_system.create_shared_goal(
            f"{member1_name} & {member2_name} Partnership",
            commitment_statement,
            [member1.member_id, member2.member_id]
        )
        
        # Create a communication channel for them
        channel_id = self.communication_hub.create_communication_channel(
            f"{member1_name}-{member2_name} Core Channel",
            [member1.member_id, member2.member_id],
            "Dedicated channel for foundational partnership communication"
        )
        
        return {
            "success": True,
            "commitment": commitment,
            "shared_goal": goal,
            "communication_channel": channel_id,
            "message": f"Foundational commitment established between {member1_name} and {member2_name}"
        }
        
    def get_foundational_commitments(self) -> List[Dict]:
        """
        Get all foundational commitments in the system.
        
        Returns:
            List of foundational commitments
        """
        return self._foundational_commitments
        
    def check_all_connections(self, unit_id: str) -> Dict:
        """
        Run connection monitoring for a unit.
        
        Args:
            unit_id: ID of the unit to check
            
        Returns:
            Check results
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return {"error": "Unit not found"}
            
        return self.connection_monitor.check_unit(unit)
        
    def reunite_isolated_members(self, unit_id: str) -> List[Dict]:
        """
        Reunite isolated members in a unit.
        
        Args:
            unit_id: ID of the unit
            
        Returns:
            List of reunion actions
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return []
            
        return self.connection_monitor.reunite_isolated_members(unit)
        
    def facilitate_communication(
        self,
        unit_id: str,
        from_member_id: str,
        to_member_ids: List[str],
        message: str
    ) -> Dict:
        """
        Facilitate communication between members.
        
        Args:
            unit_id: ID of the unit
            from_member_id: ID of sender
            to_member_ids: IDs of recipients
            message: Message content
            
        Returns:
            Communication results
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return {"error": "Unit not found"}
            
        from_member = unit.get_member(from_member_id)
        if not from_member:
            return {"error": "Sender not found"}
            
        return self.communication_hub.send_message(from_member, to_member_ids, message, unit)
        
    def create_collaborative_project(
        self,
        unit_id: str,
        project_name: str,
        description: str,
        participant_ids: List[str],
        goal: Optional[str] = None
    ) -> Dict:
        """
        Create a collaborative project in a unit.
        
        Args:
            unit_id: ID of the unit
            project_name: Name of the project
            description: Project description
            participant_ids: List of participant IDs
            goal: Optional goal
            
        Returns:
            Created project
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return {"error": "Unit not found"}
            
        return self.inclusivity_system.create_collaborative_project(
            project_name, description, participant_ids, unit, goal
        )
        
    def get_system_status(self, unit_id: Optional[str] = None) -> Dict:
        """
        Get comprehensive system status.
        
        Args:
            unit_id: Optional specific unit ID, or None for all units
            
        Returns:
            System status dictionary
        """
        status = {
            "timestamp": datetime.now(),
            "system_initialized": self.initialized,
            "total_units": len(self.units),
            "foundational_commitments": len(self._foundational_commitments)
        }
        
        if unit_id:
            unit = self.get_unit(unit_id)
            if unit:
                status["unit"] = {
                    "id": unit.unit_id,
                    "name": unit.name,
                    "members": unit.get_member_count(),
                    "average_connections": unit.get_average_connections(),
                    "isolated_members": len(unit.get_isolated_members()),
                    "connection_health": self.connection_monitor.check_unit(unit),
                    "communication_stats": self.communication_hub.get_communication_stats(unit),
                    "inclusion_metrics": self.inclusivity_system.analyze_inclusion_metrics(unit)
                }
        else:
            # Summary of all units
            status["units"] = [
                {
                    "id": u.unit_id,
                    "name": u.name,
                    "members": u.get_member_count()
                }
                for u in self.units.values()
            ]
            
        return status
        
    def run_comprehensive_check(self, unit_id: str) -> Dict:
        """
        Run a comprehensive check on all aspects of a unit.
        
        Args:
            unit_id: ID of the unit to check
            
        Returns:
            Comprehensive check results
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return {"error": "Unit not found"}
            
        return {
            "timestamp": datetime.now(),
            "unit_id": unit_id,
            "unit_name": unit.name,
            "connection_check": self.connection_monitor.check_unit(unit),
            "communication_gaps": self.communication_hub.detect_communication_gaps(unit),
            "reconnection_suggestions": self.communication_hub.suggest_reconnections(unit),
            "inclusion_metrics": self.inclusivity_system.analyze_inclusion_metrics(unit),
            "collaboration_suggestions": self.inclusivity_system.suggest_polytechnic_collaborations(unit),
            "foundational_commitments": [
                c for c in self._foundational_commitments
                if c["unit_id"] == unit_id and c["status"] == "active"
            ]
        }
        
    def promote_interconnectedness(self, unit_id: str) -> Dict:
        """
        Take proactive actions to promote interconnectedness in a unit.
        
        Args:
            unit_id: ID of the unit
            
        Returns:
            Results of actions taken
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return {"error": "Unit not found"}
            
        results = {
            "timestamp": datetime.now(),
            "unit_id": unit_id,
            "actions": []
        }
        
        # Reunite isolated members
        reunion_actions = self.connection_monitor.reunite_isolated_members(unit)
        if reunion_actions:
            results["actions"].extend(reunion_actions)
            
        # Foster inclusivity
        inclusivity_actions = self.inclusivity_system.foster_interconnectedness(unit)
        results["actions"].extend(inclusivity_actions.get("details", []))
        
        # Facilitate check-ins for members with communication gaps
        gaps = self.communication_hub.detect_communication_gaps(unit)
        for gap in gaps:
            member = unit.get_member(gap["member_id"])
            if member and member.connections:
                check_in = self.communication_hub.facilitate_check_in(member, unit)
                if check_in.get("success"):
                    results["actions"].append({
                        "action": "facilitated_check_in",
                        "member": member.name,
                        "contacted": check_in.get("contacted", 0)
                    })
                    
        results["total_actions"] = len(results["actions"])
        return results
