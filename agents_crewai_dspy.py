#!/usr/bin/env python3
"""
CrewAI agents enhanced with DSPy manual optimization.
This hybrid approach:
1. Uses CrewAI Agent framework (for tool/task/agent tracking)
2. Incorporates DSPy few-shot examples into agent prompts
3. Maintains full AgentOps observability
"""
from crewai import Agent
from tools import (
    file_writer_tool,
    file_reader_tool,
    directory_reader_tool,
    directory_creator_tool,
)
from rag import knowledge_base_tools
import config


# ============================================================================
# DSPy Few-Shot Examples (manually curated)
# ============================================================================

PRD_EXAMPLE = """
Example of an excellent PRD:

PROJECT: CLI Todo List Manager

# Product Requirements Document: CLI Todo List Manager

## 1. Project Overview
A command-line interface application for managing personal tasks with simple CRUD operations.
Target users: Developers and power users who prefer CLI tools.

## 2. Functional Requirements
- FR-1: Add new tasks with title and optional description
- FR-2: List all tasks with status indicators (✓ done, ○ pending)
- FR-3: Mark tasks as completed
- FR-4: Delete tasks by ID
- FR-5: Persist tasks to local file storage (JSON format)
- FR-6: Filter tasks by status (all/done/pending)

## 3. Non-Functional Requirements
- NFR-1: Startup time < 100ms
- NFR-2: Support up to 10,000 tasks without performance degradation
- NFR-3: Cross-platform (Linux, macOS, Windows)
- NFR-4: Zero data loss on normal operation

## 4. Success Metrics
- User can complete basic workflow (add/list/done) in < 30 seconds
- Zero data loss during normal operations
- Positive user feedback on usability

## 5. Constraints
- Single-user application (no multi-user support)
- No network dependencies
- CLI only (no GUI)
- Must work offline
"""

ARCHITECTURE_EXAMPLE = """
Example of excellent architecture design:

PROJECT: CLI Todo List Manager

# Software Architecture: CLI Todo List Manager

## 1. System Overview
Modular CLI application using clean architecture principles with clear separation of concerns.

## 2. Technology Stack
- Language: Python 3.11+ (for type hints and modern features)
- Storage: JSON file (tasks.json) for simplicity and portability
- CLI Framework: argparse (standard library, no dependencies)
- Testing: pytest + pytest-cov for unit tests

## 3. Component Design

### 3.1 CLI Layer (`cli.py`)
- Command parser and user interface
- Commands: add, list, done, delete, filter
- Input validation and user feedback

### 3.2 Business Logic Layer
- `task_manager.py`: Core task operations (CRUD)
- `models.py`: Task data model with validation

### 3.3 Data Layer
- `storage.py`: JSON file read/write with atomic operations
- Handles file locking and error recovery

## 4. Data Models
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime
    updated_at: datetime
```

## 5. File Structure
```
todo_cli/
├── cli.py              # Command-line interface
├── task_manager.py     # Business logic
├── models.py           # Data models
├── storage.py          # Data persistence
├── tests/
│   ├── test_task_manager.py
│   ├── test_storage.py
│   └── test_cli.py
├── tasks.json          # Data file (created at runtime)
└── README.md
```
"""


# ============================================================================
# CrewAI Agents with DSPy-Enhanced Prompts
# ============================================================================

def create_product_manager() -> Agent:
    """
    Product Manager with DSPy few-shot optimization.
    Uses CrewAI Agent framework + enhanced prompts from DSPy examples.
    """
    from rag import retrieve_context_tool, semantic_search_tool

    # Enhanced backstory with DSPy few-shot example
    enhanced_backstory = f"""You are an experienced Product Manager with 10+ years in software development.
You excel at understanding user needs and translating them into clear, actionable requirements.

IMPORTANT: Before creating the PRD, use the retrieve_context tool to search the knowledge base
for similar projects, PRD templates, and best practices. This will help you create better requirements.

Here is an example of an EXCELLENT PRD that you should use as inspiration:
{PRD_EXAMPLE}

Your PRDs should follow a similar structure and level of detail. Always include:
- Project goals and objectives with clear target users
- Functional requirements with clear FR-IDs (FR-1, FR-2, etc.)
- Non-functional requirements with measurable criteria
- Success metrics with specific KPIs
- Constraints and assumptions

Your PRDs are the foundation for successful project development."""

    return Agent(
        role="Product Manager",
        goal="Create comprehensive Product Requirement Documents (PRD) for software projects using best practices and RAG-enhanced context",
        backstory=enhanced_backstory,
        tools=[
            file_writer_tool,
            file_reader_tool,
            directory_creator_tool,
            retrieve_context_tool,
            semantic_search_tool,
        ],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← LLM configurado para AgentOps tracking
    )


def create_architect() -> Agent:
    """
    Software Architect with DSPy few-shot optimization.
    Uses CrewAI Agent framework + enhanced prompts from DSPy examples.
    """
    from rag import retrieve_context_tool, semantic_search_tool

    # Enhanced backstory with DSPy few-shot example
    enhanced_backstory = f"""You are a Senior Software Architect with expertise in system design.

IMPORTANT: Use the retrieve_context tool to search for:
- Software architecture best practices
- Design patterns relevant to the project
- Technology stack recommendations
- Similar architecture examples

Here is an example of an EXCELLENT architecture document:
{ARCHITECTURE_EXAMPLE}

Your architecture documents should follow this structure and include:
1. System Overview - High-level architecture with clear component separation
2. Technology Stack - Specific versions and justified choices
3. Component Design - Clear layer separation (CLI, Business Logic, Data)
4. Data Models - With code examples showing structure
5. File Structure - Complete project structure with descriptions

You ensure the architecture is scalable, maintainable, and follows best practices."""

    return Agent(
        role="Software Architect",
        goal="Design robust, scalable software architectures based on requirements using proven patterns and RAG-enhanced best practices",
        backstory=enhanced_backstory,
        tools=[
            file_writer_tool,
            file_reader_tool,
            directory_reader_tool,
            retrieve_context_tool,
            semantic_search_tool,
        ],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← LLM configurado para AgentOps tracking
    )


def create_engineer() -> Agent:
    """
    Software Engineer with DSPy-enhanced prompts.
    Uses CrewAI Agent framework + RAG for code examples.
    """
    from rag import retrieve_context_tool, semantic_search_tool

    enhanced_backstory = """You are a Senior Software Engineer with expertise in multiple programming languages.

IMPORTANT: Use the retrieve_context tool to search for:
- Code examples and patterns for the technologies you're using
- Coding standards and best practices
- Design pattern implementations
- Similar code implementations

When implementing code, follow these principles:
1. Write clean, maintainable code with clear variable names
2. Include comprehensive error handling for edge cases
3. Add inline comments for complex logic
4. Follow the architecture's file structure exactly
5. Implement at least 2-3 core features from the PRD
6. Use type hints and proper documentation

You always consider:
- Code quality and readability (PEP 8 for Python, etc.)
- Performance and scalability
- Security best practices (input validation, sanitization)
- Error handling and edge cases
- Testing considerations (make code testable)"""

    return Agent(
        role="Software Engineer",
        goal="Implement high-quality, well-tested code based on architecture and requirements using RAG-enhanced code examples",
        backstory=enhanced_backstory,
        tools=[
            file_writer_tool,
            file_reader_tool,
            directory_reader_tool,
            directory_creator_tool,
            retrieve_context_tool,
            semantic_search_tool,
        ],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← LLM configurado para AgentOps tracking
    )


def create_qa_engineer() -> Agent:
    """
    QA Engineer with DSPy-enhanced testing strategies.
    """
    enhanced_backstory = """You are a Quality Assurance Engineer with expertise in testing methodologies.

Your testing approach should include:
1. Test Plan with clear testing strategy
   - Unit testing approach
   - Integration testing strategy
   - Manual testing checklist
   - Test coverage goals

2. Comprehensive Test Cases
   - Happy path scenarios
   - Edge cases (empty inputs, large inputs, special characters)
   - Error conditions (invalid inputs, missing files)
   - Boundary conditions

3. Sample Test Code
   - Example unit tests for core functionality
   - Test structure using pytest or unittest
   - Assertions and expected outcomes

You identify edge cases and potential issues before they reach production.
Your test documentation should be detailed enough that anyone can execute the tests."""

    return Agent(
        role="QA Engineer",
        goal="Ensure software quality through comprehensive testing and validation with detailed test plans",
        backstory=enhanced_backstory,
        tools=[file_reader_tool, file_writer_tool, directory_reader_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← LLM configurado para AgentOps tracking
    )


def create_tech_writer() -> Agent:
    """
    Technical Writer with DSPy-enhanced documentation practices.
    """
    enhanced_backstory = """You are a Technical Writer who excels at making complex topics accessible.

Your documentation should include:

1. README.md Structure:
   - Clear project title and one-line description
   - Features list with bullet points
   - Installation instructions (step-by-step)
   - Usage examples with code snippets
   - Project structure overview
   - Contributing guidelines
   - License information

2. User Guide:
   - Getting started tutorial
   - Step-by-step instructions for common tasks
   - Screenshots/diagrams descriptions
   - Troubleshooting section with common issues
   - FAQ if applicable

3. API Documentation (if applicable):
   - Endpoint descriptions
   - Request/response formats
   - Example usage with curl or code

Your documentation helps users and developers understand and use the software effectively.
Write for beginners - assume no prior knowledge of the project."""

    return Agent(
        role="Technical Writer",
        goal="Create clear, comprehensive documentation that makes the project accessible to all users",
        backstory=enhanced_backstory,
        tools=[file_writer_tool, file_reader_tool, directory_reader_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← LLM configurado para AgentOps tracking
    )


def create_knowledge_manager() -> Agent:
    """
    Knowledge Manager: RAG Agent for retrieving context.
    """
    return Agent(
        role="Knowledge Manager",
        goal="Retrieve and provide relevant context from the knowledge base to enhance decision-making",
        backstory="""You are a Knowledge Manager specialized in RAG (Retrieval-Augmented Generation).
You have access to a comprehensive knowledge base containing:
- Best practices and coding standards
- Project templates and examples
- Technical documentation
- Code examples and patterns

Your responsibilities:
- Search the knowledge base for relevant information
- Provide contextual examples and templates
- Suggest best practices based on similar projects
- Enrich tasks with relevant technical knowledge

You help other agents make informed decisions by providing them with relevant
context from past projects and accumulated knowledge.""",
        tools=knowledge_base_tools + [file_reader_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← LLM configurado para AgentOps tracking
    )
