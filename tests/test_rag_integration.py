#!/usr/bin/env python3
"""
Teste rápido da integração RAG com os agentes.
Valida que os agentes têm acesso às RAG tools.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def test_agent_rag_tools():
    """Testa se os agentes têm as RAG tools."""
    print("🧪 Testando integração RAG com agentes...")
    print()

    try:
        from agents import (
            create_product_manager,
            create_architect,
            create_engineer,
        )

        # Test Product Manager
        pm = create_product_manager()
        pm_tools = [tool.name for tool in pm.tools]
        print(f"✅ Product Manager tools: {len(pm.tools)}")
        print(f"   {pm_tools}")

        assert "retrieve_context" in pm_tools, "PM missing retrieve_context"
        assert "semantic_search" in pm_tools, "PM missing semantic_search"
        print("   ✅ RAG tools presente!")
        print()

        # Test Architect
        arch = create_architect()
        arch_tools = [tool.name for tool in arch.tools]
        print(f"✅ Software Architect tools: {len(arch.tools)}")
        print(f"   {arch_tools}")

        assert "retrieve_context" in arch_tools, "Architect missing retrieve_context"
        assert "semantic_search" in arch_tools, "Architect missing semantic_search"
        print("   ✅ RAG tools presente!")
        print()

        # Test Engineer
        eng = create_engineer()
        eng_tools = [tool.name for tool in eng.tools]
        print(f"✅ Software Engineer tools: {len(eng.tools)}")
        print(f"   {eng_tools}")

        assert "retrieve_context" in eng_tools, "Engineer missing retrieve_context"
        assert "semantic_search" in eng_tools, "Engineer missing semantic_search"
        print("   ✅ RAG tools presente!")
        print()

        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_initialization():
    """Testa se o main.py tem as funções de inicialização RAG."""
    print("🧪 Testando funções de inicialização...")
    print()

    try:
        # Importar main não vai executar nada ainda
        import main

        # Verificar se as funções existem
        assert hasattr(main, "initialize_rag"), "main.py missing initialize_rag"
        print("✅ main.initialize_rag() presente")

        assert hasattr(main, "initialize_observability"), "main.py missing initialize_observability"
        print("✅ main.initialize_observability() presente")

        print()
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_base_exists():
    """Verifica se a base de conhecimento existe."""
    print("🧪 Verificando base de conhecimento...")
    print()

    from pathlib import Path

    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("❌ Diretório knowledge_base não encontrado")
        return False

    # Contar arquivos
    files = list(kb_path.rglob("*.*"))
    print(f"✅ Base de conhecimento encontrada")
    print(f"   Arquivos: {len(files)}")

    # Listar arquivos
    for f in files:
        rel_path = f.relative_to(kb_path)
        print(f"   - {rel_path}")

    print()
    return True


def main():
    """Executa todos os testes."""
    print("=" * 80)
    print("🚀 TESTE DE INTEGRAÇÃO RAG")
    print("=" * 80)
    print()

    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY não configurada")
        print("   Configure antes de executar o sistema completo.")
        print()

    tests = [
        ("Base de Conhecimento", test_knowledge_base_exists),
        ("Funções de Inicialização", test_main_initialization),
        ("Agentes com RAG Tools", test_agent_rag_tools),
    ]

    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))

    # Resumo
    print("=" * 80)
    print("📊 RESUMO DOS TESTES")
    print("=" * 80)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name:30s}: {status}")

    print()
    print("=" * 80)
    print(f"Resultado: {passed}/{total} testes passaram")
    print("=" * 80)
    print()

    if passed == total:
        print("🎉 Todos os testes passaram!")
        print()
        print("✅ A integração RAG está funcionando!")
        print()
        print("Próximos passos:")
        print("  1. Configure OPENAI_API_KEY no .env (se ainda não fez)")
        print("  2. Execute: ./quick_test.sh")
        print("  3. Os agentes usarão RAG automaticamente!")
        print()
    else:
        print(f"⚠️  {total - passed} teste(s) falharam.")
        print("Verifique os erros acima antes de executar.")


if __name__ == "__main__":
    main()
