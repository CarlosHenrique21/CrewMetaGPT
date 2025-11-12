#!/bin/bash

# Script para executar teste baseline
# Executa 5 projetos em sequência e coleta métricas

echo "🧪 CrewAI Baseline Test"
echo "======================================"
echo ""
echo "Este teste executa 5 projetos para estabelecer baseline de performance."
echo "Duração estimada: 10-15 minutos"
echo ""

cd "$(dirname "$0")/.."

# Verificar API Key
echo "Verificando configuração..."
API_KEY=$(python -c "import config; print(config.OPENAI_API_KEY[:20] if config.OPENAI_API_KEY else 'None')" 2>/dev/null)
if [[ $API_KEY == "None" ]] || [[ -z $API_KEY ]]; then
    echo "❌ OPENAI_API_KEY não configurada!"
    echo ""
    echo "Configure no arquivo .env antes de executar:"
    echo "  OPENAI_API_KEY=sk-proj-your-key-here"
    exit 1
fi

echo "✅ API Key configurada"
echo ""

# Criar diretório de output se não existir
mkdir -p metrics/data

# Limpar workspace anterior (opcional)
# echo "Limpando workspace anterior..."
# rm -rf workspace/*

# Executar teste
echo "======================================"
echo "Iniciando teste baseline..."
echo "======================================"
echo ""

python tests/test_baseline.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ Teste baseline concluído com sucesso!"
    echo "======================================"
    echo ""
    echo "📊 Resultados:"
    echo "   - Relatório: metrics/data/baseline_report.json"
    echo "   - Métricas individuais: metrics/data/baseline_project_*.json"
    echo "   - Arquivos gerados: workspace/"
    echo ""
    echo "Para visualizar o relatório:"
    echo "   cat metrics/data/baseline_report.json | python -m json.tool"
    echo ""
else
    echo ""
    echo "======================================"
    echo "❌ Teste baseline falhou (código: $EXIT_CODE)"
    echo "======================================"
    echo ""
fi

exit $EXIT_CODE
