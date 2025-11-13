#!/bin/bash
# Script para executar teste baseline COM RAG + DSPy MANUAL usando CrewAI
# Faz LLM calls reais, executa tasks, cria arquivos, e rastreia TUDO no AgentOps!

echo "================================================================================"
echo "🧪 CrewAI + DSPy Baseline Test - HYBRID APPROACH"
echo "================================================================================"
echo ""
echo "Este script executa 5 projetos usando:"
echo "✅ CrewAI framework (agents, tasks, tools)"
echo "✅ DSPy manual optimization (few-shot examples)"
echo "✅ RAG para contexto"
echo "✅ AgentOps tracking COMPLETO (tools, agents, tasks, LLM, costs)"
echo ""

# Mudar para diretório raiz do projeto
cd "$(dirname "$0")/.." || exit 1

# Verificar se API key está configurada
echo "Verificando configuração..."
API_KEY=$(python -c "from dotenv import load_dotenv; import config; load_dotenv(override=True); print(config.OPENAI_API_KEY[:20] if config.OPENAI_API_KEY else 'None')" 2>/dev/null)
if [ "$API_KEY" = "None" ]; then
    echo "❌ OPENAI_API_KEY não configurada!"
    echo ""
    echo "Por favor, configure a API key no arquivo .env:"
    echo "  OPENAI_API_KEY=sk-proj-your-key-here"
    echo ""
    exit 1
fi

if [[ $API_KEY == sk-proj* ]] || [[ $API_KEY == sk-* ]]; then
    echo "✅ API Key configurada: ${API_KEY}..."
else
    echo "⚠️  Formato de API key inesperado: $API_KEY"
    echo "    Continuando mesmo assim..."
fi
echo ""

# Informar sobre configuração
echo "✅ RAG: HABILITADO"
echo "🔧 DSPy: OTIMIZAÇÃO MANUAL (few-shot examples)"
echo "🤖 CrewAI: FRAMEWORK COMPLETO (agents, tasks, tools)"
echo "📊 AgentOps: TRACKING COMPLETO"
echo "💡 LLM CALLS: REAIS"
echo ""

# Executar teste
echo "Iniciando teste baseline CrewAI + DSPy..."
echo "Duração estimada: 30-50 minutos (executa tasks completas!)"
echo "Custo estimado: ~\$5.00-10.00"
echo ""

# Limpar API key cache e executar
unset OPENAI_API_KEY
exec python -c "
import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Forçar reload do .env
from dotenv import load_dotenv
load_dotenv(override=True)

# Add to path
sys.path.insert(0, '.')

# CRITICAL: Import LLM modules BEFORE agentops.init()
# This allows AgentOps to instrument them properly
print('📦 Carregando módulos LLM...')
import openai
import langchain
import langchain_openai
from crewai import Agent, Task, Crew

print('✅ Módulos LLM carregados')

# Import config and dspy
import config
from dspy_config import configure_dspy

print('📦 Carregando crew...')

# NOW import and initialize AgentOps BEFORE importing crew
import agentops

agentops_enabled = False
try:
    agentops_key = os.getenv('AGENTOPS_API_KEY')
    if agentops_key:
        print('🔍 Inicializando AgentOps...')
        # Initialize with proper instrumentation (like baselines)
        agentops.init(
            api_key=agentops_key,
            default_tags=['baseline', 'crewai-dspy', 'rag', 'hybrid'],
            auto_start_session=True,
            instrument_llm_calls=True,  # ENABLE LLM tracking!
        )
        agentops_enabled = True
        print('✅ AgentOps inicializado')
        print('   🔍 LLM Call Tracking: ENABLED')
        print('   📊 Agent/Task/Tool Tracking: ENABLED')
        print()
    else:
        print('⚠️  AGENTOPS_API_KEY não configurada')
        print()
except Exception as e:
    print(f'⚠️  AgentOps não disponível: {e}')
    print()

# Import crew function AFTER AgentOps is initialized
from crew_crewai_dspy import run_software_dev_crew_dspy

# Projetos de teste
TEST_PROJECTS = [
    {
        'id': 'project_01',
        'name': 'Todo List CLI',
        'description': 'crie uma aplicação CLI para gerenciar lista de tarefas com comandos add, list, done e delete'
    },
    {
        'id': 'project_02',
        'name': 'URL Shortener API',
        'description': 'crie uma API REST para encurtar URLs com endpoints para criar, listar e redirecionar'
    },
    {
        'id': 'project_03',
        'name': 'Weather CLI',
        'description': 'crie uma ferramenta CLI que consulta API de clima e mostra previsão formatada'
    },
    {
        'id': 'project_04',
        'name': 'Password Generator',
        'description': 'crie um gerador de senhas seguras CLI com opções de tamanho, caracteres especiais e força'
    },
    {
        'id': 'project_05',
        'name': 'Markdown to HTML Converter',
        'description': 'crie um conversor de Markdown para HTML com suporte a títulos, listas e links'
    },
]

print()
print('=' * 80)
print('🧪 TESTE BASELINE CREWAI + DSPY - BATCH DE 5 PROJETOS')
print('=' * 80)
print()
print('Este teste usa CrewAI COM DSPy otimização manual.')
print('FAZ LLM CALLS REAIS e executa TASKS COMPLETAS!')
print('Rastreia TUDO no AgentOps: tools, agents, tasks, LLM, costs')
print()

# Configurar DSPy (para RAG)
print('⚙️  Configurando DSPy...')
configure_dspy()
print('✅ DSPy configurado')
print()
print('✅ CrewAI + DSPy + RAG + AgentOps configurado!')
print()

# Listar projetos
print(f'📋 Projetos a serem executados: {len(TEST_PROJECTS)}')
for i, proj in enumerate(TEST_PROJECTS, 1):
    print(f'   {i}. {proj[\"name\"]} ({proj[\"id\"]})')
print()
print('Iniciando em 3 segundos...')
time.sleep(3)
print()

# Executar batch
all_metrics = []
batch_start = time.time()

for i, project in enumerate(TEST_PROJECTS, 1):
    print()
    print('=' * 80)
    print(f'📋 PROJETO {i}/{len(TEST_PROJECTS)}: {project[\"name\"]}')
    print(f'ID: {project[\"id\"]}')
    print('=' * 80)
    print()

    start = time.time()

    try:
        # Executar CrewAI crew com DSPy optimization
        result = run_software_dev_crew_dspy(
            project_idea=project['description']
        )

        duration = time.time() - start

        metrics = {
            'project_id': project['id'],
            'project_name': project['name'],
            'status': 'success',
            'duration_seconds': round(duration, 2),
            'timestamp': datetime.now().isoformat(),
            'approach': 'crewai_dspy_hybrid',
            'note': 'CrewAI framework + DSPy manual few-shot + RAG + AgentOps'
        }

        # Salvar métricas
        metrics_dir = Path('metrics/data/crewai_dspy')
        metrics_dir.mkdir(parents=True, exist_ok=True)
        metrics_file = metrics_dir / f'baseline_{project[\"id\"]}.json'
        metrics_file.write_text(json.dumps(metrics, indent=2))

        print()
        print('=' * 80)
        print(f'✅ PROJETO {i} CONCLUÍDO')
        print('=' * 80)
        print(f'⏱️  Duração: {duration:.2f}s ({duration/60:.1f} min)')
        print()

        all_metrics.append(metrics)

    except Exception as e:
        duration = time.time() - start
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

        all_metrics.append({
            'project_id': project['id'],
            'project_name': project['name'],
            'status': 'error',
            'duration_seconds': round(duration, 2),
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'approach': 'crewai_dspy_hybrid'
        })

    # Pausa entre projetos
    if i < len(TEST_PROJECTS):
        print('\\n⏸️  Aguardando 10 segundos antes do próximo projeto...')
        time.sleep(10)

batch_duration = time.time() - batch_start

# Gerar relatório
total_duration = sum(m['duration_seconds'] for m in all_metrics)
successful = sum(1 for m in all_metrics if m['status'] == 'success')

print()
print('=' * 80)
print('📊 RELATÓRIO BASELINE CREWAI + DSPY - RESUMO')
print('=' * 80)
print()
print(f'Total de projetos: {len(all_metrics)}')
print(f'✅ Sucesso: {successful}')
print(f'❌ Falhas: {len(all_metrics) - successful}')
print(f'⏱️  Duração total: {total_duration:.2f}s ({total_duration/60:.1f} min)')
print(f'⏱️  Duração média: {total_duration/len(all_metrics):.2f}s ({total_duration/len(all_metrics)/60:.1f} min) por projeto')
print()

# Salvar relatório
report_path = Path('metrics/data/crewai_dspy/baseline_report.json')
report = {
    'test_type': 'baseline_crewai_dspy_hybrid',
    'test_date': datetime.now().isoformat(),
    'total_projects': len(all_metrics),
    'successful': successful,
    'failed': len(all_metrics) - successful,
    'total_duration_seconds': round(total_duration, 2),
    'avg_duration_per_project_seconds': round(total_duration/len(all_metrics), 2),
    'projects': all_metrics,
    'approach': {
        'framework': 'CrewAI',
        'optimization': 'DSPy manual few-shot',
        'rag': 'enabled',
        'tracking': 'AgentOps (tools, agents, tasks, LLM, costs)'
    }
}
report_path.write_text(json.dumps(report, indent=2))
print(f'💾 Relatório salvo em: {report_path}')

print()
print('=' * 80)
print('🎉 TESTE BASELINE CREWAI + DSPY CONCLUÍDO!')
print('=' * 80)
print()
print('Este teste usou:')
print('✅ CrewAI framework (executa tasks, usa tools, cria arquivos)')
print('✅ DSPy manual optimization (few-shot examples)')
print('✅ RAG para contexto')
print('✅ AgentOps tracking COMPLETO')
print()
print('📊 Verifique o dashboard do AgentOps para métricas completas:')
print('   - Tool calls')
print('   - Agent actions')
print('   - Task execution')
print('   - LLM calls e tokens')
print('   - Costs')
print()

# Finalizar AgentOps
if agentops_enabled:
    print('📊 Finalizando AgentOps session...')
    agentops.end_session(end_state='Success')

sys.exit(0)
"
