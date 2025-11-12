#!/usr/bin/env python3
"""
Script de teste para verificar a implementação RAG.
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(override=True)


def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🧪 Testando imports...")

    try:
        from rag import (
            VectorStore,
            setup_knowledge_base,
            knowledge_base_tools,
        )
        print("✅ RAG modules importados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar RAG modules: {e}")
        return False

    try:
        from metrics import MetricsTracker, get_tracker
        print("✅ Metrics modules importados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Metrics modules: {e}")
        return False

    return True


def test_vector_store():
    """Testa criação do vector store."""
    print("\n🧪 Testando Vector Store...")

    try:
        from rag import VectorStore

        # Criar vector store
        vs = VectorStore(collection_name="test_collection")
        print("✅ Vector Store criado com sucesso")

        # Testar adição de documentos
        test_docs = [
            "Python é uma linguagem de programação de alto nível.",
            "Machine Learning é um subcampo da inteligência artificial.",
            "Embeddings são representações vetoriais de texto.",
        ]

        num_added = vs.add_documents(test_docs)
        print(f"✅ {num_added} documentos adicionados ao vector store")

        # Testar busca
        results = vs.search("o que é python", top_k=1)
        if results:
            print(f"✅ Busca funcionou: encontrados {len(results)} resultados")
            print(f"   Top resultado: {results[0]['document'][:50]}...")
        else:
            print("⚠️  Busca não retornou resultados")

        # Limpar
        vs.clear()
        print("✅ Vector store limpo")

        return True
    except Exception as e:
        print(f"❌ Erro no test_vector_store: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_base():
    """Testa carregamento da base de conhecimento."""
    print("\n🧪 Testando Knowledge Base...")

    try:
        from rag import setup_knowledge_base
        from pathlib import Path

        kb_path = Path("knowledge_base")
        if not kb_path.exists():
            print("⚠️  Diretório knowledge_base não encontrado")
            return False

        print(f"📚 Carregando base de conhecimento de {kb_path}...")
        vector_store = setup_knowledge_base(str(kb_path))

        stats = vector_store.get_stats()
        print(f"✅ Base de conhecimento carregada:")
        print(f"   - Total de documentos: {stats['total_documents']}")
        print(f"   - Modelo de embedding: {stats['embedding_model']}")
        print(f"   - Dimensão: {stats['dimension']}")

        # Testar busca na base de conhecimento
        if stats['total_documents'] > 0:
            results = vector_store.search("design patterns python", top_k=2)
            print(f"\n🔍 Teste de busca: encontrados {len(results)} resultados")
            for i, result in enumerate(results, 1):
                print(f"\n   Resultado {i} (Score: {result['score']:.3f}):")
                print(f"   Fonte: {result['metadata'].get('filename', 'N/A')}")
                print(f"   Preview: {result['document'][:100]}...")

        return True
    except Exception as e:
        print(f"❌ Erro no test_knowledge_base: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_metrics():
    """Testa sistema de métricas."""
    print("\n🧪 Testando Sistema de Métricas...")

    try:
        from metrics import MetricsTracker

        tracker = MetricsTracker()
        print("✅ MetricsTracker criado")

        # Testar tracking de retrieval
        tracker.track_retrieval(
            duration=0.5,
            docs_retrieved=3,
            relevance_score=0.85,
            embedding_latency=0.1
        )
        print("✅ Retrieval tracking funcionou")

        # Testar tracking de LLM
        tracker.track_llm_call(
            duration=2.3,
            tokens_prompt=500,
            tokens_completion=800,
            model="gpt-4"
        )
        print("✅ LLM tracking funcionou")

        # Testar tracking de tool
        tracker.track_tool_call("test_tool", 0.1, True)
        print("✅ Tool tracking funcionou")

        # Testar summary
        summary = tracker.get_summary()
        print(f"✅ Summary gerado: {summary['session_id']}")

        return True
    except Exception as e:
        print(f"❌ Erro no test_metrics: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools():
    """Testa RAG tools."""
    print("\n🧪 Testando RAG Tools...")

    try:
        from rag import knowledge_base_tools

        print(f"✅ {len(knowledge_base_tools)} tools disponíveis:")
        for tool in knowledge_base_tools:
            print(f"   - {tool.name}")

        return True
    except Exception as e:
        print(f"❌ Erro no test_tools: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes."""
    print("=" * 80)
    print("🚀 TESTE DE IMPLEMENTAÇÃO RAG")
    print("=" * 80)

    # Verificar variáveis de ambiente
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não encontrada!")
        print("   Configure a variável de ambiente antes de executar os testes.")
        return

    print(f"✅ OPENAI_API_KEY configurada (primeiros 20 chars: {os.getenv('OPENAI_API_KEY')[:20]}...)")

    # Executar testes
    tests = [
        ("Imports", test_imports),
        ("Vector Store", test_vector_store),
        ("Knowledge Base", test_knowledge_base),
        ("Metrics", test_metrics),
        ("Tools", test_tools),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Teste '{name}' falhou com exceção: {e}")
            results.append((name, False))

    # Resumo
    print("\n" + "=" * 80)
    print("📊 RESUMO DOS TESTES")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name:20s}: {status}")

    print("\n" + "=" * 80)
    print(f"Resultado: {passed}/{total} testes passaram")
    print("=" * 80)

    if passed == total:
        print("\n🎉 Todos os testes passaram! A implementação RAG está funcionando corretamente.")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique os erros acima.")


if __name__ == "__main__":
    main()
