#!/usr/bin/env python3
"""
Script para treinar e otimizar o pipeline DSPy.
Deve ser executado ANTES do baseline DSPy para melhores resultados.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dspy_optimizer import optimize_pipeline, evaluate_pipeline, save_evaluation_results, create_training_examples


def main():
    print()
    print("=" * 80)
    print("🔧 DSPy PIPELINE TRAINING & OPTIMIZATION")
    print("=" * 80)
    print()
    print("Este script treina e otimiza o pipeline DSPy usando exemplos.")
    print("Execute isto ANTES de rodar o baseline DSPy para melhores resultados.")
    print()

    # Ask for confirmation (skip if --yes flag is provided)
    if "--yes" not in sys.argv and "-y" not in sys.argv:
        response = input("Deseja continuar? (y/n): ")
        if response.lower() != 'y':
            print("Operação cancelada.")
            return 0

    print()

    # Optimize pipeline
    print("Iniciando otimização do pipeline...")
    print()

    optimized_pipeline = optimize_pipeline(
        optimizer_type="bootstrap",
        max_demos=4,
        use_baseline_examples=True,  # Use baseline data if available
    )

    print()
    print("=" * 80)
    print("✅ OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print()

    # Evaluate on test set
    print("Avaliando pipeline otimizado...")
    print()

    test_examples = create_training_examples()[:3]  # Use 3 examples for evaluation
    eval_results = evaluate_pipeline(optimized_pipeline, test_examples)

    # Save evaluation results
    save_evaluation_results(eval_results)

    print()
    print("=" * 80)
    print("🎉 TREINAMENTO E AVALIAÇÃO COMPLETOS!")
    print("=" * 80)
    print()
    print("Pipeline otimizado foi salvo e está pronto para uso.")
    print("Execute agora: ./scripts/run_baseline_dspy.sh")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
