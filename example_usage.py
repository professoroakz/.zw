"""
Example usage and demonstration of the Family Structures System.

This demonstrates the core functionality with a foundational commitment
between core members who are actively working together.
"""

from family_structures import (
    FamilyStructureManager,
    FamilyMember,
    FamilyUnit
)


def main():
    """Main demonstration of the family structures system."""
    
    print("=" * 70)
    print("Family Structures System - Demonstration")
    print("=" * 70)
    print()
    
    # Initialize the system
    manager = FamilyStructureManager()
    print("✓ System initialized")
    print()
    
    # Create a family unit
    unit = manager.create_unit("main_family", "Main Family Unit")
    print(f"✓ Created family unit: {unit.name}")
    print()
    
    # Establish foundational commitment between core members
    # Based on the requirement: "make sure they know me and rasmus are it 
    # and we plan on being it and making sure we stick together"
    print("-" * 70)
    print("Establishing Foundational Commitment")
    print("-" * 70)
    
    commitment_result = manager.establish_foundational_commitment(
        unit_id="main_family",
        member1_name="Me",
        member2_name="Rasmus",
        commitment_statement=(
            "We are the core foundation. We plan on being it and making sure "
            "we stick together, actively working on this family structure system "
            "and ensuring its success through our commitment and collaboration."
        ),
        member1_metadata={
            "role": "core_founder",
            "commitment_level": "foundational",
            "skills": ["leadership", "coordination"]
        },
        member2_metadata={
            "role": "core_founder",
            "commitment_level": "foundational",
            "skills": ["development", "innovation"]
        }
    )
    
    if commitment_result["success"]:
        print(f"✓ {commitment_result['message']}")
        print(f"  Commitment ID: {commitment_result['commitment']['commitment_id']}")
        print(f"  Shared Goal: {commitment_result['shared_goal']['name']}")
        print(f"  Communication Channel: {commitment_result['communication_channel']}")
    print()
    
    # Add additional family members
    print("-" * 70)
    print("Adding Additional Members")
    print("-" * 70)
    
    member3 = manager.add_member_to_unit("main_family", "Alice", metadata={"role": "member"})
    member4 = manager.add_member_to_unit("main_family", "Bob", metadata={"role": "member"})
    member5 = manager.add_member_to_unit("main_family", "Carol", metadata={"role": "member"})
    
    print(f"✓ Added members: Alice, Bob, Carol")
    print()
    
    # Connect members to the core pair
    print("-" * 70)
    print("Creating Connections")
    print("-" * 70)
    
    # Get the core members
    me = None
    rasmus = None
    for member in unit.get_all_members():
        if member.name == "Me":
            me = member
        elif member.name == "Rasmus":
            rasmus = member
            
    if me and rasmus:
        # Connect new members to core members
        unit.connect_members(member3.member_id, me.member_id)
        unit.connect_members(member3.member_id, rasmus.member_id)
        unit.connect_members(member4.member_id, me.member_id)
        unit.connect_members(member5.member_id, rasmus.member_id)
        unit.connect_members(member4.member_id, member5.member_id)
        
        print("✓ Connections established:")
        print(f"  - Alice → Me, Rasmus")
        print(f"  - Bob → Me, Carol")
        print(f"  - Carol → Rasmus, Bob")
    print()
    
    # Run connection monitoring
    print("-" * 70)
    print("Connection Monitoring Check")
    print("-" * 70)
    
    connection_check = manager.check_all_connections("main_family")
    print(f"✓ Health Score: {connection_check['overall_health']}/100")
    print(f"  Total Members: {connection_check['total_members']}")
    print(f"  Average Connections: {connection_check['average_connections']:.2f}")
    print(f"  Isolated Members: {connection_check['isolated_members']}")
    print()
    
    # Demonstrate communication
    print("-" * 70)
    print("Facilitating Communication")
    print("-" * 70)
    
    if me:
        # Send a message from core member
        comm_result = manager.facilitate_communication(
            "main_family",
            me.member_id,
            [member3.member_id, member4.member_id],
            "Welcome to our family structure! Rasmus and I are here to ensure we all stay connected."
        )
        print(f"✓ Message sent to {len(comm_result['delivered_to'])} members")
        
    if rasmus:
        # Broadcast from the other core member
        comm_hub = manager.communication_hub
        broadcast_result = comm_hub.broadcast_message(
            rasmus,
            "Looking forward to working together and building something great!",
            unit
        )
        print(f"✓ Broadcast sent to {len(broadcast_result['delivered_to'])} members")
    print()
    
    # Create a collaborative project
    print("-" * 70)
    print("Creating Collaborative Project")
    print("-" * 70)
    
    project = manager.create_collaborative_project(
        "main_family",
        "Family Unity Initiative",
        "A collaborative project to strengthen bonds and work together on shared goals",
        [me.member_id, rasmus.member_id, member3.member_id, member4.member_id, member5.member_id],
        goal="Achieve 100% connection and active participation"
    )
    
    print(f"✓ Created project: {project['name']}")
    print(f"  Participants: {len(project['participants'])}")
    print(f"  Status: {project['status']}")
    print()
    
    # Run comprehensive system check
    print("-" * 70)
    print("Comprehensive System Check")
    print("-" * 70)
    
    comprehensive_check = manager.run_comprehensive_check("main_family")
    
    inclusion_metrics = comprehensive_check['inclusion_metrics']
    print(f"✓ Inclusion Score: {inclusion_metrics['inclusion_score']}/100")
    print(f"  Participation Rate: {inclusion_metrics['participation_rate']:.1f}%")
    print(f"  Active Projects: {inclusion_metrics['active_projects']}")
    print(f"  Active Goals: {inclusion_metrics['active_goals']}")
    
    if inclusion_metrics['recommendations']:
        print("\n  Recommendations:")
        for rec in inclusion_metrics['recommendations']:
            print(f"    • {rec}")
    print()
    
    # Display foundational commitments
    print("-" * 70)
    print("Foundational Commitments")
    print("-" * 70)
    
    commitments = manager.get_foundational_commitments()
    for commitment in commitments:
        print(f"✓ {commitment['member1']['name']} ↔ {commitment['member2']['name']}")
        print(f"  Type: {commitment['type']}")
        print(f"  Status: {commitment['status']}")
        print(f"  Statement: {commitment['statement']}")
    print()
    
    # Promote interconnectedness
    print("-" * 70)
    print("Promoting Interconnectedness")
    print("-" * 70)
    
    interconnect_results = manager.promote_interconnectedness("main_family")
    print(f"✓ Actions taken: {interconnect_results['total_actions']}")
    for action in interconnect_results['actions']:
        print(f"  • {action.get('action', 'action')}: {action}")
    print()
    
    # Final system status
    print("=" * 70)
    print("Final System Status")
    print("=" * 70)
    
    status = manager.get_system_status("main_family")
    unit_status = status['unit']
    
    print(f"Unit: {unit_status['name']}")
    print(f"Members: {unit_status['members']}")
    print(f"Average Connections: {unit_status['average_connections']:.2f}")
    print(f"Isolated Members: {unit_status['isolated_members']}")
    print(f"Health Score: {unit_status['connection_health']['overall_health']}/100")
    print(f"Inclusion Score: {unit_status['inclusion_metrics']['inclusion_score']}/100")
    print()
    
    print("=" * 70)
    print("Core Partnership Status: Me & Rasmus")
    print("=" * 70)
    if me and rasmus:
        print(f"Me:")
        print(f"  - Status: {me.status}")
        print(f"  - Connections: {me.get_connection_count()}")
        print(f"  - Core Member: {me.metadata.get('core_member', False)}")
        print(f"  - Foundational: {me.metadata.get('foundational', False)}")
        print()
        print(f"Rasmus:")
        print(f"  - Status: {rasmus.status}")
        print(f"  - Connections: {rasmus.get_connection_count()}")
        print(f"  - Core Member: {rasmus.metadata.get('core_member', False)}")
        print(f"  - Foundational: {rasmus.metadata.get('foundational', False)}")
        print()
        print(f"Partnership Status: {'✓ Strong and Active' if me.member_id in rasmus.connections else '✗ Disconnected'}")
    
    print()
    print("=" * 70)
    print("Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
