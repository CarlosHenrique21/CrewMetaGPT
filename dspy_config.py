# dspy_config.py
"""
DSPy Configuration for CrewAI Project
Configures LM, retriever, and optimizers for prompt optimization.
"""
import os
import dspy
from pathlib import Path
from typing import List, Optional
import config


class FAISSRetriever(dspy.Retrieve):
    """
    Custom DSPy Retriever using FAISS vector store.
    Integrates our existing RAG system with DSPy.
    """

    def __init__(self, k: int = 3):
        super().__init__(k=k)
        self.k = k
        self._vector_store = None

    @property
    def vector_store(self):
        """Lazy load vector store."""
        if self._vector_store is None:
            from rag import get_vector_store
            self._vector_store = get_vector_store()
        return self._vector_store

    def forward(self, query_or_queries, k: Optional[int] = None):
        """
        Retrieve relevant documents from FAISS.

        Args:
            query_or_queries: Search query (string or list)
            k: Number of results (default: self.k)

        Returns:
            dspy.Prediction with passages attribute
        """
        k = k or self.k

        # Handle both single query and batch queries
        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries

        all_passages = []

        try:
            for query in queries:
                results = self.vector_store.search(query, top_k=k)

                # Format results for DSPy
                # DSPy expects passages to be objects with 'long_text' attribute
                for result in results:
                    # Extract the document text (key is 'document')
                    doc_text = result.get('document', '')
                    if doc_text:
                        # Create a simple object with long_text attribute
                        # Using dotdict (DSPy's utility class)
                        passage = dspy.Prediction(long_text=doc_text)
                        all_passages.append(passage)

            # Return list of passage objects (DSPy will handle this)
            return all_passages

        except Exception as e:
            print(f"⚠️  Error in retrieval: {e}")
            import traceback
            traceback.print_exc()
            # Return empty list on error
            return []


def configure_dspy(
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
) -> None:
    """
    Configure DSPy with OpenAI and custom FAISS retriever.

    Args:
        model: OpenAI model name (default: from config)
        temperature: Sampling temperature
        max_tokens: Maximum tokens per generation
    """
    # Use model from config if not specified
    if model is None:
        model = config.OPENAI_MODEL

    # Configure OpenAI LM using the correct DSPy API
    # DSPy 2.4+ uses dspy.LM with provider specification
    lm = dspy.LM(
        model=f"openai/{model}",
        api_key=config.OPENAI_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Configure FAISS retriever
    retriever = FAISSRetriever(k=3)

    # Set as default LM and RM (Retrieval Model)
    dspy.settings.configure(
        lm=lm,
        rm=retriever,
    )

    print(f"✅ DSPy configured with:")
    print(f"   - Model: {model}")
    print(f"   - Temperature: {temperature}")
    print(f"   - Max Tokens: {max_tokens}")
    print(f"   - Retriever: FAISS (k=3)")


def get_dspy_cache_dir() -> Path:
    """Get directory for DSPy cache and compiled models."""
    cache_dir = Path("dspy_cache")
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def save_compiled_program(program, name: str) -> Path:
    """
    Save a compiled DSPy program.

    Args:
        program: Compiled DSPy program
        name: Name for the saved program

    Returns:
        Path to saved program
    """
    cache_dir = get_dspy_cache_dir()
    save_path = cache_dir / f"{name}.json"

    try:
        program.save(str(save_path))
        print(f"💾 Compiled program saved: {save_path}")
    except Exception as e:
        # If lzma is not available, use pickle as fallback
        print(f"⚠️  Standard save failed ({e}), using pickle fallback...")
        import pickle
        pickle_path = cache_dir / f"{name}.pkl"
        with open(pickle_path, 'wb') as f:
            pickle.dump(program, f)
        print(f"💾 Compiled program saved (pickle): {pickle_path}")
        return pickle_path

    return save_path


def load_compiled_program(program_class, name: str):
    """
    Load a compiled DSPy program.

    Args:
        program_class: DSPy program class
        name: Name of the saved program

    Returns:
        Loaded DSPy program or None if not found
    """
    cache_dir = get_dspy_cache_dir()

    # Try JSON first
    load_path = cache_dir / f"{name}.json"
    if load_path.exists():
        try:
            program = program_class()
            program.load(str(load_path))
            print(f"✅ Compiled program loaded: {load_path}")
            return program
        except Exception as e:
            print(f"⚠️  Error loading JSON: {e}")

    # Try pickle fallback
    pickle_path = cache_dir / f"{name}.pkl"
    if pickle_path.exists():
        try:
            import pickle
            with open(pickle_path, 'rb') as f:
                program = pickle.load(f)
            print(f"✅ Compiled program loaded (pickle): {pickle_path}")
            return program
        except Exception as e:
            print(f"❌ Error loading pickle: {e}")
            return None

    print(f"⚠️  Compiled program not found: {load_path} or {pickle_path}")
    return None


# DSPy Optimizer configurations
OPTIMIZER_CONFIGS = {
    "bootstrap": {
        "name": "BootstrapFewShot",
        "description": "Few-shot learning with bootstrapped examples",
        "max_bootstrapped_demos": 4,
        "max_labeled_demos": 4,
    },
    "mipro": {
        "name": "MIPRO",
        "description": "Multi-prompt instruction optimization",
        "num_candidates": 10,
        "init_temperature": 1.0,
    },
    "copro": {
        "name": "COPRO",
        "description": "Coordinate ascent prompt optimization",
        "breadth": 10,
        "depth": 3,
    },
}


def get_optimizer(optimizer_type: str = "bootstrap", **kwargs):
    """
    Get a DSPy optimizer.

    Args:
        optimizer_type: Type of optimizer (bootstrap, mipro, copro)
        **kwargs: Additional optimizer arguments

    Returns:
        DSPy optimizer instance
    """
    if optimizer_type not in OPTIMIZER_CONFIGS:
        raise ValueError(f"Unknown optimizer: {optimizer_type}. Choose from {list(OPTIMIZER_CONFIGS.keys())}")

    config_dict = OPTIMIZER_CONFIGS[optimizer_type].copy()
    optimizer_name = config_dict.pop("name")
    config_dict.pop("description")

    # Merge with kwargs
    config_dict.update(kwargs)

    if optimizer_name == "BootstrapFewShot":
        return dspy.BootstrapFewShot(**config_dict)
    elif optimizer_name == "MIPRO":
        return dspy.MIPROv2(**config_dict)
    elif optimizer_name == "COPRO":
        return dspy.COPRO(**config_dict)
    else:
        raise ValueError(f"Optimizer {optimizer_name} not implemented")


if __name__ == "__main__":
    # Test configuration
    print("Testing DSPy configuration...")
    configure_dspy()
    print("\n✅ DSPy configuration successful!")
