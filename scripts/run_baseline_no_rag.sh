#!/bin/bash
# Script para executar teste baseline SEM RAG

echo "================================================================================"
echo "🧪 CrewAI Baseline Test - SEM RAG"
echo "================================================================================"
echo ""
echo "Este script executa 5 projetos SEM RAG para comparação."
echo ""

# Mudar para diretório raiz do projeto
cd "$(dirname "$0")/.." || exit 1

# Verificar se API key está configurada
echo "Verificando configuração..."
API_KEY=$(python -c "import config; print(config.OPENAI_API_KEY[:20] if config.OPENAI_API_KEY else 'None')" 2>/dev/null)
if [ "$API_KEY" = "None" ]; then
    echo "❌ OPENAI_API_KEY não configurada!"
    echo ""
    echo "Por favor, configure a API key no arquivo .env:"
    echo "  OPENAI_API_KEY=sk-proj-your-key-here"
    echo ""
    exit 1
fi

if [[ $API_KEY == sk-proj* ]] || [[ $API_KEY == sk-* ]]; then
    echo "✅ API Key configurada: ${API_KEY}..."
else
    echo "⚠️  Formato de API key inesperado: $API_KEY"
    echo "    Continuando mesmo assim..."
fi
echo ""

# Informar sobre RAG
echo "🚫 RAG: DESABILITADO (baseline sem RAG)"
echo ""

# Executar teste
echo "Iniciando teste baseline SEM RAG..."
echo "Duração estimada: 10-15 minutos"
echo "Custo estimado: ~\$1.50-3.00"
echo ""

# Adicionar diretório atual ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

python tests/test_baseline_no_rag.py
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Teste baseline SEM RAG concluído com sucesso!"
    echo ""
    echo "📊 Resultados salvos em:"
    echo "   - metrics/data/no_rag/baseline_report.json (relatório consolidado)"
    echo "   - metrics/data/no_rag/baseline_project_*.json (métricas individuais)"
    echo ""
    echo "📈 Próximos passos:"
    echo "   1. Compare com baseline COM RAG:"
    echo "      python scripts/compare_baselines.py"
    echo ""
    echo "   2. Analise os relatórios:"
    echo "      cat metrics/data/no_rag/baseline_report.json | python -m json.tool"
    echo "      cat metrics/data/baseline_report.json | python -m json.tool"
    echo ""
else
    echo "❌ Teste baseline SEM RAG falhou com código $EXIT_CODE"
    echo ""
    echo "Verifique os logs acima para mais detalhes."
    echo ""
fi

exit $EXIT_CODE
