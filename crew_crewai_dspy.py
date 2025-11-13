#!/usr/bin/env python3
"""
CrewAI crew with DSPy-enhanced agents.
This hybrid approach provides:
1. Full CrewAI orchestration (agents, tasks, tools)
2. DSPy few-shot optimized prompts
3. Complete AgentOps tracking (tools, agents, tasks, LLM calls, costs)
4. RAG integration for context enhancement
"""
from crewai import Crew, Process, Task
from agents_crewai_dspy import (
    create_product_manager,
    create_architect,
    create_engineer,
    create_qa_engineer,
    create_tech_writer,
)
import config


def create_tasks_dspy(project_idea: str) -> list[Task]:
    """
    Create tasks with DSPy-enhanced descriptions.
    Tasks use the enhanced agents from agents_crewai_dspy.
    """

    # Task 1: Create PRD
    prd_task = Task(
        description=f"""Create a comprehensive Product Requirements Document (PRD) for the following project:

PROJECT IDEA: {project_idea}

INSTRUCTIONS:
1. FIRST, use the retrieve_context tool to search for similar PRDs and best practices
2. THEN, create a PRD following the example structure you've been trained on

Your PRD MUST include these sections:
1. Project Overview
   - Project name and description
   - Target users
   - Key objectives

2. Functional Requirements (use FR-1, FR-2, etc.)
   - Core features (must-have)
   - Nice-to-have features
   - User stories

3. Non-Functional Requirements (use NFR-1, NFR-2, etc.)
   - Performance expectations (with numbers)
   - Security requirements
   - Scalability considerations

4. Success Metrics
   - KPIs to measure success (specific and measurable)
   - Acceptance criteria

5. Constraints and Assumptions
   - Technical constraints
   - Timeline considerations
   - Resource constraints

Save the PRD to 'prd.md' using the file_writer tool.""",
        expected_output="A comprehensive PRD document saved to workspace/prd.md following best practices",
        agent=create_product_manager(),
    )

    # Task 2: Design Architecture
    arch_task = Task(
        description="""Based on the PRD, design a detailed system architecture.

INSTRUCTIONS:
1. Read the PRD from 'prd.md' using file_reader tool
2. Use retrieve_context tool to find architecture patterns and best practices
3. Design architecture following the example structure you've been trained on

Your architecture document MUST include:
1. System Overview
   - High-level architecture diagram (described in text/ASCII)
   - Key components and their responsibilities
   - Component interaction flow

2. Technology Stack
   - Programming language(s) with version
   - Frameworks and libraries (with justification)
   - Database choice and rationale
   - Development and testing tools

3. Component Design
   - Clear layer separation (e.g., CLI, Business Logic, Data)
   - Each component's responsibility
   - APIs and interfaces

4. Data Models
   - Key entities and relationships
   - Data structures (with code examples)
   - Database schema if applicable

5. File Structure
   - Complete project structure
   - Directory organization with descriptions
   - Key files and their purposes

Save your architecture to 'architecture.md' using the file_writer tool.""",
        expected_output="A detailed architecture document saved to workspace/architecture.md with complete system design",
        agent=create_architect(),
    )

    # Task 3: Implement Code
    impl_task = Task(
        description="""Implement the core functionality based on the architecture and PRD.

INSTRUCTIONS:
1. Read the PRD from 'prd.md'
2. Read the architecture from 'architecture.md'
3. Use retrieve_context tool to find code examples and patterns
4. Create the project structure EXACTLY as specified in architecture
5. Implement core features

Your implementation MUST:
1. Create ALL directories specified in the architecture using directory_creator tool
2. Implement at least 2-3 core features from the PRD
3. Follow the file structure from the architecture document
4. Include proper error handling for edge cases
5. Add inline comments for complex logic
6. Follow coding best practices (PEP 8 for Python, etc.)
7. Include type hints if using Python
8. Make code testable (avoid tight coupling)

Create all necessary source files using the file_writer tool.
Focus on quality over quantity - better to have 2 well-implemented features than 5 poor ones.""",
        expected_output="Core implementation files created in the workspace following the architecture structure",
        agent=create_engineer(),
    )

    # Task 4: Create Tests
    test_task = Task(
        description="""Create a comprehensive testing strategy and test cases.

INSTRUCTIONS:
1. Read the implementation files from the workspace
2. Understand what functionality was implemented
3. Create thorough test documentation

Your deliverables MUST include:
1. Test Plan (save to 'test_plan.md')
   - Testing approach and strategy
   - Types of tests (unit, integration, manual)
   - Test coverage goals (aim for 80%+)
   - Testing tools and frameworks

2. Test Cases (save to 'test_cases.md')
   - Happy path scenarios (expected usage)
   - Edge cases (empty inputs, large inputs, special characters)
   - Error conditions (invalid inputs, missing files, network errors)
   - Boundary conditions
   - For EACH test case include:
     * Test ID
     * Description
     * Preconditions
     * Steps
     * Expected result

3. Sample Unit Tests (save to 'tests.py' or include in test_cases.md)
   - Example unit tests for core functionality
   - Test structure using pytest or unittest
   - Clear assertions and expected outcomes

Use file_writer tool to save all test documentation.""",
        expected_output="Complete testing documentation saved to workspace: test_plan.md and test_cases.md with comprehensive test coverage",
        agent=create_qa_engineer(),
    )

    # Task 5: Create Documentation
    docs_task = Task(
        description="""Create comprehensive project documentation.

INSTRUCTIONS:
1. Read ALL project files from workspace (PRD, architecture, implementation, tests)
2. Create user-friendly documentation

Your documentation MUST include:
1. README.md
   - Project title with one-line description
   - Features list (bullet points)
   - Installation instructions (step-by-step)
   - Usage examples with code snippets
   - Project structure overview
   - Testing instructions
   - Contributing guidelines
   - License information (suggest MIT or similar)

2. User Guide (save to 'user_guide.md')
   - Getting started tutorial
   - Step-by-step instructions for common tasks
   - Screenshots/diagrams descriptions (in text)
   - Troubleshooting section with common issues and solutions
   - FAQ section if applicable

3. API Documentation (if applicable - save to 'api_docs.md')
   - Endpoint descriptions
   - Request/response formats
   - Example usage with code

Write for BEGINNERS - assume no prior knowledge of the project.
Make it easy for anyone to get started in under 5 minutes.

Use file_writer tool to save all documentation.""",
        expected_output="Complete project documentation saved to workspace: README.md and user_guide.md that makes the project accessible",
        agent=create_tech_writer(),
    )

    # Set task dependencies
    arch_task.context = [prd_task]
    impl_task.context = [prd_task, arch_task]
    test_task.context = [impl_task]
    docs_task.context = [prd_task, arch_task, impl_task, test_task]

    return [prd_task, arch_task, impl_task, test_task, docs_task]


def create_software_dev_crew_dspy(project_idea: str) -> Crew:
    """
    Create a software development crew with DSPy-enhanced agents.

    This crew will:
    1. Create PRD (Product Manager with DSPy optimization)
    2. Design Architecture (Architect with DSPy optimization)
    3. Implement Code (Engineer with RAG + DSPy)
    4. Create Tests (QA Engineer with enhanced practices)
    5. Write Documentation (Tech Writer with best practices)

    All steps are tracked by AgentOps:
    - Agent actions
    - Task execution
    - Tool calls
    - LLM calls and costs
    """
    tasks = create_tasks_dspy(project_idea)

    crew = Crew(
        tasks=tasks,
        process=Process.sequential,
        verbose=config.CREW_CONFIG["verbose"],
        memory=config.CREW_CONFIG["memory"],
        max_rpm=config.CREW_CONFIG["max_rpm"],
    )

    return crew


def run_software_dev_crew_dspy(project_idea: str) -> dict:
    """
    Run the software development crew with DSPy optimization.

    Args:
        project_idea: Description of the software to build

    Returns:
        dict: Results from the crew execution

    This function:
    - Creates CrewAI crew with DSPy-enhanced agents
    - Executes all tasks sequentially
    - Tracks EVERYTHING in AgentOps (tools, agents, tasks, LLM calls, costs)
    - Saves all outputs to workspace
    """
    print("=" * 80)
    print(f"🚀 Starting Software Development Crew (DSPy Enhanced)")
    print(f"📋 Project: {project_idea}")
    print(f"✨ Using DSPy manual few-shot optimization")
    print(f"🔍 RAG enabled for context enhancement")
    print(f"📊 AgentOps tracking: Tools + Agents + Tasks + LLM + Costs")
    print("=" * 80)
    print()

    # Create and run crew
    crew = create_software_dev_crew_dspy(project_idea)
    result = crew.kickoff()

    print()
    print("=" * 80)
    print("✅ Software Development Crew (DSPy Enhanced) Completed!")
    print("=" * 80)
    print()
    print(f"📁 Output saved to: {config.WORKSPACE_DIR}")
    print(f"📊 Check AgentOps dashboard for complete metrics")
    print()

    return result


if __name__ == "__main__":
    # Test the DSPy-enhanced crew
    print("Testing DSPy-Enhanced CrewAI Implementation...")
    print()

    test_idea = "crie uma calculadora CLI simples com operações básicas"

    result = run_software_dev_crew_dspy(test_idea)

    print()
    print("=" * 80)
    print("✅ DSPy-Enhanced CrewAI Test Completed!")
    print("=" * 80)
    print()
    print("This implementation:")
    print("✅ Uses CrewAI framework (full agent/task/tool tracking)")
    print("✅ Incorporates DSPy few-shot optimization (better prompts)")
    print("✅ Includes RAG for context enhancement")
    print("✅ Tracks everything in AgentOps")
    print("✅ Creates actual files using tools")
    print()
