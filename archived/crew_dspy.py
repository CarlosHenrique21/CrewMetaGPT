# crew_dspy.py
"""
DSPy-based Software Development Pipeline.
Optimizable end-to-end pipeline using DSPy modules.
"""
import dspy
from pathlib import Path
from typing import Dict, Any
from agents_dspy import (
    ProductManagerModule,
    ArchitectModule,
    EngineerModule,
    QAEngineerModule,
    TechWriterModule,
)
from tools import (
    file_writer_tool,
    directory_creator_tool,
)
import config


class SoftwareDevPipeline(dspy.Module):
    """
    Complete software development pipeline as a DSPy Module.
    Orchestrates all agents sequentially with optimizable prompts.
    """

    def __init__(self):
        super().__init__()

        # Initialize all agent modules
        self.product_manager = ProductManagerModule()
        self.architect = ArchitectModule()
        self.engineer = EngineerModule()
        self.qa_engineer = QAEngineerModule()
        self.tech_writer = TechWriterModule()

    def forward(self, project_idea: str):
        """
        Execute complete software development pipeline.

        Args:
            project_idea: The software project description

        Returns:
            dspy.Prediction with all outputs
        """
        print("=" * 80)
        print(f"🚀 Starting DSPy Software Development Pipeline")
        print(f"📋 Project: {project_idea}")
        print("=" * 80)
        print()

        # Step 1: Product Manager creates PRD
        print("📋 Step 1/5: Creating PRD...")
        prd_result = self.product_manager(project_idea=project_idea)
        prd_content = prd_result.prd_content
        print(f"   ✅ PRD created ({len(prd_content)} chars)")

        # Step 2: Architect designs system
        print("🏗️  Step 2/5: Designing architecture...")
        arch_result = self.architect(prd=prd_content)
        arch_content = arch_result.architecture_content
        print(f"   ✅ Architecture designed ({len(arch_content)} chars)")

        # Step 3: Engineer implements code
        print("💻 Step 3/5: Implementing code...")
        impl_result = self.engineer(prd=prd_content, architecture=arch_content)
        impl_plan = impl_result.implementation_plan
        print(f"   ✅ Implementation plan created ({len(impl_plan)} chars)")

        # Step 4: QA creates tests
        print("🧪 Step 4/5: Creating tests...")
        test_result = self.qa_engineer(implementation_summary=impl_plan)
        test_plan = test_result.test_plan
        print(f"   ✅ Test plan created ({len(test_plan)} chars)")

        # Step 5: Tech Writer creates docs
        print("📚 Step 5/5: Creating documentation...")
        project_summary = f"""
Project Idea: {project_idea}

PRD Summary:
{prd_content[:500]}...

Architecture Summary:
{arch_content[:500]}...

Implementation Summary:
{impl_plan[:500]}...
"""
        docs_result = self.tech_writer(project_summary=project_summary)
        documentation = docs_result.documentation
        print(f"   ✅ Documentation created ({len(documentation)} chars)")

        print()
        print("=" * 80)
        print("✅ DSPy Pipeline Completed!")
        print("=" * 80)
        print()

        # Return as dspy.Prediction (required for DSPy optimization)
        return dspy.Prediction(
            prd=prd_content,
            architecture=arch_content,
            implementation=impl_plan,
            tests=test_plan,
            documentation=documentation,
        )


def run_software_dev_crew_dspy(
    project_idea: str,
    save_outputs: bool = True,
    compiled_pipeline: SoftwareDevPipeline = None
):
    """
    Run the DSPy software development pipeline.

    Args:
        project_idea: Description of the software to build
        save_outputs: Whether to save outputs to workspace
        compiled_pipeline: Pre-compiled/optimized pipeline (if available)

    Returns:
        dspy.Prediction with all outputs
    """
    from dspy_config import configure_dspy

    # Configure DSPy if not already configured
    if dspy.settings.lm is None:
        configure_dspy()

    # Use compiled pipeline if provided, otherwise create new one
    pipeline = compiled_pipeline if compiled_pipeline else SoftwareDevPipeline()

    # Run pipeline
    result = pipeline(project_idea=project_idea)

    # Save outputs to workspace if requested
    if save_outputs:
        save_pipeline_outputs(result, project_idea)

    return result


def save_pipeline_outputs(result, project_idea: str) -> None:
    """
    Save pipeline outputs to workspace directory.

    Args:
        result: Pipeline result (dspy.Prediction)
        project_idea: The project idea (for context)
    """
    workspace = Path(config.WORKSPACE_DIR)

    print(f"💾 Saving outputs to {workspace}...")

    # Create workspace directory
    directory_creator_tool._run(str(workspace))

    # Save each output (accessing dspy.Prediction attributes)
    outputs = {
        "prd.md": result.prd,
        "architecture.md": result.architecture,
        "implementation_plan.md": result.implementation,
        "test_plan.md": result.tests,
        "README.md": result.documentation,
    }

    for filename, content in outputs.items():
        # file_writer_tool expects file_path (relative) and content
        file_writer_tool._run(
            file_path=filename,  # Use relative path, tool adds workspace dir
            content=content
        )
        print(f"   ✅ Saved: {filename}")

    print(f"\n📁 All outputs saved to: {workspace}")


def load_optimized_pipeline(name: str = "software_dev_pipeline") -> SoftwareDevPipeline:
    """
    Load a previously optimized pipeline.

    Args:
        name: Name of the saved pipeline

    Returns:
        Optimized pipeline or new pipeline if not found
    """
    from dspy_config import load_compiled_program

    pipeline = load_compiled_program(SoftwareDevPipeline, name)

    if pipeline is None:
        print("⚠️  No optimized pipeline found, using default")
        pipeline = SoftwareDevPipeline()

    return pipeline


if __name__ == "__main__":
    # Test pipeline
    from dspy_config import configure_dspy

    print("Testing DSPy Software Development Pipeline...")
    configure_dspy()

    # Test with simple project
    test_idea = "crie uma calculadora CLI simples com operações básicas"

    result = run_software_dev_crew_dspy(
        project_idea=test_idea,
        save_outputs=False  # Don't save for test
    )

    print("\n📊 Pipeline Results:")
    print(f"   prd: {len(result.prd)} chars")
    print(f"   architecture: {len(result.architecture)} chars")
    print(f"   implementation: {len(result.implementation)} chars")
    print(f"   tests: {len(result.tests)} chars")
    print(f"   documentation: {len(result.documentation)} chars")

    print("\n✅ DSPy pipeline test successful!")
