#!/usr/bin/env python3
"""
Pipeline DSPy com otimização MANUAL (few-shot).
Faz LLM calls reais com prompts otimizados manualmente.
"""
import dspy
from pathlib import Path
from typing import Dict, Any
from agents_dspy_manual import (
    ProductManagerModuleManual,
    ArchitectModuleManual,
    EngineerModuleManual,
    QAEngineerModuleManual,
    TechWriterModuleManual,
)
from tools import (
    file_writer_tool,
    directory_creator_tool,
)
import config


class SoftwareDevPipelineManual(dspy.Module):
    """
    Pipeline DSPy com otimização MANUAL.
    Usa few-shot examples manuais em vez de optimizer automático.
    FAZ LLM CALLS REAIS!
    """

    def __init__(self):
        super().__init__()

        # Initialize all agent modules (com otimização manual)
        self.product_manager = ProductManagerModuleManual()
        self.architect = ArchitectModuleManual()
        self.engineer = EngineerModuleManual()
        self.qa_engineer = QAEngineerModuleManual()
        self.tech_writer = TechWriterModuleManual()

    def forward(self, project_idea: str):
        """
        Execute complete software development pipeline.
        COM LLM calls reais e otimização manual!

        Args:
            project_idea: The software project description

        Returns:
            dspy.Prediction with all outputs
        """
        print("=" * 80)
        print(f"🚀 Starting DSPy Pipeline (MANUAL OPTIMIZATION)")
        print(f"📋 Project: {project_idea}")
        print(f"💡 Fazendo LLM calls REAIS com few-shot examples!")
        print("=" * 80)
        print()

        # Step 1: Product Manager creates PRD (com few-shot)
        print("📋 Step 1/5: Creating PRD (with few-shot examples)...")
        prd_result = self.product_manager(project_idea=project_idea)
        prd_content = prd_result.prd_content
        print(f"   ✅ PRD created ({len(prd_content)} chars)")

        # Step 2: Architect designs system (com few-shot)
        print("🏗️  Step 2/5: Designing architecture (with few-shot examples)...")
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
        print("✅ DSPy Pipeline (MANUAL) Completed!")
        print("=" * 80)
        print()

        # Return as dspy.Prediction
        return dspy.Prediction(
            prd=prd_content,
            architecture=arch_content,
            implementation=impl_plan,
            tests=test_plan,
            documentation=documentation,
        )


def run_software_dev_crew_dspy_manual(
    project_idea: str,
    save_outputs: bool = True,
):
    """
    Run DSPy pipeline with MANUAL optimization.
    Faz LLM calls REAIS!

    Args:
        project_idea: Description of the software to build
        save_outputs: Whether to save outputs to workspace

    Returns:
        dspy.Prediction with all outputs
    """
    from dspy_config import configure_dspy

    # Configure DSPy if not already configured
    if dspy.settings.lm is None:
        configure_dspy()

    # Create fresh pipeline (sem otimização automática)
    pipeline = SoftwareDevPipelineManual()

    # Run pipeline (FAZ LLM CALLS REAIS!)
    result = pipeline(project_idea=project_idea)

    # Save outputs to workspace if requested
    if save_outputs:
        save_pipeline_outputs_manual(result, project_idea)

    return result


def save_pipeline_outputs_manual(result, project_idea: str) -> None:
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

    # Save each output
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
            file_path=filename,
            content=content
        )
        print(f"   ✅ Saved: {filename}")

    print(f"\n📁 All outputs saved to: {workspace}")


if __name__ == "__main__":
    # Test pipeline
    from dspy_config import configure_dspy

    print("Testing DSPy Pipeline with MANUAL Optimization...")
    configure_dspy()

    # Test with simple project
    test_idea = "crie uma calculadora CLI simples com operações básicas"

    result = run_software_dev_crew_dspy_manual(
        project_idea=test_idea,
        save_outputs=False  # Don't save for test
    )

    print("\n📊 Pipeline Results:")
    print(f"   prd: {len(result.prd)} chars")
    print(f"   architecture: {len(result.architecture)} chars")
    print(f"   implementation: {len(result.implementation)} chars")
    print(f"   tests: {len(result.tests)} chars")
    print(f"   documentation: {len(result.documentation)} chars")

    print("\n✅ DSPy pipeline with MANUAL optimization test successful!")
    print("💡 This made REAL LLM calls with few-shot examples!")
