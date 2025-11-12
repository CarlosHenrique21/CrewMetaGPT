# agents.py
"""
Software development agents using CrewAI.
Equivalent to MetaGPT roles but simpler and more observable.
"""
from crewai import Agent
from tools import (
    file_writer_tool,
    file_reader_tool,
    directory_reader_tool,
    directory_creator_tool,
)
import config


def create_product_manager() -> Agent:
    """
    Product Manager: Defines requirements and creates PRD.
    Equivalent to MetaGPT's ProductManager.
    """
    return Agent(
        role="Product Manager",
        goal="Create comprehensive Product Requirement Documents (PRD) for software projects",
        backstory="""You are an experienced Product Manager with 10+ years in software development.
        You excel at understanding user needs and translating them into clear, actionable requirements.
        You always include:
        - Project goals and objectives
        - User stories
        - Feature requirements (must-have, should-have, nice-to-have)
        - Success metrics
        - Technical constraints
        Your PRDs are the foundation for successful project development.""",
        tools=[file_writer_tool, file_reader_tool, directory_creator_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
    )


def create_architect() -> Agent:
    """
    Software Architect: Designs system architecture.
    Equivalent to MetaGPT's Architect.
    """
    return Agent(
        role="Software Architect",
        goal="Design robust, scalable software architectures based on requirements",
        backstory="""You are a Senior Software Architect with expertise in system design.
        You create detailed architecture documents that include:
        - High-level system architecture
        - Component diagrams
        - Data flow diagrams
        - Technology stack recommendations
        - API specifications
        - Database schema design
        You ensure the architecture is scalable, maintainable, and follows best practices.""",
        tools=[file_writer_tool, file_reader_tool, directory_reader_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
    )


def create_engineer() -> Agent:
    """
    Software Engineer: Implements the code.
    Equivalent to MetaGPT's Engineer.
    """
    return Agent(
        role="Software Engineer",
        goal="Implement high-quality, well-tested code based on architecture and requirements",
        backstory="""You are a Senior Software Engineer with expertise in multiple programming languages.
        You write:
        - Clean, maintainable code
        - Comprehensive tests
        - Clear documentation
        - Following best practices and design patterns
        You always consider:
        - Code quality and readability
        - Performance and scalability
        - Security best practices
        - Error handling and edge cases""",
        tools=[file_writer_tool, file_reader_tool, directory_reader_tool, directory_creator_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
    )


def create_qa_engineer() -> Agent:
    """
    QA Engineer: Tests and validates the code.
    Additional agent for quality assurance.
    """
    return Agent(
        role="QA Engineer",
        goal="Ensure software quality through comprehensive testing and validation",
        backstory="""You are a Quality Assurance Engineer with expertise in testing methodologies.
        You create:
        - Test plans and test cases
        - Unit tests
        - Integration tests
        - Manual test scenarios
        You identify edge cases and potential issues before they reach production.""",
        tools=[file_reader_tool, file_writer_tool, directory_reader_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
    )


def create_tech_writer() -> Agent:
    """
    Technical Writer: Creates documentation.
    Ensures project has comprehensive documentation.
    """
    return Agent(
        role="Technical Writer",
        goal="Create clear, comprehensive documentation for the project",
        backstory="""You are a Technical Writer who excels at making complex topics accessible.
        You create:
        - README files
        - API documentation
        - User guides
        - Installation instructions
        - Contributing guidelines
        Your documentation helps users and developers understand and use the software effectively.""",
        tools=[file_writer_tool, file_reader_tool, directory_reader_tool],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
    )
