#!/usr/bin/env python3
"""
Agentes DSPy com otimização MANUAL (few-shot examples).
Faz LLM calls reais MAS com prompts otimizados manualmente.
"""
import dspy
from typing import List, Optional


# ============================================================================
# Signatures (mesmas de antes)
# ============================================================================

class CreatePRDSignature(dspy.Signature):
    """Create a comprehensive Product Requirements Document from a project idea."""
    project_idea = dspy.InputField(desc="The software project idea to develop")
    context = dspy.InputField(desc="Relevant examples and best practices from knowledge base", default="")

    prd_content = dspy.OutputField(desc="Complete PRD in markdown format with: project overview, functional requirements, non-functional requirements, success metrics, constraints")


class DesignArchitectureSignature(dspy.Signature):
    """Design robust, scalable software architecture based on requirements."""
    prd = dspy.InputField(desc="Product Requirements Document")
    context = dspy.InputField(desc="Architecture patterns and best practices from knowledge base", default="")

    architecture_content = dspy.OutputField(desc="Detailed architecture document in markdown with: system overview, technology stack, component design, data models, file structure")


class ImplementCodeSignature(dspy.Signature):
    """Implement high-quality, well-tested code based on architecture and requirements."""
    prd = dspy.InputField(desc="Product Requirements Document")
    architecture = dspy.InputField(desc="System architecture document")
    context = dspy.InputField(desc="Code examples and patterns from knowledge base", default="")

    implementation_plan = dspy.OutputField(desc="Implementation plan with file structure and main code components to be created")


class CreateTestsSignature(dspy.Signature):
    """Create comprehensive testing strategy and test cases."""
    implementation_summary = dspy.InputField(desc="Summary of the implementation")

    test_plan = dspy.OutputField(desc="Test plan and test cases in markdown format")


class CreateDocsSignature(dspy.Signature):
    """Create comprehensive project documentation."""
    project_summary = dspy.InputField(desc="Summary of the entire project including PRD, architecture, and implementation")

    documentation = dspy.OutputField(desc="Complete documentation including README and user guide in markdown")


# ============================================================================
# Few-Shot Examples Manuais
# ============================================================================

# Exemplos para guiar o modelo (few-shot learning)
PRD_EXAMPLES = [
    dspy.Example(
        project_idea="Build a CLI todo list manager",
        context="",
        prd_content="""# Product Requirements Document: CLI Todo List Manager

## 1. Project Overview
A command-line interface application for managing personal tasks with simple CRUD operations.

## 2. Functional Requirements
- FR-1: Add new tasks with title and optional description
- FR-2: List all tasks with status indicators
- FR-3: Mark tasks as completed
- FR-4: Delete tasks by ID
- FR-5: Persist tasks to local file storage

## 3. Non-Functional Requirements
- NFR-1: Startup time < 100ms
- NFR-2: Support up to 10,000 tasks
- NFR-3: Cross-platform (Linux, macOS, Windows)

## 4. Success Metrics
- User can complete basic workflow in < 30 seconds
- Zero data loss on normal operation

## 5. Constraints
- Single-user application
- No network dependencies
- CLI only (no GUI)
"""
    ).with_inputs("project_idea", "context")
]

ARCHITECTURE_EXAMPLES = [
    dspy.Example(
        prd="# PRD for CLI Todo App\n\nCommand-line task manager with add, list, done, delete commands.",
        context="",
        architecture_content="""# Software Architecture: CLI Todo List Manager

## 1. System Overview
Modular CLI application using clean architecture principles.

## 2. Technology Stack
- Language: Python 3.11+
- Storage: JSON file (tasks.json)
- CLI Framework: argparse / click
- Testing: pytest

## 3. Component Design

### 3.1 CLI Layer
- `cli.py`: Command parser and user interface
- Commands: add, list, done, delete

### 3.2 Business Logic Layer
- `task_manager.py`: Core task operations
- `models.py`: Task data model

### 3.3 Data Layer
- `storage.py`: JSON file read/write operations

## 4. Data Models
```python
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

## 5. File Structure
```
todo_cli/
├── cli.py
├── task_manager.py
├── models.py
├── storage.py
├── tests/
│   ├── test_task_manager.py
│   └── test_storage.py
└── tasks.json
```
"""
    ).with_inputs("prd", "context")
]


# ============================================================================
# Módulos com Few-Shot Manual
# ============================================================================

class ProductManagerModuleManual(dspy.Module):
    """PM com few-shot examples manuais."""

    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)

        # ChainOfThought COM demonstrações manuais
        self.generate_prd = dspy.ChainOfThought(
            CreatePRDSignature,
            # Adiciona examples manualmente para few-shot
        )

    def forward(self, project_idea: str):
        try:
            # Retrieve context
            context_query = f"PRD templates and best practices for: {project_idea}"
            retrieval_result = self.retrieve(context_query)

            if isinstance(retrieval_result, list):
                context_docs = [psg.long_text for psg in retrieval_result if hasattr(psg, 'long_text')]
            else:
                context_docs = []
            context = "\n\n".join(context_docs) if context_docs else ""

            # Gerar PRD COM few-shot examples
            # Adiciona exemplos no contexto do prompt
            result = self.generate_prd(
                project_idea=project_idea,
                context=context,
                demos=PRD_EXAMPLES[:1]  # Usa 1 exemplo como demonstração
            )

            return result
        except Exception as e:
            print(f"❌ Error in ProductManager: {e}")
            import traceback
            traceback.print_exc()
            return dspy.Prediction(prd_content=f"Error generating PRD: {e}")


class ArchitectModuleManual(dspy.Module):
    """Architect com few-shot examples manuais."""

    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.design = dspy.ChainOfThought(DesignArchitectureSignature)

    def forward(self, prd: str):
        try:
            # Retrieve context
            context_query = f"Software architecture patterns for: {prd[:200]}"
            retrieval_result = self.retrieve(context_query)

            if isinstance(retrieval_result, list):
                context_docs = [psg.long_text for psg in retrieval_result if hasattr(psg, 'long_text')]
            else:
                context_docs = []
            context = "\n\n".join(context_docs) if context_docs else ""

            # Design COM few-shot examples
            result = self.design(
                prd=prd,
                context=context,
                demos=ARCHITECTURE_EXAMPLES[:1]  # Usa 1 exemplo
            )

            return result
        except Exception as e:
            print(f"❌ Error in Architect: {e}")
            import traceback
            traceback.print_exc()
            return dspy.Prediction(architecture_content=f"Error designing architecture: {e}")


class EngineerModuleManual(dspy.Module):
    """Engineer sem examples (deixa o RAG guiar)."""

    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.implement = dspy.ChainOfThought(ImplementCodeSignature)

    def forward(self, prd: str, architecture: str) -> dspy.Prediction:
        try:
            context_query = f"Code examples and patterns for: {architecture[:200]}"
            retrieval_result = self.retrieve(context_query)

            if isinstance(retrieval_result, list):
                context_docs = [psg.long_text for psg in retrieval_result if hasattr(psg, 'long_text')]
            else:
                context_docs = []
            context = "\n\n".join(context_docs) if context_docs else ""

            result = self.implement(
                prd=prd,
                architecture=architecture,
                context=context
            )

            return result
        except Exception as e:
            print(f"❌ Error in Engineer: {e}")
            import traceback
            traceback.print_exc()
            return dspy.Prediction(implementation_plan=f"Error generating implementation: {e}")


class QAEngineerModuleManual(dspy.Module):
    """QA sem examples."""

    def __init__(self):
        super().__init__()
        self.create_tests = dspy.ChainOfThought(CreateTestsSignature)

    def forward(self, implementation_summary: str) -> dspy.Prediction:
        try:
            result = self.create_tests(
                implementation_summary=implementation_summary
            )
            return result
        except Exception as e:
            print(f"❌ Error in QA Engineer: {e}")
            import traceback
            traceback.print_exc()
            return dspy.Prediction(test_plan=f"Error generating test plan: {e}")


class TechWriterModuleManual(dspy.Module):
    """Tech Writer sem examples."""

    def __init__(self):
        super().__init__()
        self.write_docs = dspy.ChainOfThought(CreateDocsSignature)

    def forward(self, project_summary: str) -> dspy.Prediction:
        try:
            result = self.write_docs(
                project_summary=project_summary
            )
            return result
        except Exception as e:
            print(f"❌ Error in Tech Writer: {e}")
            import traceback
            traceback.print_exc()
            return dspy.Prediction(documentation=f"Error generating documentation: {e}")


# ============================================================================
# Helper Functions
# ============================================================================

def create_product_manager_manual() -> ProductManagerModuleManual:
    """Create DSPy Product Manager module with manual optimization."""
    return ProductManagerModuleManual()


def create_architect_manual() -> ArchitectModuleManual:
    """Create DSPy Architect module with manual optimization."""
    return ArchitectModuleManual()


def create_engineer_manual() -> EngineerModuleManual:
    """Create DSPy Engineer module with manual optimization."""
    return EngineerModuleManual()


def create_qa_engineer_manual() -> QAEngineerModuleManual:
    """Create DSPy QA Engineer module with manual optimization."""
    return QAEngineerModuleManual()


def create_tech_writer_manual() -> TechWriterModuleManual:
    """Create DSPy Technical Writer module with manual optimization."""
    return TechWriterModuleManual()


if __name__ == "__main__":
    # Test module creation
    from dspy_config import configure_dspy

    print("Testing DSPy agent modules with MANUAL optimization...")
    configure_dspy()

    pm = create_product_manager_manual()
    print(f"✅ Product Manager module created (with manual few-shot): {pm}")

    arch = create_architect_manual()
    print(f"✅ Architect module created (with manual few-shot): {arch}")

    eng = create_engineer_manual()
    print(f"✅ Engineer module created: {eng}")

    qa = create_qa_engineer_manual()
    print(f"✅ QA Engineer module created: {qa}")

    tw = create_tech_writer_manual()
    print(f"✅ Tech Writer module created: {tw}")

    print("\n✅ All DSPy agent modules with MANUAL optimization created successfully!")
    print("These modules will make REAL LLM calls with improved prompts via few-shot examples!")
