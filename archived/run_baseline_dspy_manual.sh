#!/bin/bash
# Script para executar teste baseline COM RAG + DSPy MANUAL
# FAZ LLM CALLS REAIS com few-shot optimization manual!

echo "================================================================================"
echo "🧪 CrewAI Baseline Test - COM RAG + DSPy MANUAL (LLM CALLS REAIS)"
echo "================================================================================"
echo ""
echo "Este script executa 5 projetos usando DSPy COM RAG e otimização MANUAL."
echo "✅ FAZ LLM CALLS REAIS (não usa demos auto-compiladas)"
echo "✅ USA few-shot examples manuais para melhorar prompts"
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

# Informar sobre RAG + DSPy Manual
echo "✅ RAG: HABILITADO"
echo "🔧 DSPy: OTIMIZAÇÃO MANUAL (few-shot examples)"
echo "💡 LLM CALLS: REAIS"
echo ""

# Executar teste
echo "Iniciando teste baseline COM RAG + DSPy Manual..."
echo "Duração estimada: 20-35 minutos (faz LLM calls REAIS!)"
echo "Custo estimado: ~\$3.00-6.00"
echo ""

# Limpar API key cache e executar
unset OPENAI_API_KEY
exec python -c "
import os
import sys

# Forçar reload do .env
from dotenv import load_dotenv
load_dotenv(override=True)

# Executar teste
sys.path.insert(0, '.')

# Importar e executar teste baseline manual
import time
import json
from pathlib import Path
from datetime import datetime
from crew_dspy_manual import run_software_dev_crew_dspy_manual
from dspy_config import configure_dspy
import config

# Projetos
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
print('🧪 TESTE BASELINE COM RAG + DSPy MANUAL - BATCH DE 5 PROJETOS')
print('=' * 80)
print()
print('Este teste usa DSPy COM otimização MANUAL (few-shot).')
print('FAZ LLM CALLS REAIS!')
print()

# Configurar DSPy
print('⚙️  Configurando DSPy...')
configure_dspy()
print()

# Inicializar AgentOps
try:
    import agentops
    if config.AGENTOPS_API_KEY:
        agentops.init(api_key=config.AGENTOPS_API_KEY, tags=['baseline', 'dspy-manual', 'rag'])
        print('✅ AgentOps inicializado')
    else:
        print('⚠️  AgentOps não configurado')
except:
    print('⚠️  AgentOps não disponível')

print('✅ RAG HABILITADO + DSPy MANUAL (LLM calls reais)')
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
        # Executar pipeline manual (FAZ LLM CALLS REAIS!)
        result = run_software_dev_crew_dspy_manual(
            project_idea=project['description'],
            save_outputs=True
        )

        duration = time.time() - start

        metrics = {
            'project_id': project['id'],
            'project_name': project['name'],
            'status': 'success',
            'duration_seconds': round(duration, 2),
            'timestamp': datetime.now().isoformat(),
            'note': 'Real LLM calls with manual few-shot optimization'
        }

        # Salvar métricas
        metrics_dir = Path('metrics/data/dspy_manual')
        metrics_dir.mkdir(parents=True, exist_ok=True)
        metrics_file = metrics_dir / f'baseline_{project[\"id\"]}.json'
        metrics_file.write_text(json.dumps(metrics, indent=2))

        print()
        print('=' * 80)
        print(f'✅ PROJETO {i} CONCLUÍDO')
        print('=' * 80)
        print(f'⏱️  Duração: {duration:.2f}s')
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
        })

    # Pausa entre projetos
    if i < len(TEST_PROJECTS):
        print('\\n⏸️  Aguardando 5 segundos antes do próximo projeto...')
        time.sleep(5)

batch_duration = time.time() - batch_start

# Gerar relatório
total_duration = sum(m['duration_seconds'] for m in all_metrics)
successful = sum(1 for m in all_metrics if m['status'] == 'success')

print()
print('=' * 80)
print('📊 RELATÓRIO BASELINE COM RAG + DSPy MANUAL - RESUMO')
print('=' * 80)
print()
print(f'Total de projetos: {len(all_metrics)}')
print(f'✅ Sucesso: {successful}')
print(f'❌ Falhas: {len(all_metrics) - successful}')
print(f'⏱️  Duração total: {total_duration:.2f}s ({total_duration/60:.1f} min)')
print(f'⏱️  Duração média: {total_duration/len(all_metrics):.2f}s por projeto')
print()

# Salvar relatório
report_path = Path('metrics/data/dspy_manual/baseline_report.json')
report = {
    'test_type': 'baseline_dspy_manual',
    'test_date': datetime.now().isoformat(),
    'total_projects': len(all_metrics),
    'successful': successful,
    'failed': len(all_metrics) - successful,
    'total_duration_seconds': round(total_duration, 2),
    'avg_duration_per_project_seconds': round(total_duration/len(all_metrics), 2),
    'projects': all_metrics,
}
report_path.write_text(json.dumps(report, indent=2))
print(f'💾 Relatório salvo em: {report_path}')

print()
print('=' * 80)
print('🎉 TESTE BASELINE COM RAG + DSPy MANUAL CONCLUÍDO!')
print('=' * 80)
print()
print('Este teste FEZ LLM CALLS REAIS com otimização manual!')
print()

# Finalizar AgentOps
try:
    import agentops
    agentops.end_session(end_state='Success')
except:
    pass

sys.exit(0)
"
