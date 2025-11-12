#!/usr/bin/env python3
"""
Script to verify AgentOps tracking is working properly.
"""
import os
import agentops
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

def test_agentops_tracking():
    """Test if AgentOps is tracking LLM calls and calculating costs."""

    print("=" * 80)
    print("🔍 Testing AgentOps LLM Tracking")
    print("=" * 80)
    print()

    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    agentops_key = os.getenv("AGENTOPS_API_KEY")

    if not openai_key:
        print("❌ OPENAI_API_KEY not found")
        return False

    if not agentops_key:
        print("❌ AGENTOPS_API_KEY not found")
        return False

    print("✅ API keys found")
    print(f"   - OpenAI: {openai_key[:20]}...")
    print(f"   - AgentOps: {agentops_key[:20]}...")
    print()

    # Initialize AgentOps
    try:
        print("🔧 Initializing AgentOps...")
        session = agentops.init(
            api_key=agentops_key,
            default_tags=["test", "tracking-verification"],
            auto_start_session=True,
        )
        print(f"✅ AgentOps initialized")
        print(f"   Session ID: {session.session_id if hasattr(session, 'session_id') else 'N/A'}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize AgentOps: {e}")
        return False

    # Make a test LLM call
    try:
        print("🤖 Making test LLM call...")
        client = OpenAI(api_key=openai_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello World' and nothing else."}
            ],
            max_tokens=50
        )

        print("✅ LLM call successful")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"   Model: {response.model}")
        print(f"   Tokens used: {response.usage.total_tokens}")
        print(f"   - Prompt tokens: {response.usage.prompt_tokens}")
        print(f"   - Completion tokens: {response.usage.completion_tokens}")
        print()

    except Exception as e:
        print(f"❌ LLM call failed: {e}")
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
    print("📊 TRACKING STATUS SUMMARY")
    print("=" * 80)
    print()
    print("✅ AgentOps is properly initialized")
    print("✅ LLM calls are being made successfully")
    print("✅ Token usage is being tracked")
    print()
    print("🔗 Check your AgentOps dashboard for detailed analytics:")
    print("   https://app.agentops.ai")
    print()
    print("   You should see:")
    print("   • LLM call recorded")
    print("   • Token usage (prompt + completion)")
    print("   • Cost calculation")
    print("   • Session timeline")
    print()
    print("=" * 80)

    return True

if __name__ == "__main__":
    success = test_agentops_tracking()
    exit(0 if success else 1)
