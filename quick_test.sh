#!/bin/bash

# Quick Test Script for CrewAI Project
# Run after fixing OPENAI_API_KEY environment variable

echo "🔍 CrewAI Project - Quick Test Script"
echo "======================================"
echo ""

cd "$(dirname "$0")"

# 1. Check API Key
echo "1️⃣  Checking API Key..."
API_KEY=$(python -c "import config; print(config.OPENAI_API_KEY[:20])" 2>/dev/null)
if [[ $API_KEY == "sk-proj--MHwduuoeC4I" ]]; then
    echo "✅ API Key is correct (new key loaded)"
elif [[ $API_KEY == "sk-proj-qjfm7yYc1U7" ]]; then
    echo "❌ API Key is WRONG (old key still loaded)"
    echo ""
    echo "Fix with:"
    echo "  unset OPENAI_API_KEY"
    echo "  export OPENAI_API_KEY=\"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\""
    exit 1
else
    echo "⚠️  Unknown API Key: $API_KEY"
    exit 1
fi

# 2. Clean workspace
# echo ""
#  echo "2️⃣  Cleaning workspace..."
# rm -rf workspace/*
# echo "✅ Workspace cleaned"

# 3. Run test
echo ""
echo "3️⃣  Running test (this may take 2-3 minutes)..."
echo ""
python main.py "write a cli snake game based on pygame"

# 4. Check results
echo ""
echo "4️⃣  Checking results..."
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

# 5. Check root is clean
echo ""
echo "5️⃣  Checking root directory..."
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
echo "  2. Visit https://app.agentops.ai for observability"
echo "  3. Try other prompts from test_prompts.json"
