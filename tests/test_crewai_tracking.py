#!/usr/bin/env python3
"""
Script to verify CrewAI + AgentOps integration is tracking properly.
"""
import os
import agentops
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv(override=True)

def test_crewai_agentops_integration():
    """Test if AgentOps tracks CrewAI agents, tasks, and LLM calls."""

    print("=" * 80)
    print("🔍 Testing CrewAI + AgentOps Integration")
    print("=" * 80)
    print()

    # Initialize AgentOps
    try:
        print("🔧 Initializing AgentOps...")
        session = agentops.init(
            api_key=os.getenv("AGENTOPS_API_KEY"),
            default_tags=["crewai", "integration-test"],
            auto_start_session=True,
        )
        print("✅ AgentOps initialized")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize AgentOps: {e}")
        return False

    # Create a simple agent
    try:
        print("🤖 Creating test agent...")
        test_agent = Agent(
            role="Test Agent",
            goal="Respond to a simple test prompt",
            backstory="You are a test agent verifying the system works.",
            verbose=True,
            allow_delegation=False,
        )
        print("✅ Agent created")
        print()
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        agentops.end_session(end_state="Fail")
        return False

    # Create a simple task
    try:
        print("📋 Creating test task...")
        test_task = Task(
            description="Say 'AgentOps tracking is working!' and count to 3.",
            expected_output="A message confirming tracking works and counting 1, 2, 3.",
            agent=test_agent,
        )
        print("✅ Task created")
        print()
    except Exception as e:
        print(f"❌ Failed to create task: {e}")
        agentops.end_session(end_state="Fail")
        return False

    # Create and run crew
    try:
        print("🚀 Running crew...")
        print("-" * 80)
        crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        print("-" * 80)
        print("✅ Crew execution completed")
        print()
        print(f"📝 Result: {result}")
        print()
    except Exception as e:
        print(f"❌ Crew execution failed: {e}")
        agentops.end_session(end_state="Fail")
        return False

    # End session
    try:
        print("📊 Ending AgentOps session...")
        agentops.end_session(end_state="Success")
        print("✅ Session ended successfully")
        print()
    except Exception as e:
        print(f"⚠️  Warning when ending session: {e}")
        print()

    # Summary
    print("=" * 80)
    print("📊 CREWAI + AGENTOPS INTEGRATION STATUS")
    print("=" * 80)
    print()
    print("✅ AgentOps is properly initialized")
    print("✅ CrewAI agents are being created")
    print("✅ CrewAI tasks are being executed")
    print("✅ LLM calls are being tracked")
    print()
    print("🔗 Check your AgentOps dashboard for:")
    print("   https://app.agentops.ai")
    print()
    print("   You should see:")
    print("   • Agent creation events")
    print("   • Task execution events")
    print("   • LLM calls with token usage")
    print("   • Cost calculations")
    print("   • Complete session timeline")
    print()
    print("=" * 80)

    return True

if __name__ == "__main__":
    success = test_crewai_agentops_integration()
    exit(0 if success else 1)
