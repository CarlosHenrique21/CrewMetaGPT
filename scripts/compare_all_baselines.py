#!/usr/bin/env python3
"""
Script de Comparação Completa: SEM RAG vs COM RAG vs COM RAG + DSPy
Compara os 3 baselines e gera análise detalhada
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
    """Calcula diferença percentual entre dois valores."""
    if value2 == 0:
        return 0, "="
    diff = ((value1 - value2) / value2) * 100
    if abs(diff) < 0.01:
        return 0, "="
    elif diff > 0:
        return diff, "📈"
    else:
        return abs(diff), "📉"


def compare_three_baselines(report_no_rag, report_rag, report_dspy):
    """Compara os 3 relatórios e gera análise completa."""
    print()
    print("=" * 100)
    print("📊 COMPARAÇÃO COMPLETA: 3 BASELINES")
    print("=" * 100)
    print()
    print("  1️⃣  SEM RAG (baseline)")
    print("  2️⃣  COM RAG (RAG integrado)")
    print("  3️⃣  COM RAG + DSPy (otimizado)")
    print()
    print("=" * 100)
    print()

    # Informações básicas
    print("--- INFORMAÇÕES DOS TESTES ---")
    print()
    print(f"1️⃣  Baseline SEM RAG:")
    print(f"  Data: {report_no_rag.get('timestamp', 'N/A')}")
    print(f"  Projetos: {report_no_rag.get('successful_projects', 0)}/{report_no_rag.get('total_projects', 0)}")
    print(f"  Duração: {report_no_rag.get('batch_duration_seconds', 0):.2f}s")
    print()

    print(f"2️⃣  Baseline COM RAG:")
    print(f"  Data: {report_rag.get('timestamp', 'N/A')}")
    print(f"  Projetos: {report_rag.get('successful_projects', 0)}/{report_rag.get('total_projects', 0)}")
    print(f"  Duração: {report_rag.get('batch_duration_seconds', 0):.2f}s")
    print()

    print(f"3️⃣  Baseline COM RAG + DSPy:")
    print(f"  Data: {report_dspy.get('timestamp', 'N/A')}")
    print(f"  Projetos: {report_dspy.get('successful_projects', 0)}/{report_dspy.get('total_projects', 0)}")
    print(f"  Duração: {report_dspy.get('batch_duration_seconds', 0):.2f}s")
    print()

    # Extrair estatísticas
    stats_no_rag = report_no_rag.get('aggregated_stats', {})
    stats_rag = report_rag.get('aggregated_stats', {})
    stats_dspy = report_dspy.get('aggregated_stats', {})

    # === COMPARAÇÃO DE CUSTOS ===
    print("=" * 100)
    print("💰 COMPARAÇÃO DE CUSTOS")
    print("=" * 100)
    print()

    cost_no_rag = stats_no_rag.get('total_cost', 0)
    cost_rag = stats_rag.get('total_cost', 0)
    cost_dspy = stats_dspy.get('total_cost', 0)

    avg_cost_no_rag = stats_no_rag.get('avg_cost_per_project', 0)
    avg_cost_rag = stats_rag.get('avg_cost_per_project', 0)
    avg_cost_dspy = stats_dspy.get('avg_cost_per_project', 0)

    print("Custo Total:")
    print(f"  1️⃣  SEM RAG:          ${cost_no_rag:.4f}")
    print(f"  2️⃣  COM RAG:          ${cost_rag:.4f}")
    print(f"  3️⃣  COM RAG + DSPy:   ${cost_dspy:.4f}")
    print()

    # Comparações
    diff_rag_vs_no_rag, symbol1 = calculate_percentage_diff(cost_rag, cost_no_rag)
    diff_dspy_vs_rag, symbol2 = calculate_percentage_diff(cost_dspy, cost_rag)
    diff_dspy_vs_no_rag, symbol3 = calculate_percentage_diff(cost_dspy, cost_no_rag)

    print("Comparações:")
    print(f"  RAG vs SEM RAG:        {symbol1} {diff_rag_vs_no_rag:.2f}%")
    print(f"  DSPy vs RAG:           {symbol2} {diff_dspy_vs_rag:.2f}%")
    print(f"  DSPy vs SEM RAG:       {symbol3} {diff_dspy_vs_no_rag:.2f}%")
    print()

    print("Custo Médio por Projeto:")
    print(f"  1️⃣  SEM RAG:          ${avg_cost_no_rag:.4f}")
    print(f"  2️⃣  COM RAG:          ${avg_cost_rag:.4f}")
    print(f"  3️⃣  COM RAG + DSPy:   ${avg_cost_dspy:.4f}")
    print()

    # === COMPARAÇÃO DE TOKENS ===
    print("=" * 100)
    print("🎫 COMPARAÇÃO DE TOKENS")
    print("=" * 100)
    print()

    tokens_no_rag = stats_no_rag.get('total_tokens', 0)
    tokens_rag = stats_rag.get('total_tokens', 0)
    tokens_dspy = stats_dspy.get('total_tokens', 0)

    print("Tokens Totais:")
    print(f"  1️⃣  SEM RAG:          {tokens_no_rag:,}")
    print(f"  2️⃣  COM RAG:          {tokens_rag:,}")
    print(f"  3️⃣  COM RAG + DSPy:   {tokens_dspy:,}")
    print()

    diff_rag_vs_no_rag_t, symbol1_t = calculate_percentage_diff(tokens_rag, tokens_no_rag)
    diff_dspy_vs_rag_t, symbol2_t = calculate_percentage_diff(tokens_dspy, tokens_rag)
    diff_dspy_vs_no_rag_t, symbol3_t = calculate_percentage_diff(tokens_dspy, tokens_no_rag)

    print("Comparações:")
    print(f"  RAG vs SEM RAG:        {symbol1_t} {diff_rag_vs_no_rag_t:.2f}%")
    print(f"  DSPy vs RAG:           {symbol2_t} {diff_dspy_vs_rag_t:.2f}%")
    print(f"  DSPy vs SEM RAG:       {symbol3_t} {diff_dspy_vs_no_rag_t:.2f}%")
    print()

    # === COMPARAÇÃO DE PERFORMANCE ===
    print("=" * 100)
    print("⏱️  COMPARAÇÃO DE PERFORMANCE (TEMPO)")
    print("=" * 100)
    print()

    duration_no_rag = stats_no_rag.get('avg_duration_per_project', 0)
    duration_rag = stats_rag.get('avg_duration_per_project', 0)
    duration_dspy = stats_dspy.get('avg_duration_per_project', 0)

    print("Duração Média por Projeto:")
    print(f"  1️⃣  SEM RAG:          {duration_no_rag:.2f}s ({duration_no_rag/60:.2f} min)")
    print(f"  2️⃣  COM RAG:          {duration_rag:.2f}s ({duration_rag/60:.2f} min)")
    print(f"  3️⃣  COM RAG + DSPy:   {duration_dspy:.2f}s ({duration_dspy/60:.2f} min)")
    print()

    diff_rag_vs_no_rag_d, symbol1_d = calculate_percentage_diff(duration_rag, duration_no_rag)
    diff_dspy_vs_rag_d, symbol2_d = calculate_percentage_diff(duration_dspy, duration_rag)
    diff_dspy_vs_no_rag_d, symbol3_d = calculate_percentage_diff(duration_dspy, duration_no_rag)

    print("Comparações:")
    print(f"  RAG vs SEM RAG:        {symbol1_d} {diff_rag_vs_no_rag_d:.2f}%")
    print(f"  DSPy vs RAG:           {symbol2_d} {diff_dspy_vs_rag_d:.2f}%")
    print(f"  DSPy vs SEM RAG:       {symbol3_d} {diff_dspy_vs_no_rag_d:.2f}%")
    print()

    # === COMPARAÇÃO DE LLM CALLS ===
    print("=" * 100)
    print("📞 COMPARAÇÃO DE LLM CALLS")
    print("=" * 100)
    print()

    calls_no_rag = stats_no_rag.get('total_llm_calls', 0)
    calls_rag = stats_rag.get('total_llm_calls', 0)
    calls_dspy = stats_dspy.get('total_llm_calls', 0)

    print("LLM Calls Totais:")
    print(f"  1️⃣  SEM RAG:          {calls_no_rag}")
    print(f"  2️⃣  COM RAG:          {calls_rag}")
    print(f"  3️⃣  COM RAG + DSPy:   {calls_dspy}")
    print()

    # === RESUMO EXECUTIVO ===
    print("=" * 100)
    print("📈 RESUMO EXECUTIVO - ANÁLISE COMPARATIVA")
    print("=" * 100)
    print()

    print("🎯 IMPACTO DO RAG (vs SEM RAG):")
    print(f"  💰 Custo: {symbol1} {diff_rag_vs_no_rag:.2f}%")
    print(f"  🎫 Tokens: {symbol1_t} {diff_rag_vs_no_rag_t:.2f}%")
    print(f"  ⏱️  Performance: {symbol1_d} {diff_rag_vs_no_rag_d:.2f}%")
    print()

    print("🔧 IMPACTO DO DSPy (vs RAG básico):")
    print(f"  💰 Custo: {symbol2} {diff_dspy_vs_rag:.2f}%")
    print(f"  🎫 Tokens: {symbol2_t} {diff_dspy_vs_rag_t:.2f}%")
    print(f"  ⏱️  Performance: {symbol2_d} {diff_dspy_vs_rag_d:.2f}%")
    print()

    print("🚀 IMPACTO TOTAL DO DSPy (vs SEM RAG):")
    print(f"  💰 Custo: {symbol3} {diff_dspy_vs_no_rag:.2f}%")
    print(f"  🎫 Tokens: {symbol3_t} {diff_dspy_vs_no_rag_t:.2f}%")
    print(f"  ⏱️  Performance: {symbol3_d} {diff_dspy_vs_no_rag_d:.2f}%")
    print()

    # Melhor baseline
    print("🏆 RECOMENDAÇÃO:")
    print()

    # Determinar melhor opção por custo
    costs = {"SEM RAG": cost_no_rag, "COM RAG": cost_rag, "COM RAG + DSPy": cost_dspy}
    best_cost = min(costs, key=costs.get)

    # Determinar melhor opção por performance
    perfs = {"SEM RAG": duration_no_rag, "COM RAG": duration_rag, "COM RAG + DSPy": duration_dspy}
    best_perf = min(perfs, key=perfs.get)

    print(f"  🥇 Menor custo: {best_cost} (${costs[best_cost]:.4f})")
    print(f"  🥇 Melhor performance: {best_perf} ({perfs[best_perf]:.2f}s)")
    print()

    if best_cost == "COM RAG + DSPy" and best_perf == "COM RAG + DSPy":
        print("  ✅ VENCEDOR: COM RAG + DSPy (melhor em custo E performance!)")
    elif best_cost == "COM RAG + DSPy":
        print("  ✅ VENCEDOR: COM RAG + DSPy (melhor custo, performance aceitável)")
    elif best_perf == "COM RAG + DSPy":
        print("  ✅ VENCEDOR: COM RAG + DSPy (melhor performance, custo aceitável)")
    else:
        print("  ⚖️  DEPENDE: Analise trade-off entre custo e performance para seu caso")

    print()

    # Salvar relatório de comparação
    comparison_report = {
        "timestamp": datetime.now().isoformat(),
        "baselines": {
            "no_rag": {
                "report_path": "metrics/data/no_rag/baseline_report.json",
                "date": report_no_rag.get('timestamp'),
                "stats": stats_no_rag,
            },
            "with_rag": {
                "report_path": "metrics/data/baseline_report.json",
                "date": report_rag.get('timestamp'),
                "stats": stats_rag,
            },
            "with_rag_dspy": {
                "report_path": "metrics/data/dspy/baseline_report.json",
                "date": report_dspy.get('timestamp'),
                "stats": stats_dspy,
            },
        },
        "comparison": {
            "cost": {
                "no_rag": cost_no_rag,
                "with_rag": cost_rag,
                "with_rag_dspy": cost_dspy,
                "best": best_cost,
            },
            "performance": {
                "no_rag": duration_no_rag,
                "with_rag": duration_rag,
                "with_rag_dspy": duration_dspy,
                "best": best_perf,
            },
            "tokens": {
                "no_rag": tokens_no_rag,
                "with_rag": tokens_rag,
                "with_rag_dspy": tokens_dspy,
            },
        },
    }

    comparison_path = Path("metrics/data/comparison_all_baselines.json")
    comparison_path.write_text(json.dumps(comparison_report, indent=2))

    print(f"💾 Relatório de comparação completa salvo em: {comparison_path}")
    print()


def main():
    """Main function."""
    print()
    print("🔍 Buscando relatórios dos 3 baselines...")
    print()

    # Caminhos dos relatórios
    report_no_rag_path = Path("metrics/data/no_rag/baseline_report.json")
    report_rag_path = Path("metrics/data/baseline_report.json")
    report_dspy_path = Path("metrics/data/dspy/baseline_report.json")

    # Carregar relatórios
    report_no_rag = load_report(report_no_rag_path)
    report_rag = load_report(report_rag_path)
    report_dspy = load_report(report_dspy_path)

    # Verificar se todos existem
    missing = []
    if not report_no_rag:
        missing.append(("SEM RAG", report_no_rag_path, "./scripts/run_baseline_no_rag.sh"))
    if not report_rag:
        missing.append(("COM RAG", report_rag_path, "./scripts/run_baseline_test.sh"))
    if not report_dspy:
        missing.append(("COM RAG + DSPy", report_dspy_path, "./scripts/run_baseline_dspy.sh"))

    if missing:
        print("❌ Relatórios faltando:")
        print()
        for name, path, script in missing:
            print(f"  {name}:")
            print(f"    Caminho: {path}")
            print(f"    Execute: {script}")
            print()
        return 1

    print(f"✅ Todos os 3 relatórios encontrados!")
    print()

    # Comparar
    compare_three_baselines(report_no_rag, report_rag, report_dspy)

    print("=" * 100)
    print("✅ ANÁLISE COMPARATIVA COMPLETA")
    print("=" * 100)
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
