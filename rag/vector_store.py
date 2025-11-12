# rag/vector_store.py
"""
Vector Store para gerenciamento de embeddings e busca semântica.
Suporta FAISS para armazenamento local eficiente.
"""
import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS não instalado. Instale com: pip install faiss-cpu")

from openai import OpenAI


class VectorStore:
    """
    Armazena e busca documentos usando embeddings vetoriais.
    """

    def __init__(
        self,
        collection_name: str = "knowledge_base",
        persist_directory: str = "rag/vector_db",
        embedding_model: str = "text-embedding-3-small"
    ):
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.embedding_model = embedding_model

        # OpenAI client para embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada")
        self.client = OpenAI(api_key=api_key)

        # FAISS index
        self.index = None
        self.documents = []  # Lista de documentos
        self.metadata = []   # Metadados dos documentos
        self.dimension = 1536  # Dimensão do embedding (text-embedding-3-small)

        # Tentar carregar índice existente
        self.load_index()

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Gera embedding para um texto usando OpenAI.

        Args:
            text: Texto para gerar embedding

        Returns:
            Vetor numpy com o embedding
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            return embedding
        except Exception as e:
            print(f"❌ Erro ao gerar embedding: {e}")
            raise

    def get_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Gera embeddings para múltiplos textos.

        Args:
            texts: Lista de textos

        Returns:
            Array numpy com embeddings (shape: [n_texts, dimension])
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            embeddings = np.array(
                [item.embedding for item in response.data],
                dtype=np.float32
            )
            return embeddings
        except Exception as e:
            print(f"❌ Erro ao gerar embeddings em lote: {e}")
            raise

    def initialize_index(self):
        """Inicializa índice FAISS."""
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS não está instalado")

        # Usar IndexFlatL2 para busca exata (melhor para pequenos datasets)
        # Para datasets maiores, considerar IndexIVFFlat
        self.index = faiss.IndexFlatL2(self.dimension)
        print(f"✅ Índice FAISS inicializado (dimensão: {self.dimension})")

    def add_documents(
        self,
        documents: List[str],
        metadata: Optional[List[Dict]] = None
    ) -> int:
        """
        Adiciona documentos ao vector store.

        Args:
            documents: Lista de textos
            metadata: Lista de metadados (opcional)

        Returns:
            Número de documentos adicionados
        """
        if not documents:
            return 0

        if self.index is None:
            self.initialize_index()

        # Gerar embeddings
        print(f"🔄 Gerando embeddings para {len(documents)} documentos...")
        embeddings = self.get_embeddings_batch(documents)

        # Adicionar ao índice FAISS
        self.index.add(embeddings)

        # Armazenar documentos e metadata
        self.documents.extend(documents)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in documents])

        print(f"✅ {len(documents)} documentos adicionados ao vector store")
        return len(documents)

    def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Dict]:
        """
        Busca documentos similares.

        Args:
            query: Query de busca
            top_k: Número de resultados
            score_threshold: Limite de similaridade (opcional)

        Returns:
            Lista de documentos com scores e metadata
        """
        if self.index is None or len(self.documents) == 0:
            print("⚠️  Vector store vazio")
            return []

        # Gerar embedding da query
        query_embedding = self.get_embedding(query)
        query_embedding = np.array([query_embedding])

        # Buscar no FAISS
        distances, indices = self.index.search(query_embedding, top_k)

        # Preparar resultados
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS retorna -1 se não encontrar suficientes
                continue

            # Converter distância L2 para score de similaridade (0-1)
            # Score mais alto = mais similar
            similarity_score = 1 / (1 + distance)

            if score_threshold and similarity_score < score_threshold:
                continue

            result = {
                'document': self.documents[idx],
                'metadata': self.metadata[idx],
                'score': float(similarity_score),
                'rank': i + 1
            }
            results.append(result)

        return results

    def save_index(self):
        """Salva índice e documentos em disco."""
        if self.index is None:
            print("⚠️  Nenhum índice para salvar")
            return

        # Salvar índice FAISS
        index_path = self.persist_directory / f"{self.collection_name}.index"
        faiss.write_index(self.index, str(index_path))

        # Salvar documentos e metadata
        data_path = self.persist_directory / f"{self.collection_name}.pkl"
        with open(data_path, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata,
                'dimension': self.dimension
            }, f)

        print(f"✅ Vector store salvo em {self.persist_directory}")

    def load_index(self):
        """Carrega índice e documentos do disco."""
        index_path = self.persist_directory / f"{self.collection_name}.index"
        data_path = self.persist_directory / f"{self.collection_name}.pkl"

        if not index_path.exists() or not data_path.exists():
            print(f"ℹ️  Nenhum índice existente encontrado em {self.persist_directory}")
            return

        try:
            # Carregar índice FAISS
            self.index = faiss.read_index(str(index_path))

            # Carregar documentos e metadata
            with open(data_path, 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
                self.dimension = data['dimension']

            print(f"✅ Vector store carregado: {len(self.documents)} documentos")
        except Exception as e:
            print(f"❌ Erro ao carregar vector store: {e}")
            self.index = None
            self.documents = []
            self.metadata = []

    def clear(self):
        """Limpa o vector store."""
        self.index = None
        self.documents = []
        self.metadata = []
        print("✅ Vector store limpo")

    def get_stats(self) -> Dict:
        """Retorna estatísticas do vector store."""
        return {
            'total_documents': len(self.documents),
            'dimension': self.dimension,
            'embedding_model': self.embedding_model,
            'collection_name': self.collection_name,
            'has_index': self.index is not None
        }


class DocumentLoader:
    """
    Carrega documentos de diferentes formatos.
    """

    @staticmethod
    def load_text_file(file_path: Path) -> str:
        """Carrega arquivo de texto."""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"❌ Erro ao carregar {file_path}: {e}")
            return ""

    @staticmethod
    def load_directory(
        directory: Path,
        extensions: List[str] = ['.txt', '.md', '.py'],
        recursive: bool = True
    ) -> List[Dict]:
        """
        Carrega todos os arquivos de um diretório.

        Args:
            directory: Caminho do diretório
            extensions: Extensões aceitas
            recursive: Buscar recursivamente

        Returns:
            Lista de dicts com 'content' e 'metadata'
        """
        documents = []
        pattern = "**/*" if recursive else "*"

        for ext in extensions:
            for file_path in directory.glob(f"{pattern}{ext}"):
                if file_path.is_file():
                    content = DocumentLoader.load_text_file(file_path)
                    if content:
                        documents.append({
                            'content': content,
                            'metadata': {
                                'source': str(file_path),
                                'filename': file_path.name,
                                'extension': ext,
                                'size': len(content)
                            }
                        })

        print(f"✅ Carregados {len(documents)} documentos de {directory}")
        return documents

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[str]:
        """
        Divide texto em chunks menores.

        Args:
            text: Texto para dividir
            chunk_size: Tamanho do chunk
            chunk_overlap: Sobreposição entre chunks

        Returns:
            Lista de chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap

        return chunks


# Funções auxiliares
def create_vector_store(
    knowledge_base_dir: str = "knowledge_base",
    collection_name: str = "knowledge_base"
) -> VectorStore:
    """
    Cria e popula vector store a partir de um diretório.

    Args:
        knowledge_base_dir: Diretório com arquivos
        collection_name: Nome da coleção

    Returns:
        VectorStore populado
    """
    vector_store = VectorStore(collection_name=collection_name)

    # Carregar documentos
    kb_path = Path(knowledge_base_dir)
    if not kb_path.exists():
        print(f"⚠️  Diretório {knowledge_base_dir} não encontrado")
        return vector_store

    loader = DocumentLoader()
    docs_data = loader.load_directory(kb_path)

    if not docs_data:
        print("⚠️  Nenhum documento encontrado")
        return vector_store

    # Extrair documentos e metadata
    documents = [d['content'] for d in docs_data]
    metadata = [d['metadata'] for d in docs_data]

    # Adicionar ao vector store
    vector_store.add_documents(documents, metadata)

    # Salvar
    vector_store.save_index()

    return vector_store
