#!/usr/bin/env python3
"""
Simple test to verify DSPy LM is working with current API key.
"""
import dspy
from dspy_config import configure_dspy

# Configure DSPy
print("Configuring DSPy...")
configure_dspy()

# Test 1: Simple signature
print("\n" + "="*80)
print("Test 1: Simple DSPy signature")
print("="*80)

class SimpleQA(dspy.Signature):
    """Answer a simple question."""
    question = dspy.InputField()
    answer = dspy.OutputField()

# Try basic prediction
try:
    predictor = dspy.Predict(SimpleQA)
    result = predictor(question="What is 2+2?")
    print(f"✅ Simple predict works!")
    print(f"   Question: What is 2+2?")
    print(f"   Answer: {result.answer}")
except Exception as e:
    print(f"❌ Simple predict failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: ChainOfThought
print("\n" + "="*80)
print("Test 2: DSPy ChainOfThought")
print("="*80)

try:
    cot = dspy.ChainOfThought(SimpleQA)
    result = cot(question="What is the capital of France?")
    print(f"✅ ChainOfThought works!")
    print(f"   Question: What is the capital of France?")
    print(f"   Answer: {result.answer}")
except Exception as e:
    print(f"❌ ChainOfThought failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("Test complete!")
print("="*80)
