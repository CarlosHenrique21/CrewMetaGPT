# agents_dspy.py
"""
Software development agents using DSPy for prompt optimization.
Each agent is a DSPy Module with optimizable signatures.
"""
import dspy
from typing import List, Optional
from tools import (
    file_writer_tool,
    file_reader_tool,
    directory_reader_tool,
    directory_creator_tool,
)


# ============================================================================
# DSPy Signatures (Declarative Prompts)
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
# DSPy Modules (Agents)
# ============================================================================

class ProductManagerModule(dspy.Module):
    """
    Product Manager agent as DSPy Module.
    Uses ChainOfThought with retrieval for context.
    """

    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.generate_prd = dspy.ChainOfThought(CreatePRDSignature)

    def forward(self, project_idea: str):
        """
        Generate PRD with RAG context.

        Args:
            project_idea: The project description

        Returns:
            DSPy Prediction with prd_content
        """
        try:
            # Retrieve relevant context
            context_query = f"PRD templates and best practices for: {project_idea}"
            retrieval_result = self.retrieve(context_query)

            # retrieval_result is now a list of Prediction objects with long_text
            # Extract the long_text from each passage
            if isinstance(retrieval_result, list):
                context_docs = [psg.long_text for psg in retrieval_result if hasattr(psg, 'long_text')]
            else:
                context_docs = []
            context = "\n\n".join(context_docs) if context_docs else ""

            # Generate PRD with context
            result = self.generate_prd(
                project_idea=project_idea,
                context=context
            )

            return result
        except Exception as e:
            print(f"❌ Error in ProductManager: {e}")
            import traceback
            traceback.print_exc()
            # Return a basic prediction on error
            return dspy.Prediction(prd_content=f"Error generating PRD: {e}")


class ArchitectModule(dspy.Module):
    """
    Software Architect agent as DSPy Module.
    Uses ChainOfThought with retrieval for architecture patterns.
    """

    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.design = dspy.ChainOfThought(DesignArchitectureSignature)

    def forward(self, prd: str):
        """
        Design architecture with RAG context.

        Args:
            prd: Product Requirements Document

        Returns:
            DSPy Prediction with architecture_content
        """
        try:
            # Retrieve architecture patterns
            context_query = f"Software architecture patterns for: {prd[:200]}"
            retrieval_result = self.retrieve(context_query)

            # retrieval_result is now a list of Prediction objects with long_text
            if isinstance(retrieval_result, list):
                context_docs = [psg.long_text for psg in retrieval_result if hasattr(psg, 'long_text')]
            else:
                context_docs = []
            context = "\n\n".join(context_docs) if context_docs else ""

            # Design architecture
            result = self.design(
                prd=prd,
                context=context
            )

            return result
        except Exception as e:
            print(f"❌ Error in Architect: {e}")
            import traceback
            traceback.print_exc()
            return dspy.Prediction(architecture_content=f"Error designing architecture: {e}")


class EngineerModule(dspy.Module):
    """
    Software Engineer agent as DSPy Module.
    Uses ChainOfThought with retrieval for code examples.
    """

    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.implement = dspy.ChainOfThought(ImplementCodeSignature)

    def forward(self, prd: str, architecture: str) -> dspy.Prediction:
        """
        Implement code with RAG context.

        Args:
            prd: Product Requirements Document
            architecture: System architecture

        Returns:
            DSPy Prediction with implementation_plan
        """
        try:
            # Retrieve code examples
            context_query = f"Code examples and patterns for: {architecture[:200]}"
            retrieval_result = self.retrieve(context_query)

            # retrieval_result is now a list of Prediction objects with long_text
            if isinstance(retrieval_result, list):
                context_docs = [psg.long_text for psg in retrieval_result if hasattr(psg, 'long_text')]
            else:
                context_docs = []
            context = "\n\n".join(context_docs) if context_docs else ""

            # Generate implementation
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


class QAEngineerModule(dspy.Module):
    """
    QA Engineer agent as DSPy Module.
    Uses ChainOfThought for test creation.
    """

    def __init__(self):
        super().__init__()
        self.create_tests = dspy.ChainOfThought(CreateTestsSignature)

    def forward(self, implementation_summary: str) -> dspy.Prediction:
        """
        Create test plan.

        Args:
            implementation_summary: Summary of implementation

        Returns:
            DSPy Prediction with test_plan
        """
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


class TechWriterModule(dspy.Module):
    """
    Technical Writer agent as DSPy Module.
    Uses ChainOfThought for documentation.
    """

    def __init__(self):
        super().__init__()
        self.write_docs = dspy.ChainOfThought(CreateDocsSignature)

    def forward(self, project_summary: str) -> dspy.Prediction:
        """
        Create documentation.

        Args:
            project_summary: Complete project summary

        Returns:
            DSPy Prediction with documentation
        """
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

def create_product_manager_dspy() -> ProductManagerModule:
    """Create DSPy Product Manager module."""
    return ProductManagerModule()


def create_architect_dspy() -> ArchitectModule:
    """Create DSPy Architect module."""
    return ArchitectModule()


def create_engineer_dspy() -> EngineerModule:
    """Create DSPy Engineer module."""
    return EngineerModule()


def create_qa_engineer_dspy() -> QAEngineerModule:
    """Create DSPy QA Engineer module."""
    return QAEngineerModule()


def create_tech_writer_dspy() -> TechWriterModule:
    """Create DSPy Technical Writer module."""
    return TechWriterModule()


if __name__ == "__main__":
    # Test module creation
    from dspy_config import configure_dspy

    print("Testing DSPy agent modules...")
    configure_dspy()

    pm = create_product_manager_dspy()
    print(f"✅ Product Manager module created: {pm}")

    arch = create_architect_dspy()
    print(f"✅ Architect module created: {arch}")

    eng = create_engineer_dspy()
    print(f"✅ Engineer module created: {eng}")

    qa = create_qa_engineer_dspy()
    print(f"✅ QA Engineer module created: {qa}")

    tw = create_tech_writer_dspy()
    print(f"✅ Tech Writer module created: {tw}")

    print("\n✅ All DSPy agent modules created successfully!")
