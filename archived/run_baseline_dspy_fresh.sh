#!/bin/bash
# Script para executar teste baseline COM RAG + DSPy FRESH (LLM calls reais)

echo "================================================================================"
echo "🧪 CrewAI Baseline Test - COM RAG + DSPy FRESH (LLM CALLS REAIS)"
echo "================================================================================"
echo ""
echo "Este script executa 5 projetos usando agentes DSPy COM RAG."
echo "DIFERENÇA: Pipeline fresh SEM otimização - faz LLM calls reais!"
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

# Informar sobre RAG + DSPy Fresh
echo "✅ RAG: HABILITADO"
echo "🔧 DSPy: FRESH (LLM calls reais, não otimizado)"
echo ""

# Executar teste
echo "Iniciando teste baseline COM RAG + DSPy Fresh..."
echo "Duração estimada: 15-25 minutos (faz LLM calls reais!)"
echo "Custo estimado: ~\$2.00-4.00"
echo ""

# Adicionar diretório atual ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

python tests/test_baseline_dspy_fresh.py --yes
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Teste baseline COM RAG + DSPy Fresh concluído com sucesso!"
    echo ""
    echo "📊 Resultados salvos em:"
    echo "   - metrics/data/dspy_fresh/baseline_report.json (relatório consolidado)"
    echo "   - metrics/data/dspy_fresh/baseline_project_*.json (métricas individuais)"
    echo ""
    echo "📈 Próximos passos:"
    echo "   1. Compare com outros baselines"
    echo "   2. Analise o relatório:"
    echo "      cat metrics/data/dspy_fresh/baseline_report.json | python -m json.tool"
    echo ""
else
    echo "❌ Teste baseline COM RAG + DSPy Fresh falhou com código $EXIT_CODE"
    echo ""
    echo "Verifique os logs acima para mais detalhes."
    echo ""
fi

exit $EXIT_CODE
