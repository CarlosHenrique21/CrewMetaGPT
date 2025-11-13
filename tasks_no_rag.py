# tasks_no_rag.py
"""
Task definitions for the software development crew - WITHOUT RAG.
Version for baseline comparison (no knowledge base retrieval).
"""
from crewai import Task
from agents_no_rag import (
    create_product_manager,
    create_architect,
    create_engineer,
    create_qa_engineer,
    create_tech_writer,
)


def create_prd_task(project_idea: str) -> Task:
    """Task: Create Product Requirements Document."""
    return Task(
        description=f"""Create a comprehensive Product Requirements Document (PRD) for the following project:

PROJECT IDEA: {project_idea}

Your PRD should include:
1. Project Overview
   - Project name
   - Brief description
   - Target users
   - Key objectives

2. Functional Requirements
   - Core features (must-have)
   - Nice-to-have features
   - User stories

3. Non-Functional Requirements
   - Performance expectations
   - Security requirements
   - Scalability considerations

4. Success Metrics
   - KPIs to measure success
   - Acceptance criteria

5. Constraints and Assumptions
   - Technical constraints
   - Timeline considerations
   - Resource constraints

Save the PRD to 'prd.md' in the workspace.""",
        expected_output="A comprehensive PRD document saved to workspace/prd.md",
        agent=create_product_manager(),
    )


def create_architecture_task() -> Task:
    """Task: Design system architecture."""
    return Task(
        description="""Based on the PRD, design a detailed system architecture.

Your architecture document should include:
1. System Overview
   - High-level architecture diagram (described in text)
   - Key components and their responsibilities

2. Technology Stack
   - Programming language(s)
   - Frameworks and libraries
   - Database choice and rationale
   - Development tools

3. Component Design
   - Frontend architecture (if applicable)
   - Backend architecture
   - Data layer design
   - API design

4. Data Models
   - Key entities and relationships
   - Database schema

5. File Structure
   - Recommended project structure
   - Directory organization

Read the PRD from 'prd.md' and save your architecture to 'architecture.md'.""",
        expected_output="A detailed architecture document saved to workspace/architecture.md",
        agent=create_architect(),
    )


def create_implementation_task() -> Task:
    """Task: Implement the core functionality."""
    return Task(
        description="""Implement the core functionality based on the architecture and PRD.

Your implementation should:
1. Create the project structure as defined in the architecture
2. Implement core features from the PRD
3. Include proper error handling
4. Add inline comments for complex logic
5. Follow coding best practices

Read the architecture from 'architecture.md' and PRD from 'prd.md'.
Create all necessary source files in the workspace with appropriate directory structure.

Focus on implementing:
- Main application logic
- Core features (at least 2-3 main features)
- Basic configuration
- Entry point (main file)

Save your implementation across multiple files with a clear structure.""",
        expected_output="Core implementation files created in the workspace with proper structure",
        agent=create_engineer(),
    )


def create_testing_task() -> Task:
    """Task: Create test plan and test cases."""
    return Task(
        description="""Create a comprehensive testing strategy and test cases.

Your deliverables should include:
1. Test Plan (test_plan.md)
   - Testing approach
   - Types of tests (unit, integration, etc.)
   - Test coverage goals
   - Testing tools

2. Test Cases (test_cases.md)
   - Detailed test scenarios
   - Expected results
   - Edge cases to test
   - Manual testing checklist

3. Sample Unit Tests (tests.py or tests.md)
   - Example unit tests for core functionality
   - Test structure and organization

Read the implementation files and create testing documentation.
Save test plan to 'test_plan.md' and test cases to 'test_cases.md'.""",
        expected_output="Testing documentation saved to workspace: test_plan.md and test_cases.md",
        agent=create_qa_engineer(),
    )


def create_documentation_task() -> Task:
    """Task: Create comprehensive project documentation."""
    return Task(
        description="""Create comprehensive documentation for the project.

Your documentation should include:
1. README.md
   - Project title and description
   - Features list
   - Installation instructions
   - Usage examples
   - Project structure overview
   - Contributing guidelines
   - License information

2. API Documentation (if applicable - api_docs.md)
   - Endpoint descriptions
   - Request/response formats
   - Example usage

3. User Guide (user_guide.md)
   - How to use the application
   - Step-by-step instructions
   - Screenshots descriptions (text)
   - Troubleshooting section

Read all project files and create comprehensive documentation.
The README should be beginner-friendly and include everything needed to get started.""",
        expected_output="Complete project documentation: README.md, user_guide.md saved to workspace",
        agent=create_tech_writer(),
    )


def get_all_tasks(project_idea: str) -> list[Task]:
    """Get all tasks in order for the software development process."""
    prd_task = create_prd_task(project_idea)
    arch_task = create_architecture_task()
    impl_task = create_implementation_task()
    test_task = create_testing_task()
    docs_task = create_documentation_task()

    # Set dependencies
    arch_task.context = [prd_task]
    impl_task.context = [prd_task, arch_task]
    test_task.context = [impl_task]
    docs_task.context = [prd_task, arch_task, impl_task, test_task]

    return [prd_task, arch_task, impl_task, test_task, docs_task]
