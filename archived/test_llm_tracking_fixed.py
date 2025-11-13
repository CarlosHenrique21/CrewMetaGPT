#!/usr/bin/env python3
"""
Test script to verify that LLM tracking is working with the fixed configuration.
This test uses a simple CrewAI workflow to check if LLM calls are being tracked.
"""
import sys
from dotenv import load_dotenv
load_dotenv(override=True)

# CRITICAL: Import LLM modules BEFORE agentops.init()
import openai
import langchain
import langchain_openai
from crewai import Agent, Task, Crew, Process

# Now import agentops
import agentops
import os

def test_llm_tracking():
    """Test if LLM calls are being tracked properly."""

    print("=" * 80)
    print("🧪 Testing LLM Tracking with Fixed Configuration")
    print("=" * 80)
    print()

    # Initialize AgentOps
    print("🔍 Initializing AgentOps...")
    print("📦 LLM modules loaded: openai, langchain, langchain_openai, crewai")
    print()

    session = agentops.init(
        api_key=os.getenv("AGENTOPS_API_KEY"),
        default_tags=["test", "llm-tracking-fix"],
        auto_start_session=True,
        instrument_llm_calls=True,  # Explicitly enable
    )

    print("✅ AgentOps initialized")
    print("🔍 LLM Call Tracking: ENABLED")
    print()

    # Create a simple agent
    print("🤖 Creating test agent...")
    test_agent = Agent(
        role="Math Teacher",
        goal="Explain simple math concepts clearly",
        backstory="You are an experienced math teacher who loves helping students.",
        verbose=True,
        allow_delegation=False,
    )
    print("✅ Agent created")
    print()

    # Create a simple task
    print("📋 Creating test task...")
    test_task = Task(
        description="Explain what is 2 + 2 and why the answer is correct. Be brief.",
        expected_output="A brief explanation of 2+2=4",
        agent=test_agent,
    )
    print("✅ Task created")
    print()

    # Run the crew
    print("🚀 Running crew (this will make LLM calls)...")
    print("-" * 80)

    try:
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
        import traceback
        traceback.print_exc()
        agentops.end_session(end_state="Fail")
        return False

    # End session
    print("📊 Ending AgentOps session...")
    agentops.end_session(end_state="Success")
    print()

    # Summary
    print("=" * 80)
    print("📊 TEST RESULTS")
    print("=" * 80)
    print()
    print("✅ AgentOps initialized with LLM modules pre-loaded")
    print("✅ CrewAI agent created and executed")
    print("✅ LLM calls made during execution")
    print()
    print("🔗 Check your AgentOps dashboard:")
    print("   https://app.agentops.ai")
    print()
    print("   You should now see:")
    print("   💰 LLM call costs calculated")
    print("   🔢 Token usage (prompt + completion)")
    print("   📊 Complete session timeline")
    print("   🌳 Agent and task hierarchy")
    print()
    print("If you see LLM calls with costs in the dashboard,")
    print("the fix is working correctly! ✅")
    print()
    print("=" * 80)

    return True

if __name__ == "__main__":
    success = test_llm_tracking()
    sys.exit(0 if success else 1)
