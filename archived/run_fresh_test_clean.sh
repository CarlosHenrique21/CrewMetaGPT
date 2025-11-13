#!/bin/bash
# Wrapper para executar teste DSPy fresh com ambiente completamente limpo

echo "🔄 Limpando variáveis de ambiente..."
unset OPENAI_API_KEY
unset AGENTOPS_API_KEY

echo "📁 Mudando para diretório do projeto..."
cd "$(dirname "$0")" || exit 1

echo "✅ Executando teste com ambiente limpo..."
echo ""

# Executar Python com ambiente limpo, forçando reload do .env
exec python -c "
import os
import sys

# Limpar qualquer API key em memória
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

# Forçar reload do .env
from dotenv import load_dotenv
load_dotenv(override=True)

# Verificar se carregou corretamente
api_key = os.getenv('OPENAI_API_KEY', '')
print(f'✅ API Key carregada: {api_key[:40]}... ({len(api_key)} chars)')
print()

# Agora executar o teste
sys.path.insert(0, '.')
from tests.test_baseline_dspy_fresh import main
sys.exit(main())
"
