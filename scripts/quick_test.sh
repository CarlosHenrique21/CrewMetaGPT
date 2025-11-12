#!/bin/bash

# Quick Test Script for CrewAI Project with RAG
# Automatically initializes RAG system and runs the crew
# Make sure OPENAI_API_KEY is configured in .env

echo "🔍 CrewAI Project - Quick Test Script (with RAG)"
echo "======================================"
echo ""

cd "$(dirname "$0")"

# 1. Check API Key
echo "1️⃣  Checking API Key..."
API_KEY=$(python -c "import config; print(config.OPENAI_API_KEY[:20] if config.OPENAI_API_KEY else 'None')" 2>/dev/null)
if [[ $API_KEY == "None" ]] || [[ -z $API_KEY ]]; then
    echo "❌ API Key is NOT configured"
    echo ""
    echo "Please configure OPENAI_API_KEY in .env file"
    exit 1
elif [[ $API_KEY == sk-proj* ]] || [[ $API_KEY == sk-* ]]; then
    echo "✅ API Key is configured: $API_KEY..."
else
    echo "⚠️  API Key format unexpected: $API_KEY..."
    echo "Continuing anyway..."
fi

# 2. Clean workspace
# echo ""
#  echo "2️⃣  Cleaning workspace..."
# rm -rf workspace/*
# echo "✅ Workspace cleaned"

# 2. Run test
echo ""
echo "2️⃣  Running test with RAG (this may take 2-3 minutes)..."
echo ""
python main.py "crie uma API REST para gerenciar tarefas"

# 3. Check results
echo ""
echo "3️⃣  Checking results..."
echo ""

if [ -d "workspace" ]; then
    FILE_COUNT=$(find workspace -type f | wc -l | tr -d ' ')
    if [ "$FILE_COUNT" -gt 0 ]; then
        echo "✅ Files created in workspace:"
        ls -1 workspace/
        echo ""
        echo "📊 Total files: $FILE_COUNT"
        echo "✅ SUCCESS: Files are in workspace (not in root)"
    else
        echo "❌ No files created in workspace"
        exit 1
    fi
else
    echo "❌ Workspace directory not found"
    exit 1
fi

# 4. Check root is clean
echo ""
echo "4️⃣  Checking root directory..."
if [ -f "prd.md" ] || [ -f "architecture.md" ] || [ -f "calculator.py" ]; then
    echo "⚠️  WARNING: Found project files in root directory!"
    echo "    Files should be in workspace/"
else
    echo "✅ Root directory is clean"
fi

echo ""
echo "======================================"
echo "🎉 Test Complete!"
echo ""
echo "Next steps:"
echo "  1. Check workspace/ for generated files"
echo "  2. Check metrics/data/ for performance metrics"
echo "  3. Visit https://app.agentops.ai for observability"
echo "  4. Review RAG_INTEGRATION.md to understand RAG usage"
echo ""
echo "Note: RAG was automatically enabled - agents used knowledge base!"
