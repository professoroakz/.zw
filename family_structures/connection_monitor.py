"""
ConnectionMonitor Entity

Checks on members regularly to ensure they are reunited or connected.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from .family_member import FamilyMember
from .family_unit import FamilyUnit


class ConnectionMonitor:
    """
    Monitors family member connections and ensures regular check-ins.
    
    This entity proactively identifies members who need attention and
    facilitates reunification and connection maintenance.
    """
    
    def __init__(
        self,
        check_interval_minutes: int = 60,
        attention_threshold_minutes: int = 120
    ):
        """
        Initialize the connection monitor.
        
        Args:
            check_interval_minutes: How often to check member status
            attention_threshold_minutes: Minutes before member needs attention
        """
        self.check_interval = timedelta(minutes=check_interval_minutes)
        self.attention_threshold = timedelta(minutes=attention_threshold_minutes)
        self.last_check = datetime.now()
        self.check_history: List[Dict] = []
        self.alert_callbacks: List[Callable] = []
        
    def register_alert_callback(self, callback: Callable) -> None:
        """
        Register a callback function to be called when issues are detected.
        
        Args:
            callback: Function to call with alert information
        """
        self.alert_callbacks.append(callback)
        
    def check_member(self, member: FamilyMember) -> Dict[str, any]:
        """
        Check an individual member's connection status.
        
        Args:
            member: FamilyMember to check
            
        Returns:
            Dictionary with check results and recommendations
        """
        now = datetime.now()
        time_since_check = now - member.last_checked
        
        result = {
            "member_id": member.member_id,
            "member_name": member.name,
            "timestamp": now,
            "time_since_last_check": time_since_check,
            "status": member.status,
            "is_isolated": member.is_isolated(),
            "connection_count": member.get_connection_count(),
            "needs_attention": False,
            "recommendations": []
        }
        
        # Check if member needs attention
        if time_since_check > self.attention_threshold:
            result["needs_attention"] = True
            result["recommendations"].append("Member hasn't been checked recently")
            member.update_status("needs_attention")
            
        # Check for isolation
        if member.is_isolated():
            result["needs_attention"] = True
            result["recommendations"].append("Member is isolated - needs connections")
            
        # Update member status
        member.last_checked = now
        if not result["needs_attention"] and member.status != "active":
            member.update_status("active")
            
        return result
        
    def check_unit(self, unit: FamilyUnit) -> Dict[str, any]:
        """
        Check all members in a family unit.
        
        Args:
            unit: FamilyUnit to check
            
        Returns:
            Dictionary with comprehensive check results
        """
        now = datetime.now()
        self.last_check = now
        
        member_results = []
        members_needing_attention = []
        isolated_members = []
        
        for member in unit.get_all_members():
            result = self.check_member(member)
            member_results.append(result)
            
            if result["needs_attention"]:
                members_needing_attention.append(member)
            if result["is_isolated"]:
                isolated_members.append(member)
                
        check_result = {
            "unit_id": unit.unit_id,
            "unit_name": unit.name,
            "timestamp": now,
            "total_members": unit.get_member_count(),
            "members_needing_attention": len(members_needing_attention),
            "isolated_members": len(isolated_members),
            "average_connections": unit.get_average_connections(),
            "member_results": member_results,
            "overall_health": self._calculate_health_score(unit)
        }
        
        # Log the check
        self.check_history.append({
            "timestamp": now,
            "unit_id": unit.unit_id,
            "summary": {
                "total": check_result["total_members"],
                "needing_attention": len(members_needing_attention),
                "isolated": len(isolated_members)
            }
        })
        
        # Trigger alerts if needed
        if members_needing_attention or isolated_members:
            self._trigger_alerts(check_result)
            
        return check_result
        
    def reunite_isolated_members(self, unit: FamilyUnit) -> List[Dict]:
        """
        Attempt to connect isolated members with others in the unit.
        
        Args:
            unit: FamilyUnit to process
            
        Returns:
            List of reunion actions taken
        """
        isolated = unit.get_isolated_members()
        well_connected = unit.get_well_connected_members(threshold=2)
        actions = []
        
        for isolated_member in isolated:
            if well_connected:
                # Connect to a well-connected member
                connector = well_connected[0]
                success = unit.connect_members(
                    isolated_member.member_id,
                    connector.member_id
                )
                if success:
                    actions.append({
                        "action": "reunite",
                        "isolated_member": isolated_member.name,
                        "connected_to": connector.name,
                        "timestamp": datetime.now()
                    })
                    isolated_member.log_communication(
                        f"Connected with {connector.name} via ConnectionMonitor"
                    )
            elif len(unit.get_all_members()) > 1:
                # Connect to any available member
                for potential_connection in unit.get_all_members():
                    if potential_connection.member_id != isolated_member.member_id:
                        unit.connect_members(
                            isolated_member.member_id,
                            potential_connection.member_id
                        )
                        actions.append({
                            "action": "reunite",
                            "isolated_member": isolated_member.name,
                            "connected_to": potential_connection.name,
                            "timestamp": datetime.now()
                        })
                        break
                        
        return actions
        
    def _calculate_health_score(self, unit: FamilyUnit) -> float:
        """
        Calculate overall health score for a unit (0-100).
        
        Args:
            unit: FamilyUnit to evaluate
            
        Returns:
            Health score from 0 (poor) to 100 (excellent)
        """
        if unit.get_member_count() == 0:
            return 0.0
            
        # Factors: connection density, isolation rate, active members
        isolation_rate = len(unit.get_isolated_members()) / unit.get_member_count()
        avg_connections = unit.get_average_connections()
        max_possible_connections = unit.get_member_count() - 1
        
        connection_score = (avg_connections / max_possible_connections) * 100 if max_possible_connections > 0 else 0
        isolation_penalty = isolation_rate * 50
        
        health_score = max(0, min(100, connection_score - isolation_penalty))
        return round(health_score, 2)
        
    def _trigger_alerts(self, check_result: Dict) -> None:
        """
        Trigger registered alert callbacks.
        
        Args:
            check_result: Results from unit check
        """
        for callback in self.alert_callbacks:
            try:
                callback(check_result)
            except Exception as e:
                print(f"Alert callback error: {e}")
                
    def get_check_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get history of checks performed.
        
        Args:
            limit: Optional limit on number of records to return
            
        Returns:
            List of historical check records
        """
        if limit:
            return self.check_history[-limit:]
        return self.check_history
