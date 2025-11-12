#!/usr/bin/env python3
# main.py
"""
Main entry point for CrewAI Software Company with AgentOps observability.

This demonstrates how simple it is to have full observability with CrewAI:
- Agents are tracked as "Agent" type ✅
- Tasks are tracked as "Task" type ✅
- Tools are tracked as "Tool" type ✅
- LLM calls are tracked as "LLM" type ✅
- No custom wrappers needed!
"""
import sys
from dotenv import load_dotenv
load_dotenv(override=True)

# CRITICAL: Import LLM modules BEFORE agentops.init()
# This allows AgentOps to instrument them properly
import openai
import langchain
import langchain_openai
from crewai import Agent, Task, Crew

# Now import agentops and initialize
import agentops
from crew import run_software_dev_crew
import config

def initialize_observability():
    """Initialize AgentOps observability."""
    if not config.AGENTOPS_API_KEY:
        print("⚠️  AgentOps API key not found - running without observability")
        return False

    try:
        print("🔍 Initializing AgentOps observability...")
        print("📦 LLM modules loaded: openai, langchain, langchain_openai, crewai")

        agentops.init(
            api_key=config.AGENTOPS_API_KEY,
            default_tags=config.AGENTOPS_TAGS,
            auto_start_session=True,
            instrument_llm_calls=True,  # Explicitly enable LLM tracking
        )

        print("✅ AgentOps initialized successfully!")
        print(f"📊 Tags: {', '.join(config.AGENTOPS_TAGS)}")
        print("🔍 LLM Call Tracking: ENABLED")
        print()

        return True
    except Exception as e:
        print(f"❌ Failed to initialize AgentOps: {e}")
        print("Continuing without observability...")
        return False


def main(project_idea: str):
    """Main execution function."""

    print()
    print("=" * 80)
    print("🎯 CrewAI Software Company with AgentOps Observability")
    print("=" * 80)
    print()

    # Initialize observability
    observability_enabled = initialize_observability()

    try:
        # Run the crew
        result = run_software_dev_crew(project_idea)

        # End session with success
        if observability_enabled:
            print("📊 Finalizing AgentOps session...")
            agentops.end_session(end_state="Success")

        print()
        print("✅ Project completed successfully!")
        print()
        print("📁 Check the workspace/ directory for generated files:")
        print("   - prd.md (Product Requirements)")
        print("   - architecture.md (System Design)")
        print("   - Source code files")
        print("   - test_plan.md (Test Plan)")
        print("   - test_cases.md (Test Cases)")
        print("   - README.md (Documentation)")
        print("   - user_guide.md (User Guide)")
        print()

        if observability_enabled:
            print("📊 Check your AgentOps dashboard for detailed analytics:")
            print("   https://app.agentops.ai")
            print()
            print("   You'll see:")
            print("   ✅ Agents (correctly classified as 'Agent')")
            print("   ✅ Tasks (correctly classified as 'Task')")
            print("   ✅ Tools (correctly classified as 'Tool')")
            print("   ✅ LLM Calls (correctly classified as 'LLM')")
            print("   ✅ Complete timeline and hierarchy")
            print("   ✅ Costs and token usage")
            print()

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        if observability_enabled:
            agentops.end_session(end_state="Indeterminate")
        return 130

    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

        if observability_enabled:
            agentops.end_session(end_state="Fail")
        return 1


if __name__ == "__main__":
    # Get project idea from command line or use default
    if len(sys.argv) > 1:
        project_idea = " ".join(sys.argv[1:])
    else:
        project_idea = "escreva um jogo cli cobra baseado em pygame"

    exit_code = main(project_idea)
    sys.exit(exit_code)
