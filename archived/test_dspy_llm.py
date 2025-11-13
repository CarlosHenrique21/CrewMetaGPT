#!/usr/bin/env python3
"""Teste simples para verificar se DSPy está fazendo LLM calls reais."""
import dspy
from dspy_config import configure_dspy

print("Configurando DSPy...")
configure_dspy()

print("\nCriando signature...")
class SimpleTask(dspy.Signature):
    """Generate a simple task description."""
    task_name = dspy.InputField()
    description = dspy.OutputField()

print("Testando com dspy.Predict (sem cache)...")
predictor = dspy.Predict(SimpleTask)

print("\nExecutando predição...")
result = predictor(task_name="Build a TODO app")

print(f"\n✅ Resultado:")
print(f"   Task: Build a TODO app")
print(f"   Description: {result.description}")
print(f"   Tipo: {type(result)}")

print("\n✅ Teste concluído!")
print("Se você viu uma descrição real, o LLM está funcionando.")
print("Se foi muito rápido (< 1s), pode estar usando cache.")
