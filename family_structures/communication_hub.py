"""
CommunicationHub Entity

Proactively prevents communication breakdowns among members.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from .family_member import FamilyMember
from .family_unit import FamilyUnit


class CommunicationHub:
    """
    Facilitates communication and prevents breakdowns among family members.
    
    This entity monitors communication patterns, identifies potential issues,
    and provides mechanisms for maintaining healthy dialogue.
    """
    
    def __init__(self, inactivity_threshold_days: int = 7):
        """
        Initialize the communication hub.
        
        Args:
            inactivity_threshold_days: Days of inactivity before flagging
        """
        self.inactivity_threshold = timedelta(days=inactivity_threshold_days)
        self.messages: List[Dict] = []
        self.communication_channels: Dict[str, Dict] = {}
        
    def send_message(
        self,
        from_member: FamilyMember,
        to_member_ids: List[str],
        message: str,
        unit: FamilyUnit
    ) -> Dict:
        """
        Send a message from one member to others.
        
        Args:
            from_member: Member sending the message
            to_member_ids: List of recipient member IDs
            message: Message content
            unit: FamilyUnit context
            
        Returns:
            Dictionary with delivery results
        """
        timestamp = datetime.now()
        delivered_to = []
        failed = []
        
        for to_id in to_member_ids:
            to_member = unit.get_member(to_id)
            if to_member:
                # Log communication for both members
                from_member.log_communication(
                    f"Sent to {to_member.name}: {message}",
                    timestamp
                )
                to_member.log_communication(
                    f"Received from {from_member.name}: {message}",
                    timestamp
                )
                delivered_to.append(to_id)
            else:
                failed.append(to_id)
                
        # Store message in hub
        message_record = {
            "message_id": f"msg_{len(self.messages)}",
            "from": from_member.member_id,
            "from_name": from_member.name,
            "to": to_member_ids,
            "delivered_to": delivered_to,
            "failed": failed,
            "message": message,
            "timestamp": timestamp
        }
        self.messages.append(message_record)
        
        return message_record
        
    def broadcast_message(
        self,
        from_member: FamilyMember,
        message: str,
        unit: FamilyUnit
    ) -> Dict:
        """
        Broadcast a message to all members in the unit.
        
        Args:
            from_member: Member sending the message
            message: Message content
            unit: FamilyUnit to broadcast to
            
        Returns:
            Dictionary with broadcast results
        """
        all_member_ids = [
            m.member_id for m in unit.get_all_members()
            if m.member_id != from_member.member_id
        ]
        return self.send_message(from_member, all_member_ids, message, unit)
        
    def create_communication_channel(
        self,
        channel_name: str,
        member_ids: List[str],
        purpose: str = ""
    ) -> str:
        """
        Create a dedicated communication channel for specific members.
        
        Args:
            channel_name: Name for the channel
            member_ids: List of member IDs in the channel
            purpose: Optional description of channel purpose
            
        Returns:
            Channel ID
        """
        channel_id = f"channel_{len(self.communication_channels)}"
        self.communication_channels[channel_id] = {
            "channel_id": channel_id,
            "name": channel_name,
            "members": set(member_ids),
            "purpose": purpose,
            "created": datetime.now(),
            "messages": [],
            "active": True
        }
        return channel_id
        
    def send_channel_message(
        self,
        channel_id: str,
        from_member: FamilyMember,
        message: str,
        unit: FamilyUnit
    ) -> bool:
        """
        Send a message to a specific communication channel.
        
        Args:
            channel_id: ID of the channel
            from_member: Member sending the message
            message: Message content
            unit: FamilyUnit context
            
        Returns:
            True if successful, False otherwise
        """
        if channel_id not in self.communication_channels:
            return False
            
        channel = self.communication_channels[channel_id]
        if from_member.member_id not in channel["members"]:
            return False
            
        timestamp = datetime.now()
        channel_message = {
            "from": from_member.member_id,
            "from_name": from_member.name,
            "message": message,
            "timestamp": timestamp
        }
        channel["messages"].append(channel_message)
        
        # Notify all channel members
        for member_id in channel["members"]:
            if member_id != from_member.member_id:
                member = unit.get_member(member_id)
                if member:
                    member.log_communication(
                        f"[{channel['name']}] {from_member.name}: {message}",
                        timestamp
                    )
                    
        return True
        
    def detect_communication_gaps(self, unit: FamilyUnit) -> List[Dict]:
        """
        Detect members or connections with communication gaps.
        
        Args:
            unit: FamilyUnit to analyze
            
        Returns:
            List of identified communication gaps
        """
        gaps = []
        now = datetime.now()
        
        for member in unit.get_all_members():
            if member.communication_log:
                last_comm = member.communication_log[-1]["timestamp"]
                time_since = now - last_comm
                
                if time_since > self.inactivity_threshold:
                    gaps.append({
                        "type": "member_inactivity",
                        "member_id": member.member_id,
                        "member_name": member.name,
                        "days_inactive": time_since.days,
                        "severity": "high" if time_since.days > 14 else "medium"
                    })
            else:
                gaps.append({
                    "type": "no_communication",
                    "member_id": member.member_id,
                    "member_name": member.name,
                    "severity": "high"
                })
                
        return gaps
        
    def suggest_reconnections(self, unit: FamilyUnit) -> List[Dict]:
        """
        Suggest members who should reconnect based on communication patterns.
        
        Args:
            unit: FamilyUnit to analyze
            
        Returns:
            List of reconnection suggestions
        """
        suggestions = []
        gaps = self.detect_communication_gaps(unit)
        
        for gap in gaps:
            if gap["type"] in ["member_inactivity", "no_communication"]:
                member_id = gap["member_id"]
                member = unit.get_member(member_id)
                
                if member and member.connections:
                    # Suggest reaching out to connected members
                    for connected_id in member.connections:
                        connected = unit.get_member(connected_id)
                        if connected:
                            suggestions.append({
                                "member": member.name,
                                "should_contact": connected.name,
                                "reason": f"No recent communication ({gap.get('days_inactive', 'unknown')} days)",
                                "priority": gap["severity"]
                            })
                            
        return suggestions
        
    def facilitate_check_in(
        self,
        member: FamilyMember,
        unit: FamilyUnit,
        auto_message: str = "Checking in - staying connected!"
    ) -> Dict:
        """
        Facilitate an automated check-in for a member.
        
        Args:
            member: Member to check in
            unit: FamilyUnit context
            auto_message: Default check-in message
            
        Returns:
            Results of the check-in
        """
        if not member.connections:
            return {
                "success": False,
                "reason": "Member has no connections to check in with"
            }
            
        # Send check-in to all connections
        connected_ids = list(member.connections)
        result = self.send_message(member, connected_ids, auto_message, unit)
        
        return {
            "success": True,
            "member": member.name,
            "contacted": len(result["delivered_to"]),
            "message": auto_message,
            "timestamp": datetime.now()
        }
        
    def get_communication_stats(self, unit: FamilyUnit) -> Dict:
        """
        Get communication statistics for the unit.
        
        Args:
            unit: FamilyUnit to analyze
            
        Returns:
            Dictionary with communication statistics
        """
        total_messages = len(self.messages)
        active_channels = sum(1 for c in self.communication_channels.values() if c["active"])
        gaps = self.detect_communication_gaps(unit)
        
        return {
            "total_messages": total_messages,
            "active_channels": active_channels,
            "total_channels": len(self.communication_channels),
            "communication_gaps": len(gaps),
            "members_with_gaps": len([g for g in gaps if g["type"] == "member_inactivity"]),
            "members_never_communicated": len([g for g in gaps if g["type"] == "no_communication"])
        }
