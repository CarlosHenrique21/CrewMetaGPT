#!/usr/bin/env python3
"""
Wrapper para treinar DSPy com ambiente limpo.
Força reload das variáveis de ambiente do .env
"""
import os
import sys
from pathlib import Path

# Limpar API key do ambiente antes de carregar
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

# Forçar reload do .env
from dotenv import load_dotenv
load_dotenv(override=True)  # override=True força recarregar

# Verificar API key
api_key = os.getenv("OPENAI_API_KEY", "")
print(f"✅ API Key carregada: {len(api_key)} chars, começa com: {api_key[:20]}...")

# Agora executar o treinamento
sys.path.insert(0, str(Path(__file__).parent))

from dspy_optimizer import optimize_pipeline, evaluate_pipeline, save_evaluation_results, create_training_examples

def main():
    print()
    print("=" * 80)
    print("🔧 DSPy PIPELINE TRAINING & OPTIMIZATION (Clean Environment)")
    print("=" * 80)
    print()

    # Optimize pipeline
    print("Iniciando otimização do pipeline...")
    print()

    optimized_pipeline = optimize_pipeline(
        optimizer_type="bootstrap",
        max_demos=4,
        use_baseline_examples=True,
    )

    print()
    print("=" * 80)
    print("✅ OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print()

    # Evaluate on test set
    print("Avaliando pipeline otimizado...")
    print()

    test_examples = create_training_examples()[:3]
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
