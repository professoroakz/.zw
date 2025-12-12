# Family Structures System

A robust and extensible system for managing family structures with features for regular member check-ins, proactive communication breakdown prevention, and promotion of inclusivity and interconnectedness.

## Overview

The Family Structures System provides a comprehensive framework for:

1. **Regular Member Check-ins**: Monitoring family members to ensure they remain connected and reunited
2. **Communication Breakdown Prevention**: Proactive mechanisms to maintain healthy dialogue and prevent isolation
3. **Inclusivity and Interconnectedness**: Promoting collaboration, shared goals, and polytechnic partnerships
4. **Extensibility and Maintainability**: Clean, well-structured code following best practices

## Architecture

The system is built with a modular, object-oriented architecture consisting of:

### Core Entities

- **FamilyMember**: Represents an individual with unique identification, status tracking, and connection management
- **FamilyUnit**: Manages collections of members and their relationships
- **ConnectionMonitor**: Regularly checks members and identifies those needing attention or reunion
- **CommunicationHub**: Facilitates communication and detects/prevents breakdowns
- **InclusivitySystem**: Promotes inclusivity, creates collaborative projects, and fosters shared goals
- **FamilyStructureManager**: Main orchestrator coordinating all system components

## Installation

1. Clone the repository:
```bash
git clone https://github.com/professoroakz/.zw.git
cd .zw
```

2. The system uses Python 3.6+ with no external dependencies (only standard library)

## Quick Start

```python
from family_structures import FamilyStructureManager

# Initialize the system
manager = FamilyStructureManager()

# Create a family unit
unit = manager.create_unit("my_family", "My Family")

# Establish a foundational commitment between core members
commitment = manager.establish_foundational_commitment(
    unit_id="my_family",
    member1_name="Me",
    member2_name="Partner",
    commitment_statement="We are committed to sticking together and working on this"
)

# Add additional members
alice = manager.add_member_to_unit("my_family", "Alice")
bob = manager.add_member_to_unit("my_family", "Bob")

# Run comprehensive check
status = manager.run_comprehensive_check("my_family")
print(f"Health Score: {status['connection_check']['overall_health']}/100")
```

## Core Features

### 1. Foundational Commitments

Establish strong, permanent bonds between core members who are committed to working together:

```python
result = manager.establish_foundational_commitment(
    unit_id="my_family",
    member1_name="Me",
    member2_name="Rasmus",
    commitment_statement="We plan on being it and making sure we stick together"
)

# This creates:
# - Bidirectional connections between members
# - A shared goal for the partnership
# - A dedicated communication channel
# - Permanent commitment record
```

### 2. Connection Monitoring

Automatically check members and identify those needing attention:

```python
# Run connection check
check_results = manager.check_all_connections("my_family")

# Reunite isolated members
reunion_actions = manager.reunite_isolated_members("my_family")
```

The ConnectionMonitor:
- Tracks when members were last checked
- Identifies isolated members (no connections)
- Calculates health scores (0-100)
- Provides recommendations for improvement
- Automatically reunites isolated members with well-connected ones

### 3. Communication Facilitation

Prevent communication breakdowns and maintain healthy dialogue:

```python
# Send message between members
manager.facilitate_communication(
    "my_family",
    from_member_id=sender_id,
    to_member_ids=[receiver_id],
    message="Checking in!"
)

# Detect communication gaps
gaps = manager.communication_hub.detect_communication_gaps(unit)

# Get reconnection suggestions
suggestions = manager.communication_hub.suggest_reconnections(unit)
```

Features:
- Direct messaging between members
- Broadcast messages to all members
- Communication channels for groups
- Gap detection (identifies inactive members)
- Automated check-ins
- Communication statistics

### 4. Inclusivity and Collaboration

Promote interconnectedness and shared goals:

```python
# Create collaborative project
project = manager.create_collaborative_project(
    "my_family",
    "Family Unity Initiative",
    "Working together on shared goals",
    participant_ids=[member1_id, member2_id, member3_id],
    goal="Achieve 100% connection"
)

# Analyze inclusion metrics
metrics = manager.inclusivity_system.analyze_inclusion_metrics(unit)
print(f"Inclusion Score: {metrics['inclusion_score']}/100")

# Get collaboration suggestions
suggestions = manager.inclusivity_system.suggest_polytechnic_collaborations(unit)
```

Features:
- Collaborative project creation
- Shared goal management
- Inclusion metric analysis (0-100 score)
- Polytechnic collaboration suggestions
- Automatic interconnectedness promotion

### 5. Comprehensive System Checks

Run full analysis of family structure health:

```python
results = manager.run_comprehensive_check("my_family")

# Returns:
# - Connection health status
# - Communication gaps and suggestions
# - Inclusion metrics
# - Collaboration opportunities
# - Active foundational commitments
```

## Example Usage

See `example_usage.py` for a complete demonstration including:
- System initialization
- Foundational commitment establishment
- Member addition and connection
- Communication facilitation
- Collaborative project creation
- Comprehensive health checks

Run the example:
```bash
python example_usage.py
```

## Running Tests

The system includes comprehensive unit tests:

```bash
python -m pytest tests/test_family_structures.py -v
```

Or using unittest:
```bash
python -m unittest tests.test_family_structures
```

## API Reference

### FamilyStructureManager

Main entry point for the system.

#### Methods

- `create_unit(unit_id, name, metadata=None)` - Create a new family unit
- `add_member_to_unit(unit_id, name, member_id=None, metadata=None)` - Add member to unit
- `establish_foundational_commitment(unit_id, member1_name, member2_name, commitment_statement, ...)` - Create core partnership
- `check_all_connections(unit_id)` - Run connection monitoring
- `reunite_isolated_members(unit_id)` - Connect isolated members
- `facilitate_communication(unit_id, from_member_id, to_member_ids, message)` - Send messages
- `create_collaborative_project(unit_id, project_name, description, participant_ids, goal=None)` - Create project
- `run_comprehensive_check(unit_id)` - Full system analysis
- `get_system_status(unit_id=None)` - Get current status
- `promote_interconnectedness(unit_id)` - Take proactive actions to improve connections

### FamilyMember

Represents an individual family member.

#### Attributes

- `member_id` - Unique identifier
- `name` - Member name
- `status` - Current status (active, inactive, needs_attention)
- `connections` - Set of connected member IDs
- `metadata` - Additional information dictionary

#### Methods

- `add_connection(member_id)` - Add connection to another member
- `remove_connection(member_id)` - Remove connection
- `is_isolated()` - Check if member has no connections
- `get_connection_count()` - Get number of connections
- `log_communication(message, timestamp=None)` - Log communication event

### FamilyUnit

Manages a collection of family members.

#### Methods

- `add_member(member)` - Add member to unit
- `remove_member(member_id)` - Remove member
- `connect_members(member_id1, member_id2, bidirectional=True)` - Connect two members
- `get_isolated_members()` - Get members with no connections
- `get_average_connections()` - Calculate average connections per member

## Design Principles

1. **Modularity**: Each component has a single, well-defined responsibility
2. **Extensibility**: Easy to add new features without modifying existing code
3. **Type Safety**: Uses Python type hints throughout
4. **Documentation**: Comprehensive docstrings for all classes and methods
5. **Testability**: Designed for easy unit testing with no external dependencies
6. **Best Practices**: Follows PEP 8 style guidelines

## Use Cases

- **Family Coordination**: Keep family members connected and engaged
- **Team Building**: Build strong team connections and collaborations
- **Community Management**: Foster inclusive, interconnected communities
- **Support Networks**: Ensure no one is isolated and everyone is connected
- **Project Management**: Coordinate collaborative efforts with shared goals

## Contributing

This system is designed to be extensible. To add new features:

1. Create new entity classes in the `family_structures/` directory
2. Import and integrate in `FamilyStructureManager`
3. Add corresponding tests in `tests/`
4. Update documentation

## License

This project is part of the `.zw` repository. See repository for license details.

## Support

For issues, questions, or contributions, please refer to the repository at: https://github.com/professoroakz/.zw
