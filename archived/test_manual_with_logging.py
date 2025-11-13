#!/usr/bin/env python3
"""Test manual DSPy with verbose logging to verify LLM calls."""
import dspy
from dspy_config import configure_dspy
from agents_dspy_manual import ProductManagerModuleManual
import time

print("=" * 80)
print("🔍 TESTE DE VERIFICAÇÃO: DSPy está fazendo LLM calls reais?")
print("=" * 80)
print()

# Configure DSPy
print("⚙️  Configuring DSPy...")
configure_dspy()
print()

# Create PM module
print("🏗️  Creating Product Manager module with manual optimization...")
pm = ProductManagerModuleManual()
print()

# Test with a simple idea
test_idea = "Build a simple TODO CLI app"
print(f"📋 Test input: {test_idea}")
print()

# Time the execution
print("⏱️  Starting execution...")
print("   (Se for < 2s = cache, se > 5s = LLM call real)")
print()

start = time.time()

try:
    result = pm(project_idea=test_idea)
    duration = time.time() - start

    print()
    print("=" * 80)
    print("✅ RESULTADO")
    print("=" * 80)
    print(f"⏱️  Duração: {duration:.2f}s")
    print(f"📝 Output length: {len(result.prd_content)} chars")
    print()
    print("Primeiras 200 chars do output:")
    print("-" * 80)
    print(result.prd_content[:200])
    print("-" * 80)
    print()

    if duration < 2:
        print("⚠️  MUITO RÁPIDO! Provavelmente usando cache.")
    elif duration < 5:
        print("🤔 MODERADO. Pode ser cache ou LLM call rápido.")
    else:
        print("✅ LENTO! Definitivamente fazendo LLM call real.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
print("FIM DO TESTE")
print("=" * 80)
