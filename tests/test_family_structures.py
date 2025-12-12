"""
Unit tests for the Family Structures System.
"""

import unittest
from datetime import datetime, timedelta
from family_structures import (
    FamilyMember,
    FamilyUnit,
    ConnectionMonitor,
    CommunicationHub,
    InclusivitySystem,
    FamilyStructureManager
)


class TestFamilyMember(unittest.TestCase):
    """Tests for FamilyMember entity."""
    
    def test_member_creation(self):
        """Test creating a family member."""
        member = FamilyMember("John")
        self.assertEqual(member.name, "John")
        self.assertEqual(member.status, "active")
        self.assertIsNotNone(member.member_id)
        
    def test_add_connection(self):
        """Test adding connections between members."""
        member1 = FamilyMember("Alice")
        member2 = FamilyMember("Bob")
        
        member1.add_connection(member2.member_id)
        self.assertIn(member2.member_id, member1.connections)
        self.assertEqual(member1.get_connection_count(), 1)
        
    def test_isolation_detection(self):
        """Test detecting isolated members."""
        member = FamilyMember("Isolated")
        self.assertTrue(member.is_isolated())
        
        member.add_connection("someone")
        self.assertFalse(member.is_isolated())
        
    def test_status_update(self):
        """Test updating member status."""
        member = FamilyMember("Test")
        member.update_status("needs_attention")
        self.assertEqual(member.status, "needs_attention")
        
    def test_communication_log(self):
        """Test logging communication."""
        member = FamilyMember("Logger")
        member.log_communication("Test message")
        self.assertEqual(len(member.communication_log), 1)
        self.assertEqual(member.communication_log[0]["message"], "Test message")


class TestFamilyUnit(unittest.TestCase):
    """Tests for FamilyUnit entity."""
    
    def test_unit_creation(self):
        """Test creating a family unit."""
        unit = FamilyUnit("unit1", "Test Unit")
        self.assertEqual(unit.unit_id, "unit1")
        self.assertEqual(unit.name, "Test Unit")
        self.assertEqual(unit.get_member_count(), 0)
        
    def test_add_member(self):
        """Test adding members to unit."""
        unit = FamilyUnit("unit1", "Test Unit")
        member = FamilyMember("Alice")
        
        unit.add_member(member)
        self.assertEqual(unit.get_member_count(), 1)
        self.assertIsNotNone(unit.get_member(member.member_id))
        
    def test_connect_members(self):
        """Test connecting members within unit."""
        unit = FamilyUnit("unit1", "Test Unit")
        member1 = FamilyMember("Alice")
        member2 = FamilyMember("Bob")
        
        unit.add_member(member1)
        unit.add_member(member2)
        
        success = unit.connect_members(member1.member_id, member2.member_id)
        self.assertTrue(success)
        self.assertIn(member2.member_id, member1.connections)
        self.assertIn(member1.member_id, member2.connections)
        
    def test_get_isolated_members(self):
        """Test finding isolated members."""
        unit = FamilyUnit("unit1", "Test Unit")
        member1 = FamilyMember("Isolated")
        member2 = FamilyMember("Connected1")
        member3 = FamilyMember("Connected2")
        
        unit.add_member(member1)
        unit.add_member(member2)
        unit.add_member(member3)
        
        unit.connect_members(member2.member_id, member3.member_id)
        
        isolated = unit.get_isolated_members()
        self.assertEqual(len(isolated), 1)
        self.assertEqual(isolated[0].name, "Isolated")
        
    def test_average_connections(self):
        """Test calculating average connections."""
        unit = FamilyUnit("unit1", "Test Unit")
        member1 = FamilyMember("A")
        member2 = FamilyMember("B")
        member3 = FamilyMember("C")
        
        unit.add_member(member1)
        unit.add_member(member2)
        unit.add_member(member3)
        
        unit.connect_members(member1.member_id, member2.member_id)
        unit.connect_members(member1.member_id, member3.member_id)
        
        # member1 has 2 connections, member2 has 1, member3 has 1
        # Average = 4/3 = 1.33...
        avg = unit.get_average_connections()
        self.assertAlmostEqual(avg, 1.33, places=1)


class TestConnectionMonitor(unittest.TestCase):
    """Tests for ConnectionMonitor entity."""
    
    def test_monitor_creation(self):
        """Test creating a connection monitor."""
        monitor = ConnectionMonitor()
        self.assertIsNotNone(monitor.check_interval)
        self.assertIsNotNone(monitor.attention_threshold)
        
    def test_check_member(self):
        """Test checking individual member."""
        monitor = ConnectionMonitor()
        member = FamilyMember("Test")
        
        result = monitor.check_member(member)
        self.assertIn("member_id", result)
        self.assertIn("needs_attention", result)
        self.assertIn("is_isolated", result)
        
    def test_check_unit(self):
        """Test checking entire unit."""
        monitor = ConnectionMonitor()
        unit = FamilyUnit("unit1", "Test Unit")
        
        member1 = FamilyMember("A")
        member2 = FamilyMember("B")
        unit.add_member(member1)
        unit.add_member(member2)
        
        result = monitor.check_unit(unit)
        self.assertEqual(result["total_members"], 2)
        self.assertIn("overall_health", result)
        
    def test_reunite_isolated(self):
        """Test reuniting isolated members."""
        monitor = ConnectionMonitor()
        unit = FamilyUnit("unit1", "Test Unit")
        
        isolated = FamilyMember("Isolated")
        connected1 = FamilyMember("Connected1")
        connected2 = FamilyMember("Connected2")
        
        unit.add_member(isolated)
        unit.add_member(connected1)
        unit.add_member(connected2)
        
        unit.connect_members(connected1.member_id, connected2.member_id)
        
        actions = monitor.reunite_isolated_members(unit)
        self.assertGreater(len(actions), 0)
        self.assertFalse(isolated.is_isolated())


class TestCommunicationHub(unittest.TestCase):
    """Tests for CommunicationHub entity."""
    
    def test_hub_creation(self):
        """Test creating a communication hub."""
        hub = CommunicationHub()
        self.assertIsNotNone(hub.inactivity_threshold)
        self.assertEqual(len(hub.messages), 0)
        
    def test_send_message(self):
        """Test sending messages."""
        hub = CommunicationHub()
        unit = FamilyUnit("unit1", "Test Unit")
        
        sender = FamilyMember("Alice")
        receiver = FamilyMember("Bob")
        
        unit.add_member(sender)
        unit.add_member(receiver)
        
        result = hub.send_message(sender, [receiver.member_id], "Hello!", unit)
        
        self.assertEqual(len(result["delivered_to"]), 1)
        self.assertIn(receiver.member_id, result["delivered_to"])
        self.assertEqual(len(sender.communication_log), 1)
        
    def test_broadcast_message(self):
        """Test broadcasting to all members."""
        hub = CommunicationHub()
        unit = FamilyUnit("unit1", "Test Unit")
        
        sender = FamilyMember("Alice")
        member2 = FamilyMember("Bob")
        member3 = FamilyMember("Carol")
        
        unit.add_member(sender)
        unit.add_member(member2)
        unit.add_member(member3)
        
        result = hub.broadcast_message(sender, "Hello everyone!", unit)
        self.assertEqual(len(result["delivered_to"]), 2)
        
    def test_create_channel(self):
        """Test creating communication channel."""
        hub = CommunicationHub()
        
        channel_id = hub.create_communication_channel(
            "Test Channel",
            ["member1", "member2"],
            "Testing"
        )
        
        self.assertIsNotNone(channel_id)
        self.assertIn(channel_id, hub.communication_channels)


class TestInclusivitySystem(unittest.TestCase):
    """Tests for InclusivitySystem entity."""
    
    def test_system_creation(self):
        """Test creating inclusivity system."""
        system = InclusivitySystem()
        self.assertEqual(len(system.collaborative_projects), 0)
        self.assertEqual(len(system.shared_goals), 0)
        
    def test_create_project(self):
        """Test creating collaborative project."""
        system = InclusivitySystem()
        unit = FamilyUnit("unit1", "Test Unit")
        
        member1 = FamilyMember("Alice")
        member2 = FamilyMember("Bob")
        unit.add_member(member1)
        unit.add_member(member2)
        
        project = system.create_collaborative_project(
            "Test Project",
            "A test project",
            [member1.member_id, member2.member_id],
            unit
        )
        
        self.assertEqual(project["name"], "Test Project")
        self.assertEqual(len(project["participants"]), 2)
        
    def test_create_shared_goal(self):
        """Test creating shared goals."""
        system = InclusivitySystem()
        
        goal = system.create_shared_goal(
            "Unity Goal",
            "Achieve unity",
            ["member1", "member2"]
        )
        
        self.assertEqual(goal["name"], "Unity Goal")
        self.assertEqual(len(goal["target_members"]), 2)
        
    def test_analyze_inclusion(self):
        """Test analyzing inclusion metrics."""
        system = InclusivitySystem()
        unit = FamilyUnit("unit1", "Test Unit")
        
        member1 = FamilyMember("Alice")
        member2 = FamilyMember("Bob")
        unit.add_member(member1)
        unit.add_member(member2)
        unit.connect_members(member1.member_id, member2.member_id)
        
        metrics = system.analyze_inclusion_metrics(unit)
        
        self.assertIn("inclusion_score", metrics)
        self.assertIn("total_members", metrics)
        self.assertGreaterEqual(metrics["inclusion_score"], 0)
        self.assertLessEqual(metrics["inclusion_score"], 100)


class TestFamilyStructureManager(unittest.TestCase):
    """Tests for FamilyStructureManager orchestrator."""
    
    def test_manager_creation(self):
        """Test creating the manager."""
        manager = FamilyStructureManager()
        self.assertIsNotNone(manager.connection_monitor)
        self.assertIsNotNone(manager.communication_hub)
        self.assertIsNotNone(manager.inclusivity_system)
        
    def test_create_unit(self):
        """Test creating a unit through manager."""
        manager = FamilyStructureManager()
        unit = manager.create_unit("unit1", "Test Unit")
        
        self.assertEqual(unit.unit_id, "unit1")
        self.assertIsNotNone(manager.get_unit("unit1"))
        
    def test_add_member_to_unit(self):
        """Test adding member through manager."""
        manager = FamilyStructureManager()
        manager.create_unit("unit1", "Test Unit")
        
        member = manager.add_member_to_unit("unit1", "Alice")
        self.assertIsNotNone(member)
        self.assertEqual(member.name, "Alice")
        
    def test_foundational_commitment(self):
        """Test establishing foundational commitment."""
        manager = FamilyStructureManager()
        manager.create_unit("unit1", "Test Unit")
        
        result = manager.establish_foundational_commitment(
            "unit1",
            "Me",
            "Rasmus",
            "We are committed to working together"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("commitment", result)
        self.assertIn("shared_goal", result)
        
        commitments = manager.get_foundational_commitments()
        self.assertEqual(len(commitments), 1)
        
    def test_comprehensive_check(self):
        """Test running comprehensive check."""
        manager = FamilyStructureManager()
        manager.create_unit("unit1", "Test Unit")
        manager.add_member_to_unit("unit1", "Alice")
        manager.add_member_to_unit("unit1", "Bob")
        
        result = manager.run_comprehensive_check("unit1")
        
        self.assertIn("connection_check", result)
        self.assertIn("inclusion_metrics", result)
        self.assertIn("communication_gaps", result)
        
    def test_system_status(self):
        """Test getting system status."""
        manager = FamilyStructureManager()
        manager.create_unit("unit1", "Test Unit")
        
        status = manager.get_system_status()
        self.assertEqual(status["total_units"], 1)


if __name__ == "__main__":
    unittest.main()
