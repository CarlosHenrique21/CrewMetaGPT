# crew_no_rag.py
"""
Main Crew definition for the software development team - WITHOUT RAG.
Version for baseline comparison (no knowledge base retrieval).
This is where AgentOps observability shines - everything is tracked automatically!
"""
from crewai import Crew, Process
from tasks_no_rag import get_all_tasks
import config


def create_software_dev_crew(project_idea: str) -> Crew:
    """
    Create a software development crew WITHOUT RAG.

    This crew will:
    1. Create PRD (Product Manager)
    2. Design Architecture (Architect)
    3. Implement Code (Engineer)
    4. Create Tests (QA Engineer)
    5. Write Documentation (Tech Writer)

    All steps are automatically tracked by AgentOps!
    """
    # Get all tasks (tasks include their agents)
    tasks = get_all_tasks(project_idea)

    # Create crew with sequential process
    crew = Crew(
        tasks=tasks,
        process=Process.sequential,  # Tasks run one after another
        verbose=config.CREW_CONFIG["verbose"],
        memory=config.CREW_CONFIG["memory"],
        max_rpm=config.CREW_CONFIG["max_rpm"],
    )

    return crew


def run_software_dev_crew(project_idea: str) -> dict:
    """
    Run the software development crew WITHOUT RAG.

    Args:
        project_idea: Description of the software to build

    Returns:
        dict: Results from the crew execution
    """
    print("=" * 80)
    print(f"🚀 Starting Software Development Crew (NO RAG)")
    print(f"📋 Project: {project_idea}")
    print("=" * 80)
    print()

    # Create and run crew
    crew = create_software_dev_crew(project_idea)
    result = crew.kickoff()

    print()
    print("=" * 80)
    print("✅ Software Development Crew Completed!")
    print("=" * 80)
    print()
    print(f"📁 Output saved to: {config.WORKSPACE_DIR}")
    print()

    return result
