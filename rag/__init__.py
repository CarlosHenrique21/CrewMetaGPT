# rag/__init__.py
"""
Sistema RAG (Retrieval-Augmented Generation) para CrewAI.
"""
from .vector_store import VectorStore, DocumentLoader, create_vector_store
from .retriever_tools import (
    knowledge_base_tools,
    initialize_knowledge_base_tool,
    semantic_search_tool,
    retrieve_context_tool,
    add_document_tool,
    get_kb_stats_tool,
    setup_knowledge_base,
    get_vector_store,
)

__all__ = [
    'VectorStore',
    'DocumentLoader',
    'create_vector_store',
    'knowledge_base_tools',
    'initialize_knowledge_base_tool',
    'semantic_search_tool',
    'retrieve_context_tool',
    'add_document_tool',
    'get_kb_stats_tool',
    'setup_knowledge_base',
    'get_vector_store',
]
