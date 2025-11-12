#!/usr/bin/env python3
"""
Script rápido para analisar resultados do baseline.
Lê o relatório e mostra estatísticas de forma amigável.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any


def format_duration(seconds: float) -> str:
    """Formata duração em formato legível."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}min"
    hours = minutes / 60
    return f"{hours:.1f}h"


def analyze_report(report_path: Path) -> None:
    """Analisa e exibe relatório baseline."""

    if not report_path.exists():
        print(f"❌ Relatório não encontrado: {report_path}")
        print()
        print("Execute o teste baseline primeiro:")
        print("  ./run_baseline_test.sh")
        return

    # Carregar relatório
    report = json.loads(report_path.read_text())

    print("\n" + "=" * 80)
    print("📊 ANÁLISE DO BASELINE")
    print("=" * 80)
    print()

    # Informações gerais
    print(f"Timestamp: {report['timestamp']}")
    print(f"Duração do batch: {format_duration(report['batch_duration_seconds'])}")
    print()

    # Resumo de projetos
    total = report['total_projects']
    success = report['successful_projects']
    failed = report['failed_projects']
    success_rate = (success / total * 100) if total > 0 else 0

    print("--- RESUMO DE EXECUÇÃO ---")
    print(f"Total de projetos: {total}")
    print(f"✅ Sucesso: {success} ({success_rate:.1f}%)")
    print(f"❌ Falhas: {failed}")
    print()

    if success == 0:
        print("⚠️  Nenhum projeto foi concluído com sucesso")
        return

    # Estatísticas agregadas
    stats = report['aggregated_stats']

    print("--- CUSTOS ---")
    print(f"💰 Custo total: ${stats['total_cost']:.4f}")
    print(f"💰 Custo médio/projeto: ${stats['avg_cost_per_project']:.4f}")
    print(f"💰 Custo por 10 projetos (estimado): ${stats['avg_cost_per_project'] * 10:.2f}")
    print()

    print("--- TOKENS ---")
    print(f"🎫 Total de tokens: {stats['total_tokens']:,}")
    print(f"🎫 Média/projeto: {stats['avg_tokens_per_project']:,}")
    print(f"🎫 Tokens prompt (est. 40%): {int(stats['total_tokens'] * 0.4):,}")
    print(f"🎫 Tokens completion (est. 60%): {int(stats['total_tokens'] * 0.6):,}")
    print()

    print("--- PERFORMANCE ---")
    print(f"📞 LLM calls totais: {stats['total_llm_calls']}")
    print(f"📞 Média/projeto: {stats['avg_llm_calls_per_project']}")
    print(f"⏱️  Duração média/projeto: {format_duration(stats['avg_duration_per_project'])}")
    print(f"🚀 Throughput: {60 / stats['avg_duration_per_project']:.2f} projetos/hora")
    if stats['total_rag_retrievals'] > 0:
        print(f"🔍 RAG retrievals: {stats['total_rag_retrievals']}")
        print(f"🔍 Média/projeto: {stats['total_rag_retrievals'] // success}")
    print()

    # Análise por projeto
    print("--- DETALHES POR PROJETO ---")
    print()

    projects = [p for p in report['projects'] if p['status'] == 'success']

    # Ordenar por custo
    projects_by_cost = sorted(projects, key=lambda p: p['metrics']['summary']['total_cost'], reverse=True)

    print("🔝 Top 3 mais caros:")
    for i, proj in enumerate(projects_by_cost[:3], 1):
        cost = proj['metrics']['summary']['total_cost']
        tokens = proj['metrics']['summary']['total_tokens']
        print(f"  {i}. {proj['project_name']}: ${cost:.4f} ({tokens:,} tokens)")
    print()

    # Ordenar por duração
    projects_by_time = sorted(projects, key=lambda p: p['duration_seconds'], reverse=True)

    print("⏱️  Top 3 mais lentos:")
    for i, proj in enumerate(projects_by_time[:3], 1):
        duration = proj['duration_seconds']
        print(f"  {i}. {proj['project_name']}: {format_duration(duration)}")
    print()

    # Projeções
    print("--- PROJEÇÕES ---")
    print()
    print("Se executar 50 projetos (estudo completo):")
    total_50 = stats['avg_cost_per_project'] * 50
    time_50 = stats['avg_duration_per_project'] * 50
    print(f"  💰 Custo estimado: ${total_50:.2f}")
    print(f"  ⏱️  Tempo estimado: {format_duration(time_50)}")
    print(f"  🎫 Tokens estimados: {stats['avg_tokens_per_project'] * 50:,}")
    print()

    print("Se executar 3 fases (baseline + RAG + otimizado) com 50 projetos cada:")
    total_150 = total_50 * 3
    time_150 = time_50 * 3
    print(f"  💰 Custo estimado: ${total_150:.2f}")
    print(f"  ⏱️  Tempo estimado: {format_duration(time_150)}")
    print()

    # Comparação com outros testes (se existirem)
    rag_report_path = report_path.parent / "rag_report.json"
    if rag_report_path.exists():
        print("--- COMPARAÇÃO COM RAG ---")
        rag_report = json.loads(rag_report_path.read_text())
        rag_stats = rag_report['aggregated_stats']

        cost_diff = ((stats['avg_cost_per_project'] - rag_stats['avg_cost_per_project']) /
                    stats['avg_cost_per_project'] * 100)
        time_diff = ((stats['avg_duration_per_project'] - rag_stats['avg_duration_per_project']) /
                    stats['avg_duration_per_project'] * 100)

        print(f"  💰 Diferença de custo: {cost_diff:+.1f}%")
        print(f"  ⏱️  Diferença de tempo: {time_diff:+.1f}%")
        print()

    print("=" * 80)
    print()


def main():
    """Entry point."""
    report_path = Path("metrics/data/baseline_report.json")

    if len(sys.argv) > 1:
        report_path = Path(sys.argv[1])

    analyze_report(report_path)


if __name__ == "__main__":
    main()
