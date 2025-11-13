#!/usr/bin/env python3
"""
Teste baseline COM RAG + DSPy (Pipeline Fresh - LLM Calls Reais).
Usa agentes DSPy otimizados MAS sem demos pré-compiladas.
Faz LLM calls reais e gera métricas reais.
"""
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from crew_dspy import SoftwareDevPipeline, save_pipeline_outputs
from dspy_config import configure_dspy

# Projetos de teste
TEST_PROJECTS = [
    {
        "id": "project_01",
        "name": "Todo List CLI",
        "description": "crie uma aplicação CLI para gerenciar lista de tarefas com comandos add, list, done e delete"
    },
    {
        "id": "project_02",
        "name": "URL Shortener API",
        "description": "crie uma API REST para encurtar URLs com endpoints para criar, listar e redirecionar"
    },
    {
        "id": "project_03",
        "name": "Weather CLI",
        "description": "crie uma ferramenta CLI que consulta API de clima e mostra previsão formatada"
    },
    {
        "id": "project_04",
        "name": "Password Generator",
        "description": "crie um gerador de senhas seguras CLI com opções de tamanho, caracteres especiais e força"
    },
    {
        "id": "project_05",
        "name": "Markdown to HTML Converter",
        "description": "crie um conversor de Markdown para HTML com suporte a títulos, listas e links"
    },
]


def initialize_observability():
    """Inicializa AgentOps se disponível."""
    try:
        import agentops
        if config.AGENTOPS_API_KEY:
            agentops.init(
                api_key=config.AGENTOPS_API_KEY,
                tags=["baseline", "dspy-fresh", "rag"]
            )
            print("✅ AgentOps inicializado")
            return True
        else:
            print("⚠️  AgentOps API key não configurada")
            return False
    except Exception as e:
        print(f"⚠️  AgentOps não disponível: {e}")
        return False


def run_single_project(project: dict, index: int, total: int, pipeline: SoftwareDevPipeline) -> dict:
    """
    Executa um único projeto e coleta métricas.

    Args:
        project: Dicionário com informações do projeto
        index: Índice do projeto (1-based)
        total: Total de projetos
        pipeline: Pipeline DSPy fresh (sem otimização)

    Returns:
        Dicionário com métricas do projeto
    """
    print()
    print("=" * 80)
    print(f"📋 PROJETO {index}/{total}: {project['name']}")
    print(f"ID: {project['id']}")
    print("=" * 80)
    print()

    start_time = time.time()

    try:
        # Executar pipeline DSPy fresh (faz LLM calls reais!)
        result = pipeline(project_idea=project['description'])

        # Salvar outputs
        save_pipeline_outputs(result, project['description'])

        duration = time.time() - start_time

        # Métricas básicas (AgentOps trackeia LLM calls automaticamente)
        metrics = {
            "project_id": project['id'],
            "project_name": project['name'],
            "status": "success",
            "duration_seconds": round(duration, 2),
            "cost_usd": 0.0,  # AgentOps trackeia custo
            "tokens_used": 0,  # AgentOps trackeia tokens
            "llm_calls": 0,  # AgentOps trackeia calls
            "timestamp": datetime.now().isoformat(),
            "note": "Metrics tracked by AgentOps - check dashboard"
        }

        # Salvar métricas individuais
        metrics_dir = Path("metrics/data/dspy_fresh")
        metrics_dir.mkdir(parents=True, exist_ok=True)

        metrics_file = metrics_dir / f"baseline_{project['id']}.json"
        metrics_file.write_text(json.dumps(metrics, indent=2))

        print()
        print("=" * 80)
        print(f"✅ PROJETO {index} CONCLUÍDO")
        print("=" * 80)
        print(f"⏱️  Duração: {duration:.2f}s")
        print(f"💰 Custo: ${metrics['cost_usd']:.4f}")
        print(f"🎫 Tokens: {metrics['tokens_used']}")
        print(f"📊 LLM Calls: {metrics['llm_calls']}")
        print()

        return metrics

    except Exception as e:
        duration = time.time() - start_time

        print()
        print("=" * 80)
        print(f"❌ PROJETO {index} FALHOU")
        print("=" * 80)
        print(f"Erro: {e}")
        print()

        import traceback
        traceback.print_exc()

        return {
            "project_id": project['id'],
            "project_name": project['name'],
            "status": "error",
            "duration_seconds": round(duration, 2),
            "cost_usd": 0.0,
            "tokens_used": 0,
            "llm_calls": 0,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def generate_consolidated_report(all_metrics: list) -> None:
    """Gera relatório consolidado de todos os projetos."""

    # Calcular estatísticas
    total_projects = len(all_metrics)
    successful = sum(1 for m in all_metrics if m['status'] == 'success')
    failed = total_projects - successful

    total_duration = sum(m['duration_seconds'] for m in all_metrics)
    total_cost = sum(m['cost_usd'] for m in all_metrics)
    total_tokens = sum(m['tokens_used'] for m in all_metrics)
    total_llm_calls = sum(m['llm_calls'] for m in all_metrics)

    avg_duration = total_duration / total_projects if total_projects > 0 else 0
    avg_cost = total_cost / total_projects if total_projects > 0 else 0
    avg_tokens = total_tokens / total_projects if total_projects > 0 else 0
    avg_llm_calls = total_llm_calls / total_projects if total_projects > 0 else 0

    print()
    print("=" * 80)
    print("📊 RELATÓRIO BASELINE COM RAG + DSPy (FRESH) - RESUMO CONSOLIDADO")
    print("=" * 80)
    print()
    print(f"Total de projetos: {total_projects}")
    print(f"✅ Sucesso: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"⏱️  Duração total: {total_duration:.2f}s ({total_duration/60:.1f} min)")
    print()
    print("--- ESTATÍSTICAS AGREGADAS (COM RAG + DSPy FRESH) ---")
    print(f"💰 Custo total: ${total_cost:.4f}")
    print(f"💰 Custo médio por projeto: ${avg_cost:.4f}")
    print(f"🎫 Tokens totais: {total_tokens}")
    print(f"🎫 Tokens médios por projeto: {int(avg_tokens)}")
    print(f"📞 LLM calls totais: {total_llm_calls}")
    print(f"📞 LLM calls médias: {int(avg_llm_calls)}")
    print(f"⏱️  Duração média por projeto: {avg_duration:.2f}s")
    print()
    print("--- DETALHES POR PROJETO ---")
    print()

    for i, metrics in enumerate(all_metrics, 1):
        status_icon = "✅" if metrics['status'] == 'success' else "❌"
        print(f"{i}. {metrics['project_name']} ({metrics['project_id']})")
        print(f"   Status: {status_icon} {metrics['status']}")
        print(f"   Duração: {metrics['duration_seconds']:.2f}s")
        print(f"   Custo: ${metrics['cost_usd']:.4f}")
        print(f"   Tokens: {metrics['tokens_used']}")
        print(f"   LLM calls: {metrics['llm_calls']}")
        if 'error' in metrics:
            print(f"   Erro: {metrics['error']}")
        print()

    # Salvar relatório consolidado
    report_path = Path("metrics/data/dspy_fresh/baseline_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    consolidated_report = {
        "test_type": "baseline_dspy_fresh",
        "test_date": datetime.now().isoformat(),
        "total_projects": total_projects,
        "successful": successful,
        "failed": failed,
        "total_duration_seconds": round(total_duration, 2),
        "aggregated_metrics": {
            "total_cost_usd": round(total_cost, 4),
            "avg_cost_per_project_usd": round(avg_cost, 4),
            "total_tokens": total_tokens,
            "avg_tokens_per_project": int(avg_tokens),
            "total_llm_calls": total_llm_calls,
            "avg_llm_calls_per_project": int(avg_llm_calls),
            "avg_duration_per_project_seconds": round(avg_duration, 2),
        },
        "projects": all_metrics,
    }

    report_path.write_text(json.dumps(consolidated_report, indent=2))
    print(f"💾 Relatório consolidado salvo em: {report_path}")
    print()


def main():
    """Executa teste baseline COM RAG + DSPy fresh completo."""
    print()
    print("=" * 80)
    print("🧪 TESTE BASELINE COM RAG + DSPy (FRESH - LLM CALLS REAIS)")
    print("=" * 80)
    print()
    print("Este teste usa agentes DSPy COM RAG fazendo LLM calls reais.")
    print("ATENÇÃO: Não usa pipeline otimizado, faz chamadas LLM reais!")
    print()

    # Verificar API key
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY não configurada!")
        print("   Configure no arquivo .env antes de executar.")
        return 1

    print(f"✅ API Key configurada")
    print()

    # Configurar DSPy
    print("⚙️  Configurando DSPy...")
    configure_dspy()
    print()

    # Criar pipeline FRESH (sem demos pré-compiladas)
    print("🏗️  Criando pipeline DSPy fresh (sem otimização)...")
    fresh_pipeline = SoftwareDevPipeline()
    print("✅ Pipeline fresh criado - fará LLM calls reais!")
    print()

    # Inicializar sistemas
    observability_enabled = initialize_observability()
    print("✅ RAG HABILITADO + DSPy FRESH (LLM calls reais)")
    print()

    # Confirmar execução
    print(f"📋 Projetos a serem executados: {len(TEST_PROJECTS)}")
    for i, proj in enumerate(TEST_PROJECTS, 1):
        print(f"   {i}. {proj['name']} ({proj['id']})")
    print()

    # Skip confirmation if --yes flag is provided
    if "--yes" not in sys.argv and "-y" not in sys.argv:
        input("Pressione ENTER para iniciar ou Ctrl+C para cancelar...")
    print()

    # Executar batch
    batch_start = time.time()
    all_metrics = []

    try:
        for i, project in enumerate(TEST_PROJECTS, 1):
            metrics = run_single_project(project, i, len(TEST_PROJECTS), fresh_pipeline)
            all_metrics.append(metrics)

            # Pequena pausa entre projetos
            if i < len(TEST_PROJECTS):
                print("\n⏸️  Aguardando 5 segundos antes do próximo projeto...")
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        if observability_enabled:
            import agentops
            agentops.end_session(end_state="Indeterminate")
        return 1

    batch_duration = time.time() - batch_start

    # Gerar relatório consolidado
    generate_consolidated_report(all_metrics)

    # Finalizar observability
    if observability_enabled:
        try:
            import agentops
            agentops.end_session(end_state="Success")
        except:
            pass

    print()
    print("=" * 80)
    print("🎉 TESTE BASELINE COM RAG + DSPy (FRESH) CONCLUÍDO!")
    print("=" * 80)
    print()
    print("Próximos passos:")
    print("  1. Revise o relatório em metrics/data/dspy_fresh/baseline_report.json")
    print("  2. Compare com outros baselines")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
