#!/usr/bin/env python3
"""
Script de Comparação entre Baselines
Compara baseline COM RAG vs baseline SEM RAG
"""
import json
import sys
from pathlib import Path
from datetime import datetime


def load_report(report_path: Path):
    """Carrega relatório JSON."""
    if not report_path.exists():
        return None

    try:
        return json.loads(report_path.read_text())
    except Exception as e:
        print(f"❌ Erro ao ler {report_path}: {e}")
        return None


def calculate_percentage_diff(value1, value2):
    """
    Calcula diferença percentual entre dois valores.
    Retorna: (diferença_percentual, símbolo)
    Positivo significa que value1 é maior que value2
    """
    if value2 == 0:
        return 0, "="

    diff = ((value1 - value2) / value2) * 100

    if abs(diff) < 0.01:
        return 0, "="
    elif diff > 0:
        return diff, "📈"
    else:
        return abs(diff), "📉"


def compare_reports(report_rag, report_no_rag):
    """Compara dois relatórios e gera análise."""
    print()
    print("=" * 100)
    print("📊 COMPARAÇÃO ENTRE BASELINES: COM RAG vs SEM RAG")
    print("=" * 100)
    print()

    # Informações básicas
    print("--- INFORMAÇÕES DOS TESTES ---")
    print()
    print(f"Baseline COM RAG:")
    print(f"  Data: {report_rag.get('timestamp', 'N/A')}")
    print(f"  Projetos executados: {report_rag.get('successful_projects', 0)}/{report_rag.get('total_projects', 0)}")
    print(f"  Duração total: {report_rag.get('batch_duration_seconds', 0):.2f}s ({report_rag.get('batch_duration_seconds', 0)/60:.1f} min)")
    print()

    print(f"Baseline SEM RAG:")
    print(f"  Data: {report_no_rag.get('timestamp', 'N/A')}")
    print(f"  Projetos executados: {report_no_rag.get('successful_projects', 0)}/{report_no_rag.get('total_projects', 0)}")
    print(f"  Duração total: {report_no_rag.get('batch_duration_seconds', 0):.2f}s ({report_no_rag.get('batch_duration_seconds', 0)/60:.1f} min)")
    print()

    # Extrair estatísticas
    stats_rag = report_rag.get('aggregated_stats', {})
    stats_no_rag = report_no_rag.get('aggregated_stats', {})

    # Comparar custos
    print("=" * 100)
    print("💰 COMPARAÇÃO DE CUSTOS")
    print("=" * 100)
    print()

    cost_rag = stats_rag.get('total_cost', 0)
    cost_no_rag = stats_no_rag.get('total_cost', 0)
    cost_diff, cost_symbol = calculate_percentage_diff(cost_rag, cost_no_rag)

    avg_cost_rag = stats_rag.get('avg_cost_per_project', 0)
    avg_cost_no_rag = stats_no_rag.get('avg_cost_per_project', 0)
    avg_cost_diff, avg_cost_symbol = calculate_percentage_diff(avg_cost_rag, avg_cost_no_rag)

    print(f"Custo Total:")
    print(f"  COM RAG:    ${cost_rag:.4f}")
    print(f"  SEM RAG:    ${cost_no_rag:.4f}")
    print(f"  Diferença:  {cost_symbol} {cost_diff:.2f}% {'(RAG mais caro)' if cost_rag > cost_no_rag else '(RAG mais barato)'}")
    print()

    print(f"Custo Médio por Projeto:")
    print(f"  COM RAG:    ${avg_cost_rag:.4f}")
    print(f"  SEM RAG:    ${avg_cost_no_rag:.4f}")
    print(f"  Diferença:  {avg_cost_symbol} {avg_cost_diff:.2f}% {'(RAG mais caro)' if avg_cost_rag > avg_cost_no_rag else '(RAG mais barato)'}")
    print()

    # Comparar tokens
    print("=" * 100)
    print("🎫 COMPARAÇÃO DE TOKENS")
    print("=" * 100)
    print()

    tokens_rag = stats_rag.get('total_tokens', 0)
    tokens_no_rag = stats_no_rag.get('total_tokens', 0)
    tokens_diff, tokens_symbol = calculate_percentage_diff(tokens_rag, tokens_no_rag)

    avg_tokens_rag = stats_rag.get('avg_tokens_per_project', 0)
    avg_tokens_no_rag = stats_no_rag.get('avg_tokens_per_project', 0)
    avg_tokens_diff, avg_tokens_symbol = calculate_percentage_diff(avg_tokens_rag, avg_tokens_no_rag)

    print(f"Tokens Totais:")
    print(f"  COM RAG:    {tokens_rag:,}")
    print(f"  SEM RAG:    {tokens_no_rag:,}")
    print(f"  Diferença:  {tokens_symbol} {tokens_diff:.2f}% {'(RAG usa mais)' if tokens_rag > tokens_no_rag else '(RAG usa menos)'}")
    print()

    print(f"Tokens Médios por Projeto:")
    print(f"  COM RAG:    {avg_tokens_rag:,}")
    print(f"  SEM RAG:    {avg_tokens_no_rag:,}")
    print(f"  Diferença:  {avg_tokens_symbol} {avg_tokens_diff:.2f}% {'(RAG usa mais)' if avg_tokens_rag > avg_tokens_no_rag else '(RAG usa menos)'}")
    print()

    # Comparar LLM calls
    print("=" * 100)
    print("📞 COMPARAÇÃO DE LLM CALLS")
    print("=" * 100)
    print()

    calls_rag = stats_rag.get('total_llm_calls', 0)
    calls_no_rag = stats_no_rag.get('total_llm_calls', 0)
    calls_diff, calls_symbol = calculate_percentage_diff(calls_rag, calls_no_rag)

    avg_calls_rag = stats_rag.get('avg_llm_calls_per_project', 0)
    avg_calls_no_rag = stats_no_rag.get('avg_llm_calls_per_project', 0)
    avg_calls_diff, avg_calls_symbol = calculate_percentage_diff(avg_calls_rag, avg_calls_no_rag)

    print(f"LLM Calls Totais:")
    print(f"  COM RAG:    {calls_rag}")
    print(f"  SEM RAG:    {calls_no_rag}")
    print(f"  Diferença:  {calls_symbol} {calls_diff:.2f}% {'(RAG faz mais calls)' if calls_rag > calls_no_rag else '(RAG faz menos calls)'}")
    print()

    print(f"LLM Calls Médias por Projeto:")
    print(f"  COM RAG:    {avg_calls_rag}")
    print(f"  SEM RAG:    {avg_calls_no_rag}")
    print(f"  Diferença:  {avg_calls_symbol} {avg_calls_diff:.2f}% {'(RAG faz mais calls)' if avg_calls_rag > avg_calls_no_rag else '(RAG faz menos calls)'}")
    print()

    # Comparar duração
    print("=" * 100)
    print("⏱️  COMPARAÇÃO DE PERFORMANCE (TEMPO)")
    print("=" * 100)
    print()

    duration_rag = stats_rag.get('avg_duration_per_project', 0)
    duration_no_rag = stats_no_rag.get('avg_duration_per_project', 0)
    duration_diff, duration_symbol = calculate_percentage_diff(duration_rag, duration_no_rag)

    print(f"Duração Média por Projeto:")
    print(f"  COM RAG:    {duration_rag:.2f}s ({duration_rag/60:.2f} min)")
    print(f"  SEM RAG:    {duration_no_rag:.2f}s ({duration_no_rag/60:.2f} min)")
    print(f"  Diferença:  {duration_symbol} {duration_diff:.2f}% {'(RAG mais lento)' if duration_rag > duration_no_rag else '(RAG mais rápido)'}")
    print()

    # RAG retrievals (apenas para baseline com RAG)
    retrievals_rag = stats_rag.get('total_rag_retrievals', 0)
    if retrievals_rag > 0:
        print("=" * 100)
        print("🔍 MÉTRICAS RAG")
        print("=" * 100)
        print()
        print(f"Total de RAG Retrievals: {retrievals_rag}")
        print(f"Média por Projeto: {retrievals_rag / report_rag.get('successful_projects', 1):.1f}")
        print()

    # Comparação por projeto
    print("=" * 100)
    print("📋 COMPARAÇÃO DETALHADA POR PROJETO")
    print("=" * 100)
    print()

    projects_rag = {p['project_id']: p for p in report_rag.get('projects', []) if p['status'] == 'success'}
    projects_no_rag = {p['project_id']: p for p in report_no_rag.get('projects', []) if p['status'] == 'success'}

    common_projects = set(projects_rag.keys()) & set(projects_no_rag.keys())

    for project_id in sorted(common_projects):
        p_rag = projects_rag[project_id]
        p_no_rag = projects_no_rag[project_id]

        print(f"Projeto: {p_rag['project_name']} ({project_id})")
        print("-" * 100)

        # Custo
        cost_p_rag = p_rag['metrics']['summary']['total_cost']
        cost_p_no_rag = p_no_rag['metrics']['summary']['total_cost']
        cost_p_diff, cost_p_symbol = calculate_percentage_diff(cost_p_rag, cost_p_no_rag)
        print(f"  Custo:      COM RAG ${cost_p_rag:.4f} | SEM RAG ${cost_p_no_rag:.4f} | Diff: {cost_p_symbol} {cost_p_diff:.2f}%")

        # Tokens
        tokens_p_rag = p_rag['metrics']['summary']['total_tokens']
        tokens_p_no_rag = p_no_rag['metrics']['summary']['total_tokens']
        tokens_p_diff, tokens_p_symbol = calculate_percentage_diff(tokens_p_rag, tokens_p_no_rag)
        print(f"  Tokens:     COM RAG {tokens_p_rag:,} | SEM RAG {tokens_p_no_rag:,} | Diff: {tokens_p_symbol} {tokens_p_diff:.2f}%")

        # Duração
        dur_p_rag = p_rag['duration_seconds']
        dur_p_no_rag = p_no_rag['duration_seconds']
        dur_p_diff, dur_p_symbol = calculate_percentage_diff(dur_p_rag, dur_p_no_rag)
        print(f"  Duração:    COM RAG {dur_p_rag:.2f}s | SEM RAG {dur_p_no_rag:.2f}s | Diff: {dur_p_symbol} {dur_p_diff:.2f}%")

        # LLM calls
        calls_p_rag = p_rag['metrics']['summary']['total_llm_calls']
        calls_p_no_rag = p_no_rag['metrics']['summary']['total_llm_calls']
        calls_p_diff, calls_p_symbol = calculate_percentage_diff(calls_p_rag, calls_p_no_rag)
        print(f"  LLM Calls:  COM RAG {calls_p_rag} | SEM RAG {calls_p_no_rag} | Diff: {calls_p_symbol} {calls_p_diff:.2f}%")

        print()

    # Resumo e conclusões
    print("=" * 100)
    print("📈 RESUMO EXECUTIVO")
    print("=" * 100)
    print()

    print("Impacto do RAG:")
    print()

    # Custo
    if cost_diff < 5:
        print(f"  💰 Custo: NEUTRO (diferença < 5%)")
    elif cost_rag > cost_no_rag:
        print(f"  💰 Custo: RAG aumenta custos em {cost_diff:.2f}%")
    else:
        print(f"  💰 Custo: RAG reduz custos em {cost_diff:.2f}%")

    # Tokens
    if tokens_diff < 5:
        print(f"  🎫 Tokens: NEUTRO (diferença < 5%)")
    elif tokens_rag > tokens_no_rag:
        print(f"  🎫 Tokens: RAG aumenta uso de tokens em {tokens_diff:.2f}%")
    else:
        print(f"  🎫 Tokens: RAG reduz uso de tokens em {tokens_diff:.2f}%")

    # Performance
    if duration_diff < 5:
        print(f"  ⏱️  Performance: NEUTRO (diferença < 5%)")
    elif duration_rag > duration_no_rag:
        print(f"  ⏱️  Performance: RAG aumenta tempo de execução em {duration_diff:.2f}%")
    else:
        print(f"  ⏱️  Performance: RAG reduz tempo de execução em {duration_diff:.2f}%")

    # LLM Calls
    if calls_diff < 5:
        print(f"  📞 LLM Calls: NEUTRO (diferença < 5%)")
    elif calls_rag > calls_no_rag:
        print(f"  📞 LLM Calls: RAG aumenta chamadas LLM em {calls_diff:.2f}%")
    else:
        print(f"  📞 LLM Calls: RAG reduz chamadas LLM em {calls_diff:.2f}%")

    print()

    # Salvar relatório de comparação
    comparison_report = {
        "timestamp": datetime.now().isoformat(),
        "baseline_with_rag": {
            "report_path": "metrics/data/baseline_report.json",
            "date": report_rag.get('timestamp'),
            "successful_projects": report_rag.get('successful_projects'),
            "stats": stats_rag,
        },
        "baseline_without_rag": {
            "report_path": "metrics/data/no_rag/baseline_report.json",
            "date": report_no_rag.get('timestamp'),
            "successful_projects": report_no_rag.get('successful_projects'),
            "stats": stats_no_rag,
        },
        "comparison": {
            "cost": {
                "with_rag": cost_rag,
                "without_rag": cost_no_rag,
                "difference_percent": cost_diff if cost_rag > cost_no_rag else -cost_diff,
                "impact": "increase" if cost_rag > cost_no_rag else "decrease",
            },
            "tokens": {
                "with_rag": tokens_rag,
                "without_rag": tokens_no_rag,
                "difference_percent": tokens_diff if tokens_rag > tokens_no_rag else -tokens_diff,
                "impact": "increase" if tokens_rag > tokens_no_rag else "decrease",
            },
            "duration": {
                "with_rag": duration_rag,
                "without_rag": duration_no_rag,
                "difference_percent": duration_diff if duration_rag > duration_no_rag else -duration_diff,
                "impact": "increase" if duration_rag > duration_no_rag else "decrease",
            },
            "llm_calls": {
                "with_rag": calls_rag,
                "without_rag": calls_no_rag,
                "difference_percent": calls_diff if calls_rag > calls_no_rag else -calls_diff,
                "impact": "increase" if calls_rag > calls_no_rag else "decrease",
            },
        },
    }

    comparison_path = Path("metrics/data/comparison_report.json")
    comparison_path.write_text(json.dumps(comparison_report, indent=2))

    print(f"💾 Relatório de comparação salvo em: {comparison_path}")
    print()


def main():
    """Main function."""
    print()
    print("🔍 Buscando relatórios de baseline...")
    print()

    # Caminhos dos relatórios
    report_rag_path = Path("metrics/data/baseline_report.json")
    report_no_rag_path = Path("metrics/data/no_rag/baseline_report.json")

    # Carregar relatórios
    report_rag = load_report(report_rag_path)
    report_no_rag = load_report(report_no_rag_path)

    # Verificar se ambos existem
    if not report_rag:
        print(f"❌ Relatório COM RAG não encontrado em: {report_rag_path}")
        print("   Execute primeiro: ./scripts/run_baseline_test.sh")
        print()
        return 1

    if not report_no_rag:
        print(f"❌ Relatório SEM RAG não encontrado em: {report_no_rag_path}")
        print("   Execute primeiro: ./scripts/run_baseline_no_rag.sh")
        print()
        return 1

    print(f"✅ Relatório COM RAG carregado: {report_rag_path}")
    print(f"✅ Relatório SEM RAG carregado: {report_no_rag_path}")

    # Comparar
    compare_reports(report_rag, report_no_rag)

    print("=" * 100)
    print("✅ ANÁLISE COMPARATIVA CONCLUÍDA")
    print("=" * 100)
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
