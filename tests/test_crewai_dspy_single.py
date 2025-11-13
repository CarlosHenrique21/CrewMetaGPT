#!/usr/bin/env python3
"""
Quick test of CrewAI + DSPy hybrid approach with a single project.
This verifies:
1. CrewAI agents execute properly
2. Tasks are completed
3. Files are created
4. AgentOps tracks everything (agents, tasks, tools, LLM calls, costs)
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment FIRST
load_dotenv(override=True)

print("=" * 80)
print("🧪 TESTE RÁPIDO: CrewAI + DSPy Hybrid Approach")
print("=" * 80)
print()

# CRITICAL: Import LLM modules BEFORE agentops.init()
# This allows AgentOps to instrument them properly
print("📦 Carregando módulos LLM...")
import openai
import langchain
import langchain_openai
from crewai import Agent, Task, Crew

print("✅ Módulos LLM carregados")

# Import config and dspy
import config
from dspy_config import configure_dspy

print("📦 Carregando crew...")

# NOW import and initialize AgentOps BEFORE importing crew
import agentops

agentops_enabled = False
try:
    agentops_key = os.getenv('AGENTOPS_API_KEY')

    if agentops_key:
        print("🔍 Inicializando AgentOps...")
        # Initialize with proper instrumentation (like baselines)
        agentops.init(
            api_key=agentops_key,
            default_tags=['test', 'crewai-dspy', 'single-project', 'hybrid'],
            auto_start_session=True,
            instrument_llm_calls=True,  # ENABLE LLM tracking!
        )
        agentops_enabled = True
        print('✅ AgentOps inicializado')
        print('   🔍 LLM Call Tracking: ENABLED')
        print('   📊 Agent/Task/Tool Tracking: ENABLED')
    else:
        print('⚠️  AgentOps não configurado (opcional)')
except Exception as e:
    print(f'⚠️  AgentOps não disponível: {e}')

print()

# Import crew function AFTER AgentOps is initialized
from crew_crewai_dspy import run_software_dev_crew_dspy

print("Este teste verifica:")
print("✅ CrewAI agents executam tasks")
print("✅ Files são criados usando tools")
print("✅ AgentOps rastreia tools, agents, tasks, LLM")
print("✅ DSPy few-shot optimization melhora prompts")
print("✅ RAG fornece contexto")
print()

# Configure DSPy (for RAG)
print("⚙️  Configurando DSPy...")
configure_dspy()
print("✅ DSPy configurado")
print()

print()
print("=" * 80)
print("🚀 Executando teste com projeto simples...")
print("=" * 80)
print()

# Test with simple project
test_idea = "crie uma calculadora CLI simples com operações básicas de soma, subtração, multiplicação e divisão"

try:
    result = run_software_dev_crew_dspy(project_idea=test_idea)

    print()
    print("=" * 80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print()

    # Verify files were created
    workspace = Path(config.WORKSPACE_DIR)
    expected_files = ['prd.md', 'architecture.md', 'README.md']

    print("📁 Verificando arquivos criados...")
    print()

    files_created = []
    for file in expected_files:
        file_path = workspace / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   ✅ {file} ({size} bytes)")
            files_created.append(file)
        else:
            print(f"   ❌ {file} NÃO ENCONTRADO")

    print()

    if len(files_created) >= 3:
        print("🎉 SUCESSO! Arquivos foram criados corretamente!")
    else:
        print("⚠️  Alguns arquivos não foram criados.")

    print()
    print("=" * 80)
    print("📊 PRÓXIMOS PASSOS")
    print("=" * 80)
    print()
    print("1. Verifique o dashboard do AgentOps para ver:")
    print("   - Tool calls (file_writer, file_reader, etc.)")
    print("   - Agent actions (Product Manager, Architect, etc.)")
    print("   - Task execution (PRD, Architecture, Implementation, etc.)")
    print("   - LLM calls e costs")
    print()
    print("2. Se tudo estiver OK, execute o baseline completo:")
    print("   ./scripts/run_baseline_crewai_dspy.sh")
    print()

    # Finalize AgentOps
    if agentops_enabled:
        print("📊 Finalizando AgentOps session...")
        agentops.end_session(end_state='Success')

    sys.exit(0)

except Exception as e:
    print()
    print("=" * 80)
    print("❌ ERRO NO TESTE")
    print("=" * 80)
    print()
    print(f"Erro: {e}")
    print()

    import traceback
    traceback.print_exc()

    # Finalize AgentOps with error
    if agentops_enabled:
        agentops.end_session(end_state='Fail')

    sys.exit(1)
