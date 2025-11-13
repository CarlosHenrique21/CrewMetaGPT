# dspy_optimizer.py
"""
DSPy Pipeline Optimization System.
Trains and optimizes the software development pipeline using examples.
"""
import dspy
from typing import List, Dict, Any, Callable
from pathlib import Path
import json
from crew_dspy import SoftwareDevPipeline
from dspy_config import (
    configure_dspy,
    get_optimizer,
    save_compiled_program,
    get_dspy_cache_dir,
)


# ============================================================================
# Training Examples
# ============================================================================

def create_training_examples() -> List[dspy.Example]:
    """
    Create training examples from baseline results or manual examples.

    Returns:
        List of DSPy Examples for training
    """
    examples = []

    # Example 1: Todo List CLI
    examples.append(
        dspy.Example(
            project_idea="crie uma aplicação CLI para gerenciar lista de tarefas com comandos add, list, done e delete",
            expected_quality="high",  # Quality metric
        ).with_inputs("project_idea")
    )

    # Example 2: URL Shortener API
    examples.append(
        dspy.Example(
            project_idea="crie uma API REST para encurtar URLs com endpoints para criar, listar e redirecionar",
            expected_quality="high",
        ).with_inputs("project_idea")
    )

    # Example 3: Weather CLI
    examples.append(
        dspy.Example(
            project_idea="crie uma ferramenta CLI que consulta API de clima e mostra previsão formatada",
            expected_quality="high",
        ).with_inputs("project_idea")
    )

    # Example 4: Password Generator
    examples.append(
        dspy.Example(
            project_idea="crie um gerador de senhas seguras CLI com opções de tamanho, caracteres especiais e força",
            expected_quality="high",
        ).with_inputs("project_idea")
    )

    # Example 5: Markdown Converter
    examples.append(
        dspy.Example(
            project_idea="crie um conversor de Markdown para HTML com suporte a títulos, listas e links",
            expected_quality="high",
        ).with_inputs("project_idea")
    )

    print(f"✅ Created {len(examples)} training examples")
    return examples


def load_baseline_examples() -> List[dspy.Example]:
    """
    Load examples from previous baseline results.

    Returns:
        List of DSPy Examples from baseline data
    """
    examples = []

    # Try to load from baseline data
    baseline_dir = Path("metrics/data")

    if not baseline_dir.exists():
        print("⚠️  No baseline data found, using default examples")
        return create_training_examples()

    # Load successful projects from baseline
    for project_file in baseline_dir.glob("baseline_project_*.json"):
        try:
            data = json.loads(project_file.read_text())

            if data.get("status") == "success":
                example = dspy.Example(
                    project_idea=data["description"],
                    expected_quality="high",
                ).with_inputs("project_idea")

                examples.append(example)
        except Exception as e:
            print(f"⚠️  Error loading {project_file}: {e}")

    if examples:
        print(f"✅ Loaded {len(examples)} examples from baseline data")
    else:
        print("⚠️  No baseline examples found, using default")
        examples = create_training_examples()

    return examples


# ============================================================================
# Metrics
# ============================================================================

def quality_metric(example: dspy.Example, prediction, trace=None) -> float:
    """
    Metric to evaluate pipeline quality.

    Args:
        example: Input example
        prediction: Pipeline prediction (dspy.Prediction object)
        trace: Execution trace (optional)

    Returns:
        Quality score (0.0 to 1.0)
    """
    score = 0.0

    # Check if all required outputs are present
    required_keys = ["prd", "architecture", "implementation", "tests", "documentation"]

    for key in required_keys:
        # Access dspy.Prediction attributes using hasattr and getattr
        if hasattr(prediction, key):
            value = getattr(prediction, key, None)
            if value:
                score += 0.2  # Each output adds 20%

    # Bonus: Check if outputs are substantial (> 100 chars each)
    for key in required_keys:
        if hasattr(prediction, key):
            value = getattr(prediction, key, None)
            if value and len(str(value)) > 100:
                score += 0.05  # Extra 5% for substantial output

    # Cap at 1.0
    return min(score, 1.0)


def completeness_metric(example: dspy.Example, prediction, trace=None) -> bool:
    """
    Binary metric: are all outputs present and non-empty?

    Args:
        example: Input example
        prediction: Pipeline prediction (dspy.Prediction object)
        trace: Execution trace (optional)

    Returns:
        True if all outputs present and non-empty
    """
    required_keys = ["prd", "architecture", "implementation", "tests", "documentation"]

    for key in required_keys:
        # Access dspy.Prediction attributes using hasattr and getattr
        if not hasattr(prediction, key):
            return False
        value = getattr(prediction, key, None)
        if not value or len(str(value)) < 50:
            return False

    return True


# ============================================================================
# Optimization Functions
# ============================================================================

def optimize_pipeline(
    optimizer_type: str = "bootstrap",
    max_demos: int = 4,
    use_baseline_examples: bool = True,
) -> SoftwareDevPipeline:
    """
    Optimize the software development pipeline using DSPy.

    Args:
        optimizer_type: Type of optimizer (bootstrap, mipro, copro)
        max_demos: Maximum number of demonstrations
        use_baseline_examples: Use examples from baseline results

    Returns:
        Optimized pipeline
    """
    print()
    print("=" * 80)
    print("🔧 DSPy PIPELINE OPTIMIZATION")
    print("=" * 80)
    print()

    # Configure DSPy
    print("⚙️  Configuring DSPy...")
    configure_dspy()

    # Load training examples
    print("📚 Loading training examples...")
    if use_baseline_examples:
        trainset = load_baseline_examples()
    else:
        trainset = create_training_examples()

    print(f"   Training examples: {len(trainset)}")
    print()

    # Create pipeline
    print("🏗️  Creating pipeline...")
    pipeline = SoftwareDevPipeline()

    # Get optimizer
    print(f"🎯 Initializing {optimizer_type} optimizer...")
    if optimizer_type == "bootstrap":
        optimizer = dspy.BootstrapFewShot(
            metric=quality_metric,
            max_bootstrapped_demos=max_demos,
            max_labeled_demos=max_demos,
        )
    else:
        optimizer = get_optimizer(optimizer_type)

    print()
    print("🚀 Starting optimization...")
    print("   This may take several minutes...")
    print()

    # Compile/optimize pipeline
    try:
        optimized_pipeline = optimizer.compile(
            pipeline,
            trainset=trainset,
        )

        print()
        print("=" * 80)
        print("✅ OPTIMIZATION COMPLETE!")
        print("=" * 80)
        print()

        # Save optimized pipeline
        try:
            save_path = save_compiled_program(optimized_pipeline, "software_dev_pipeline")
            print(f"   Saved to: {save_path}")
        except Exception as save_error:
            print(f"⚠️  Warning: Could not save optimized pipeline: {save_error}")
            print("   Pipeline will still work, but won't be persisted.")

        return optimized_pipeline

    except ModuleNotFoundError as e:
        if '_lzma' in str(e):
            print()
            print("=" * 80)
            print("⚠️  WARNING: lzma module not available")
            print("=" * 80)
            print()
            print("Optimization requires lzma module.")
            print("Using non-optimized pipeline (will still work fine).")
            print()
            print("To enable optimization, install lzma:")
            print("  brew install xz")
            print("  pyenv uninstall 3.11.12 && pyenv install 3.11.12")
            print("  pip install -r requirements.txt")
            print()
            return pipeline
        else:
            raise
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ OPTIMIZATION FAILED: {e}")
        print("=" * 80)
        print()
        import traceback
        traceback.print_exc()
        print()
        print("Returning un-optimized pipeline...")
        return pipeline


def evaluate_pipeline(
    pipeline: SoftwareDevPipeline,
    test_examples: List[dspy.Example],
    metric: Callable = quality_metric,
) -> Dict[str, Any]:
    """
    Evaluate pipeline on test examples.

    Args:
        pipeline: Pipeline to evaluate
        test_examples: Test examples
        metric: Metric function

    Returns:
        Evaluation results
    """
    print()
    print("=" * 80)
    print("📊 EVALUATING PIPELINE")
    print("=" * 80)
    print()

    scores = []
    results = []

    for i, example in enumerate(test_examples, 1):
        print(f"Evaluating example {i}/{len(test_examples)}...")

        try:
            # Run pipeline
            prediction = pipeline(project_idea=example.project_idea)

            # Calculate score
            score = metric(example, prediction)
            scores.append(score)

            results.append({
                "example_id": i,
                "project_idea": example.project_idea,
                "score": score,
                "success": score > 0.5,
            })

            print(f"   Score: {score:.2f}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            scores.append(0.0)
            results.append({
                "example_id": i,
                "project_idea": example.project_idea,
                "score": 0.0,
                "success": False,
                "error": str(e),
            })

    # Calculate statistics
    avg_score = sum(scores) / len(scores) if scores else 0.0
    success_rate = sum(1 for s in scores if s > 0.5) / len(scores) if scores else 0.0

    print()
    print("=" * 80)
    print("📊 EVALUATION RESULTS")
    print("=" * 80)
    print(f"   Average Score: {avg_score:.2f}")
    print(f"   Success Rate: {success_rate:.1%}")
    print(f"   Total Examples: {len(test_examples)}")
    print()

    return {
        "average_score": avg_score,
        "success_rate": success_rate,
        "total_examples": len(test_examples),
        "results": results,
    }


def save_evaluation_results(results: Dict[str, Any], filename: str = "dspy_evaluation.json"):
    """
    Save evaluation results to file.

    Args:
        results: Evaluation results dictionary
        filename: Output filename
    """
    cache_dir = get_dspy_cache_dir()
    filepath = cache_dir / filename

    filepath.write_text(json.dumps(results, indent=2))
    print(f"💾 Evaluation results saved: {filepath}")


if __name__ == "__main__":
    # Test optimization
    print("Testing DSPy optimization system...")

    # Optimize pipeline
    optimized = optimize_pipeline(
        optimizer_type="bootstrap",
        max_demos=2,  # Small for testing
        use_baseline_examples=False,
    )

    # Evaluate
    test_examples = create_training_examples()[:2]  # Use first 2 for testing
    results = evaluate_pipeline(optimized, test_examples)

    # Save results
    save_evaluation_results(results)

    print("\n✅ Optimization test complete!")
