# rag/retriever_tools.py
"""
Tools de RAG para uso com CrewAI agents.
Integra vector store com o sistema de tools do CrewAI.
"""
import time
from pathlib import Path
from typing import Optional
from crewai.tools import tool

from rag.vector_store import VectorStore, DocumentLoader, create_vector_store
from metrics import get_tracker


# Instância global do vector store (será inicializada no primeiro uso)
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Retorna instância global do vector store."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
        # Tentar carregar índice existente
        _vector_store.load_index()
    return _vector_store


@tool("initialize_knowledge_base")
def initialize_knowledge_base_tool(directory: str = "knowledge_base") -> str:
    """
    Inicializa a base de conhecimento carregando documentos de um diretório.

    Args:
        directory: Caminho do diretório com documentos (default: knowledge_base/)

    Returns:
        Mensagem de status da inicialização
    """
    start_time = time.time()

    try:
        kb_path = Path(directory)
        if not kb_path.exists():
            return f"❌ Diretório {directory} não encontrado"

        # Criar e popular vector store
        vector_store = create_vector_store(directory)

        # Atualizar instância global
        global _vector_store
        _vector_store = vector_store

        stats = vector_store.get_stats()
        duration = time.time() - start_time

        # Rastrear métricas
        tracker = get_tracker()
        tracker.track_tool_call("initialize_knowledge_base", duration, True)

        return f"""✅ Base de conhecimento inicializada com sucesso!

📊 Estatísticas:
- Total de documentos: {stats['total_documents']}
- Modelo de embedding: {stats['embedding_model']}
- Dimensão dos vetores: {stats['dimension']}
- Tempo de inicialização: {duration:.2f}s

A base de conhecimento está pronta para buscas semânticas."""

    except Exception as e:
        duration = time.time() - start_time
        tracker = get_tracker()
        tracker.track_tool_call("initialize_knowledge_base", duration, False)
        return f"❌ Erro ao inicializar base de conhecimento: {str(e)}"


@tool("semantic_search")
def semantic_search_tool(query: str, top_k: int = 5) -> str:
    """
    Realiza busca semântica na base de conhecimento.

    Args:
        query: Texto da query de busca
        top_k: Número de resultados a retornar (default: 5)

    Returns:
        Documentos relevantes encontrados
    """
    start_time = time.time()

    try:
        vector_store = get_vector_store()

        if len(vector_store.documents) == 0:
            return """⚠️  Base de conhecimento vazia.

Use a tool 'initialize_knowledge_base' primeiro para carregar documentos."""

        # Realizar busca
        embedding_start = time.time()
        results = vector_store.search(query, top_k=top_k)
        embedding_latency = time.time() - embedding_start

        if not results:
            return f"ℹ️  Nenhum documento relevante encontrado para: '{query}'"

        # Rastrear métricas
        duration = time.time() - start_time
        tracker = get_tracker()

        # Calcular relevance score médio
        avg_relevance = sum(r['score'] for r in results) / len(results)

        tracker.track_retrieval(
            duration=duration,
            docs_retrieved=len(results),
            relevance_score=avg_relevance,
            embedding_latency=embedding_latency
        )
        tracker.track_tool_call("semantic_search", duration, True)

        # Formatar resultados
        formatted_results = f"""🔍 Busca semântica: '{query}'

📊 Encontrados {len(results)} documentos relevantes:

"""
        for i, result in enumerate(results, 1):
            doc_preview = result['document'][:300]
            if len(result['document']) > 300:
                doc_preview += "..."

            formatted_results += f"""
--- Resultado {i} (Score: {result['score']:.3f}) ---
Fonte: {result['metadata'].get('source', 'N/A')}
Conteúdo:
{doc_preview}

"""

        formatted_results += f"\n⏱️  Busca realizada em {duration:.3f}s"
        return formatted_results

    except Exception as e:
        duration = time.time() - start_time
        tracker = get_tracker()
        tracker.track_tool_call("semantic_search", duration, False)
        return f"❌ Erro na busca semântica: {str(e)}"


@tool("retrieve_context")
def retrieve_context_tool(task_description: str, top_k: int = 3) -> str:
    """
    Recupera contexto relevante da base de conhecimento para uma tarefa específica.
    Otimizado para fornecer contexto útil aos agentes.

    Args:
        task_description: Descrição da tarefa ou necessidade
        top_k: Número de documentos a recuperar (default: 3)

    Returns:
        Contexto relevante formatado para uso pelo agente
    """
    start_time = time.time()

    try:
        vector_store = get_vector_store()

        if len(vector_store.documents) == 0:
            return """ℹ️  Base de conhecimento não inicializada.

Prosseguindo sem contexto adicional da base de conhecimento."""

        # Buscar documentos relevantes
        results = vector_store.search(task_description, top_k=top_k, score_threshold=0.5)

        if not results:
            return f"""ℹ️  Nenhum contexto relevante encontrado na base de conhecimento para: '{task_description}'

Prosseguindo com conhecimento geral."""

        # Rastrear métricas
        duration = time.time() - start_time
        tracker = get_tracker()
        avg_relevance = sum(r['score'] for r in results) / len(results)
        tracker.track_retrieval(
            duration=duration,
            docs_retrieved=len(results),
            relevance_score=avg_relevance,
            embedding_latency=0.0  # Já incluído na busca
        )
        tracker.track_tool_call("retrieve_context", duration, True)

        # Formatar contexto de forma otimizada
        context = f"""📚 CONTEXTO DA BASE DE CONHECIMENTO
(Relevância: {avg_relevance:.2f})

"""
        for i, result in enumerate(results, 1):
            source_file = Path(result['metadata'].get('source', 'unknown')).name
            context += f"""### Fonte {i}: {source_file} (Score: {result['score']:.2f})

{result['document']}

---

"""

        context += f"""
💡 Use este contexto para enriquecer sua resposta, seguir melhores práticas e incluir exemplos relevantes.
"""

        return context

    except Exception as e:
        duration = time.time() - start_time
        tracker = get_tracker()
        tracker.track_tool_call("retrieve_context", duration, False)
        return f"⚠️  Erro ao recuperar contexto: {str(e)}\n\nProsseguindo sem contexto adicional."


@tool("add_document_to_kb")
def add_document_tool(content: str, source: str = "user_provided") -> str:
    """
    Adiciona um documento à base de conhecimento.

    Args:
        content: Conteúdo do documento
        source: Origem/identificador do documento

    Returns:
        Confirmação da adição
    """
    start_time = time.time()

    try:
        vector_store = get_vector_store()

        if vector_store.index is None:
            vector_store.initialize_index()

        # Adicionar documento
        metadata = {'source': source, 'added_at': time.strftime('%Y-%m-%d %H:%M:%S')}
        vector_store.add_documents([content], [metadata])

        # Salvar
        vector_store.save_index()

        duration = time.time() - start_time
        tracker = get_tracker()
        tracker.track_tool_call("add_document_to_kb", duration, True)

        return f"""✅ Documento adicionado à base de conhecimento

Fonte: {source}
Tamanho: {len(content)} caracteres
Tempo: {duration:.2f}s

Total de documentos na base: {len(vector_store.documents)}"""

    except Exception as e:
        duration = time.time() - start_time
        tracker = get_tracker()
        tracker.track_tool_call("add_document_to_kb", duration, False)
        return f"❌ Erro ao adicionar documento: {str(e)}"


@tool("get_kb_stats")
def get_kb_stats_tool() -> str:
    """
    Retorna estatísticas da base de conhecimento.

    Returns:
        Estatísticas formatadas
    """
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_stats()

        return f"""📊 Estatísticas da Base de Conhecimento

Total de documentos: {stats['total_documents']}
Modelo de embedding: {stats['embedding_model']}
Dimensão dos vetores: {stats['dimension']}
Coleção: {stats['collection_name']}
Índice inicializado: {'✅ Sim' if stats['has_index'] else '❌ Não'}
"""
    except Exception as e:
        return f"❌ Erro ao obter estatísticas: {str(e)}"


# Exportar tools
knowledge_base_tools = [
    initialize_knowledge_base_tool,
    semantic_search_tool,
    retrieve_context_tool,
    add_document_tool,
    get_kb_stats_tool,
]


# Função helper para criar vector store manualmente
def setup_knowledge_base(directory: str = "knowledge_base") -> VectorStore:
    """
    Função helper para setup manual da base de conhecimento.
    Útil para scripts de inicialização.
    """
    return create_vector_store(directory)
