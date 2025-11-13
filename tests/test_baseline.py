#!/usr/bin/env python3
"""
Teste Baseline - Executa 5 projetos em sequência
Coleta métricas detalhadas para comparação futura (RAG, otimizado, etc)

Este script serve como baseline para estudos comparativos.
"""
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

# Import após carregar env
import openai
import langchain
import langchain_openai
from crewai import Agent, Task, Crew

import agentops
from crew import run_software_dev_crew
import config
from rag import setup_knowledge_base
from metrics import get_tracker, reset_tracker


# 5 projetos de teste para baseline
TEST_PROJECTS = [
    {
        "id": "project_01",
        "name": "Todo List CLI",
        "description": "crie uma aplicação CLI para gerenciar lista de tarefas com comandos add, list, done e delete",
    },
    {
        "id": "project_02",
        "name": "URL Shortener API",
        "description": "crie uma API REST para encurtar URLs com endpoints para criar, listar e redirecionar",
    },
    {
        "id": "project_03",
        "name": "Weather CLI",
        "description": "crie uma ferramenta CLI que consulta API de clima e mostra previsão formatada",
    },
    {
        "id": "project_04",
        "name": "Password Generator",
        "description": "crie um gerador de senhas seguras CLI com opções de tamanho, caracteres especiais e força",
    },
    {
        "id": "project_05",
        "name": "Markdown to HTML Converter",
        "description": "crie um conversor de Markdown para HTML com suporte a títulos, listas e links",
    },
]


def initialize_observability():
    """Initialize AgentOps if available."""
    if not config.AGENTOPS_API_KEY:
        print("⚠️  AgentOps não configurado - rodando sem observabilidade")
        return False

    try:
        agentops.init(
            api_key=config.AGENTOPS_API_KEY,
            default_tags=["baseline-test", "batch-run"],
            auto_start_session=True,
            instrument_llm_calls=True,
        )
        print("✅ AgentOps inicializado")
        return True
    except Exception as e:
        print(f"⚠️  Erro ao inicializar AgentOps: {e}")
        return False


def initialize_rag():
    """Initialize RAG system."""
    print("🔍 Inicializando RAG System...")
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("⚠️  Knowledge base não encontrada - RAG desabilitado")
        return False

    try:
        vector_store = setup_knowledge_base(str(kb_path))
        stats = vector_store.get_stats()
        print(f"✅ RAG inicializado: {stats['total_documents']} documentos")
        return True
    except Exception as e:
        print(f"⚠️  Erro ao inicializar RAG: {e}")
        return False


def run_single_project(project_info: dict, project_num: int, total: int):
    """
    Executa um único projeto e coleta métricas.

    Returns:
        dict: Métricas do projeto
    """
    print("\n" + "=" * 80)
    print(f"📋 PROJETO {project_num}/{total}: {project_info['name']}")
    print(f"ID: {project_info['id']}")
    print("=" * 80)
    print()

    # Reset tracker para este projeto
    tracker = reset_tracker()
    start_time = time.time()

    try:
        # Executar crew
        result = run_software_dev_crew(project_info['description'])

        # Calcular duração total
        duration = time.time() - start_time

        # Coletar métricas
        summary = tracker.get_summary()

        # Salvar métricas específicas deste projeto
        metrics_file = Path("metrics/data") / f"baseline_{project_info['id']}.json"
        metrics_file.parent.mkdir(parents=True, exist_ok=True)

        project_metrics = {
            "project_id": project_info['id'],
            "project_name": project_info['name'],
            "description": project_info['description'],
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration,
            "status": "success",
            "metrics": summary,
        }

        metrics_file.write_text(json.dumps(project_metrics, indent=2))

        print()
        print("=" * 80)
        print(f"✅ PROJETO {project_num} CONCLUÍDO")
        print("=" * 80)
        print(f"⏱️  Duração: {duration:.2f}s")
        print(f"💰 Custo: ${summary['summary']['total_cost']:.4f}")
        print(f"🎫 Tokens: {summary['summary']['total_tokens']:,}")
        print(f"📊 LLM Calls: {summary['summary']['total_llm_calls']}")
        if summary['summary']['total_retrievals'] > 0:
            print(f"🔍 RAG Retrievals: {summary['summary']['total_retrievals']}")
        print()

        return project_metrics

    except Exception as e:
        print(f"\n❌ ERRO no projeto {project_num}: {e}")
        duration = time.time() - start_time

        error_metrics = {
            "project_id": project_info['id'],
            "project_name": project_info['name'],
            "description": project_info['description'],
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration,
            "status": "failed",
            "error": str(e),
            "metrics": None,
        }

        return error_metrics


def generate_baseline_report(all_metrics: list, batch_duration: float):
    """
    Gera relatório consolidado do baseline.

    Args:
        all_metrics: Lista de métricas de todos os projetos
        batch_duration: Duração total do batch
    """
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO BASELINE - RESUMO CONSOLIDADO")
    print("=" * 80)
    print()

    # Filtrar sucessos e falhas
    successful = [m for m in all_metrics if m['status'] == 'success']
    failed = [m for m in all_metrics if m['status'] == 'failed']

    print(f"Total de projetos: {len(all_metrics)}")
    print(f"✅ Sucesso: {len(successful)}")
    print(f"❌ Falhas: {len(failed)}")
    print(f"⏱️  Duração total: {batch_duration:.2f}s ({batch_duration/60:.1f} min)")
    print()

    if not successful:
        print("⚠️  Nenhum projeto concluído com sucesso")
        return

    # Calcular estatísticas agregadas
    total_cost = sum(m['metrics']['summary']['total_cost'] for m in successful)
    total_tokens = sum(m['metrics']['summary']['total_tokens'] for m in successful)
    total_llm_calls = sum(m['metrics']['summary']['total_llm_calls'] for m in successful)
    total_retrievals = sum(m['metrics']['summary'].get('total_retrievals', 0) for m in successful)
    avg_duration = sum(m['duration_seconds'] for m in successful) / len(successful)

    print("--- ESTATÍSTICAS AGREGADAS ---")
    print(f"💰 Custo total: ${total_cost:.4f}")
    print(f"💰 Custo médio por projeto: ${total_cost/len(successful):.4f}")
    print(f"🎫 Tokens totais: {total_tokens:,}")
    print(f"🎫 Tokens médios por projeto: {total_tokens//len(successful):,}")
    print(f"📞 LLM calls totais: {total_llm_calls}")
    print(f"📞 LLM calls médias: {total_llm_calls//len(successful)}")
    if total_retrievals > 0:
        print(f"🔍 RAG retrievals totais: {total_retrievals}")
        print(f"🔍 RAG retrievals médias: {total_retrievals//len(successful)}")
    print(f"⏱️  Duração média por projeto: {avg_duration:.2f}s")
    print()

    print("--- DETALHES POR PROJETO ---")
    for i, metrics in enumerate(successful, 1):
        print(f"\n{i}. {metrics['project_name']} ({metrics['project_id']})")
        print(f"   Status: {metrics['status']}")
        print(f"   Duração: {metrics['duration_seconds']:.2f}s")
        print(f"   Custo: ${metrics['metrics']['summary']['total_cost']:.4f}")
        print(f"   Tokens: {metrics['metrics']['summary']['total_tokens']:,}")
        print(f"   LLM calls: {metrics['metrics']['summary']['total_llm_calls']}")

    if failed:
        print("\n--- PROJETOS COM FALHA ---")
        for i, metrics in enumerate(failed, 1):
            print(f"\n{i}. {metrics['project_name']} ({metrics['project_id']})")
            print(f"   Erro: {metrics['error']}")
            print(f"   Duração antes da falha: {metrics['duration_seconds']:.2f}s")

    # Salvar relatório consolidado
    report_path = Path("metrics/data/baseline_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    consolidated_report = {
        "report_type": "baseline",
        "timestamp": datetime.now().isoformat(),
        "batch_duration_seconds": batch_duration,
        "total_projects": len(all_metrics),
        "successful_projects": len(successful),
        "failed_projects": len(failed),
        "aggregated_stats": {
            "total_cost": total_cost,
            "avg_cost_per_project": total_cost / len(successful) if successful else 0,
            "total_tokens": total_tokens,
            "avg_tokens_per_project": total_tokens // len(successful) if successful else 0,
            "total_llm_calls": total_llm_calls,
            "avg_llm_calls_per_project": total_llm_calls // len(successful) if successful else 0,
            "total_rag_retrievals": total_retrievals,
            "avg_duration_per_project": avg_duration if successful else 0,
        },
        "projects": all_metrics,
    }

    report_path.write_text(json.dumps(consolidated_report, indent=2))
    print(f"\n💾 Relatório consolidado salvo em: {report_path}")
    print()


def main():
    """Executa teste baseline completo."""
    print()
    print("=" * 80)
    print("🧪 TESTE BASELINE - BATCH DE 5 PROJETOS")
    print("=" * 80)
    print()
    print("Este teste executa 5 projetos em sequência para estabelecer baseline.")
    print("Métricas coletadas servirão como referência para comparações futuras.")
    print()

    # Verificar API key
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY não configurada!")
        print("   Configure no arquivo .env antes de executar.")
        return 1

    print(f"✅ API Key configurada")
    print()

    # Inicializar sistemas
    observability_enabled = initialize_observability()
    rag_enabled = initialize_rag()
    print()

    # Confirmar execução
    print(f"📋 Projetos a serem executados: {len(TEST_PROJECTS)}")
    for i, proj in enumerate(TEST_PROJECTS, 1):
        print(f"   {i}. {proj['name']} ({proj['id']})")
    print()

    input("Pressione ENTER para iniciar ou Ctrl+C para cancelar...")
    print()

    # Executar batch
    batch_start = time.time()
    all_metrics = []

    try:
        for i, project in enumerate(TEST_PROJECTS, 1):
            metrics = run_single_project(project, i, len(TEST_PROJECTS))
            all_metrics.append(metrics)

            # Pequena pausa entre projetos
            if i < len(TEST_PROJECTS):
                print("\n⏸️  Aguardando 5 segundos antes do próximo projeto...")
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        if observability_enabled:
            agentops.end_session(end_state="Indeterminate")
        return 130

    batch_duration = time.time() - batch_start

    # Gerar relatório
    generate_baseline_report(all_metrics, batch_duration)

    # Finalizar observability
    if observability_enabled:
        agentops.end_session(end_state="Success")

    print()
    print("=" * 80)
    print("🎉 TESTE BASELINE CONCLUÍDO!")
    print("=" * 80)
    print()
    print("Próximos passos:")
    print("  1. Revise o relatório em metrics/data/baseline_report.json")
    print("  2. Compare com testes futuros (RAG, otimizado)")
    print("  3. Veja PLANO_ESTUDO_RAG_METRICAS.md para metodologia completa")
    print()

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
