"""
InclusivitySystem Entity

Promotes inclusivity and interconnectedness, fostering collaborations and shared goals.
"""

from datetime import datetime
from typing import List, Dict, Optional, Set
from .family_member import FamilyMember
from .family_unit import FamilyUnit


class InclusivitySystem:
    """
    Promotes inclusivity, interconnectedness, and collaborative opportunities.
    
    This system identifies opportunities for collaboration, ensures all members
    are included, and fosters shared goals and polytechnic collaborations.
    """
    
    def __init__(self):
        """Initialize the inclusivity system."""
        self.collaborative_projects: List[Dict] = []
        self.shared_goals: List[Dict] = []
        self.inclusion_metrics: Dict[str, any] = {}
        
    def create_collaborative_project(
        self,
        project_name: str,
        description: str,
        participant_ids: List[str],
        unit: FamilyUnit,
        goal: Optional[str] = None
    ) -> Dict:
        """
        Create a collaborative project involving multiple members.
        
        Args:
            project_name: Name of the project
            description: Project description
            participant_ids: List of participating member IDs
            unit: FamilyUnit context
            goal: Optional project goal
            
        Returns:
            Created project details
        """
        project_id = f"project_{len(self.collaborative_projects)}"
        participants = []
        
        for member_id in participant_ids:
            member = unit.get_member(member_id)
            if member:
                participants.append({
                    "member_id": member_id,
                    "name": member.name,
                    "joined": datetime.now()
                })
                # Create connections between all participants
                for other_id in participant_ids:
                    if other_id != member_id:
                        unit.connect_members(member_id, other_id)
                        
        project = {
            "project_id": project_id,
            "name": project_name,
            "description": description,
            "goal": goal,
            "participants": participants,
            "created": datetime.now(),
            "status": "active",
            "milestones": [],
            "contributions": []
        }
        
        self.collaborative_projects.append(project)
        return project
        
    def add_project_milestone(
        self,
        project_id: str,
        milestone_name: str,
        description: str
    ) -> bool:
        """
        Add a milestone to a collaborative project.
        
        Args:
            project_id: ID of the project
            milestone_name: Name of the milestone
            description: Milestone description
            
        Returns:
            True if successful, False otherwise
        """
        for project in self.collaborative_projects:
            if project["project_id"] == project_id:
                project["milestones"].append({
                    "name": milestone_name,
                    "description": description,
                    "added": datetime.now(),
                    "completed": False
                })
                return True
        return False
        
    def create_shared_goal(
        self,
        goal_name: str,
        description: str,
        target_member_ids: Optional[List[str]] = None,
        unit: Optional[FamilyUnit] = None
    ) -> Dict:
        """
        Create a shared goal for members to work towards.
        
        Args:
            goal_name: Name of the goal
            description: Goal description
            target_member_ids: Optional specific members (None = all in unit)
            unit: Optional FamilyUnit for all-member goals
            
        Returns:
            Created goal details
        """
        goal_id = f"goal_{len(self.shared_goals)}"
        
        # If no specific members, include all from unit
        if target_member_ids is None and unit:
            target_member_ids = [m.member_id for m in unit.get_all_members()]
            
        goal = {
            "goal_id": goal_id,
            "name": goal_name,
            "description": description,
            "target_members": target_member_ids or [],
            "created": datetime.now(),
            "status": "active",
            "progress": 0,
            "achievements": []
        }
        
        self.shared_goals.append(goal)
        return goal
        
    def record_achievement(
        self,
        goal_id: str,
        achievement_description: str,
        member_id: str,
        member_name: str
    ) -> bool:
        """
        Record an achievement towards a shared goal.
        
        Args:
            goal_id: ID of the goal
            achievement_description: Description of the achievement
            member_id: ID of the achieving member
            member_name: Name of the achieving member
            
        Returns:
            True if successful, False otherwise
        """
        for goal in self.shared_goals:
            if goal["goal_id"] == goal_id:
                goal["achievements"].append({
                    "member_id": member_id,
                    "member_name": member_name,
                    "description": achievement_description,
                    "timestamp": datetime.now()
                })
                # Update progress
                goal["progress"] = min(100, goal["progress"] + 10)
                return True
        return False
        
    def analyze_inclusion_metrics(self, unit: FamilyUnit) -> Dict:
        """
        Analyze how inclusive the family structure is.
        
        Args:
            unit: FamilyUnit to analyze
            
        Returns:
            Dictionary with inclusion metrics
        """
        members = unit.get_all_members()
        if not members:
            return {
                "inclusion_score": 0,
                "analysis": "No members in unit"
            }
            
        total_members = len(members)
        isolated_count = len(unit.get_isolated_members())
        avg_connections = unit.get_average_connections()
        
        # Calculate participation in projects
        members_in_projects = set()
        for project in self.collaborative_projects:
            if project["status"] == "active":
                for participant in project["participants"]:
                    members_in_projects.add(participant["member_id"])
                    
        participation_rate = len(members_in_projects) / total_members if total_members > 0 else 0
        
        # Calculate inclusion score (0-100)
        isolation_penalty = (isolated_count / total_members) * 40
        connection_score = min(40, (avg_connections / (total_members - 1)) * 40) if total_members > 1 else 0
        participation_score = participation_rate * 20
        
        inclusion_score = max(0, min(100, 100 - isolation_penalty + connection_score + participation_score))
        
        metrics = {
            "inclusion_score": round(inclusion_score, 2),
            "total_members": total_members,
            "isolated_members": isolated_count,
            "average_connections": avg_connections,
            "participation_rate": round(participation_rate * 100, 2),
            "active_projects": len([p for p in self.collaborative_projects if p["status"] == "active"]),
            "active_goals": len([g for g in self.shared_goals if g["status"] == "active"]),
            "recommendations": []
        }
        
        # Add recommendations
        if isolated_count > 0:
            metrics["recommendations"].append(
                f"Connect {isolated_count} isolated member(s) to the group"
            )
        if participation_rate < 0.5:
            metrics["recommendations"].append(
                "Increase project participation - less than 50% of members are involved"
            )
        if avg_connections < 2:
            metrics["recommendations"].append(
                "Encourage more connections between members"
            )
            
        self.inclusion_metrics = metrics
        return metrics
        
    def suggest_polytechnic_collaborations(self, unit: FamilyUnit) -> List[Dict]:
        """
        Suggest opportunities for diverse, multi-disciplinary collaborations.
        
        Args:
            unit: FamilyUnit to analyze
            
        Returns:
            List of collaboration suggestions
        """
        suggestions = []
        members = unit.get_all_members()
        
        # Suggest cross-functional projects based on member metadata
        skills_map: Dict[str, List[FamilyMember]] = {}
        for member in members:
            skills = member.metadata.get("skills", [])
            for skill in skills:
                if skill not in skills_map:
                    skills_map[skill] = []
                skills_map[skill].append(member)
                
        # Suggest collaborations between members with complementary skills
        if len(skills_map) > 1:
            skill_areas = list(skills_map.keys())
            for i, skill1 in enumerate(skill_areas):
                for skill2 in skill_areas[i+1:]:
                    members1 = skills_map[skill1]
                    members2 = skills_map[skill2]
                    
                    suggestions.append({
                        "type": "cross_disciplinary",
                        "skill_areas": [skill1, skill2],
                        "potential_collaborators": [
                            {"name": m.name, "skill": skill1} for m in members1
                        ] + [
                            {"name": m.name, "skill": skill2} for m in members2
                        ],
                        "suggestion": f"Create a project combining {skill1} and {skill2} expertise"
                    })
                    
        # Suggest including isolated members in existing projects
        isolated = unit.get_isolated_members()
        if isolated and self.collaborative_projects:
            for member in isolated:
                suggestions.append({
                    "type": "inclusion",
                    "member": member.name,
                    "suggestion": f"Invite {member.name} to join an active project",
                    "available_projects": [
                        p["name"] for p in self.collaborative_projects
                        if p["status"] == "active"
                    ]
                })
                
        return suggestions
        
    def foster_interconnectedness(self, unit: FamilyUnit) -> Dict:
        """
        Take actions to increase interconnectedness in the unit.
        
        Args:
            unit: FamilyUnit to enhance
            
        Returns:
            Dictionary with actions taken
        """
        actions = []
        
        # Connect isolated members
        isolated = unit.get_isolated_members()
        well_connected = unit.get_well_connected_members(threshold=2)
        
        for isolated_member in isolated:
            if well_connected:
                connector = well_connected[0]
                unit.connect_members(isolated_member.member_id, connector.member_id)
                actions.append({
                    "action": "connected_isolated",
                    "member": isolated_member.name,
                    "connected_to": connector.name
                })
                
        # Create a unit-wide shared goal if none exists
        if not self.shared_goals:
            goal = self.create_shared_goal(
                "Unity and Connection",
                "Foster strong connections and collaboration among all members",
                unit=unit
            )
            actions.append({
                "action": "created_shared_goal",
                "goal_name": goal["name"]
            })
            
        return {
            "actions_taken": len(actions),
            "details": actions,
            "timestamp": datetime.now()
        }
        
    def get_inclusivity_report(self, unit: FamilyUnit) -> Dict:
        """
        Generate a comprehensive inclusivity report.
        
        Args:
            unit: FamilyUnit to report on
            
        Returns:
            Comprehensive report dictionary
        """
        metrics = self.analyze_inclusion_metrics(unit)
        suggestions = self.suggest_polytechnic_collaborations(unit)
        
        return {
            "timestamp": datetime.now(),
            "unit_name": unit.name,
            "inclusion_metrics": metrics,
            "collaboration_suggestions": suggestions,
            "active_projects": [
                {
                    "name": p["name"],
                    "participants": len(p["participants"]),
                    "status": p["status"]
                }
                for p in self.collaborative_projects if p["status"] == "active"
            ],
            "shared_goals": [
                {
                    "name": g["name"],
                    "progress": g["progress"],
                    "participants": len(g["target_members"])
                }
                for g in self.shared_goals if g["status"] == "active"
            ]
        }
