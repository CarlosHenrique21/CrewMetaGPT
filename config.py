# config.py
"""
Configuration management for CrewAI Software Company.
Loads settings from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
WORKSPACE_DIR.mkdir(exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# AgentOps Configuration
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
AGENTOPS_TAGS = ["crewai", "software-company", "production"]

# Project Configuration
PROJECT_NAME = os.getenv("PROJECT_NAME", "CrewAI-Software-Company")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required settings
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

if not AGENTOPS_API_KEY:
    print("⚠️  AGENTOPS_API_KEY not found - observability will be disabled")

# Agent Configuration
AGENT_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 4000,
    "verbose": True,
}

# Crew Configuration
CREW_CONFIG = {
    "verbose": True,
    "memory": True,
    "max_rpm": 10,  # Rate limiting
}


def get_llm():
    """
    Get configured LLM for agents.
    This ensures AgentOps can track LLM calls properly.
    """
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=AGENT_CONFIG["temperature"],
        max_tokens=AGENT_CONFIG["max_tokens"],
        api_key=OPENAI_API_KEY,
    )
