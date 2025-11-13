# 🧪 Testes CrewAI Project

## Scripts de Teste Disponíveis

### 1. test_baseline.py ⭐
**Teste baseline completo com 5 projetos**

```bash
python tests/test_baseline.py
# ou
./scripts/run_baseline_test.sh
```

**O que faz:**
- Executa 5 projetos diferentes em sequência
- Coleta métricas completas de cada projeto
- Gera relatório consolidado
- Duração: ~10-15 minutos
- Custo: ~$1.50-3.00

**Outputs:**
- `metrics/data/baseline_report.json` - Relatório consolidado
- `metrics/data/baseline_project_*.json` - Métricas individuais

### 2. test_rag_setup.py
**Teste do sistema RAG isolado**

```bash
python tests/test_rag_setup.py
```

**O que testa:**
- Imports dos módulos RAG
- Criação do vector store
- Carregamento da knowledge base
- Sistema de métricas
- RAG tools

**Duração:** ~30 segundos
**Custo:** ~$0.02 (apenas embeddings)

### 3. test_rag_integration.py
**Teste de integração RAG com agentes**

```bash
python tests/test_rag_integration.py
```

**O que verifica:**
- RAG tools estão nos agentes
- Funções de inicialização existem
- Base de conhecimento está presente

**Duração:** ~5 segundos
**Custo:** $0 (sem LLM calls)

### 4. test_crewai_tracking.py
**Teste de tracking com CrewAI**

```bash
python tests/test_crewai_tracking.py
```

**O que testa:**
- Integração com AgentOps
- Tracking de agents, tasks, tools
- LLM call tracking

**Duração:** ~1 minuto
**Custo:** ~$0.10

### 5. test_tracking.py
**Teste adicional de tracking**

```bash
python tests/test_tracking.py
```

Testes adicionais do sistema de observabilidade.

## Fluxo Recomendado

### Setup Inicial
```bash
# 1. Verificar integração RAG
python tests/test_rag_integration.py

# 2. Testar RAG isolado (requer API key)
python tests/test_rag_setup.py
```

### Teste Completo
```bash
# 3. Executar baseline (5 projetos)
./scripts/run_baseline_test.sh

# 4. Analisar resultados
python scripts/analyze_baseline.py
```

## Estrutura de Testes

```
tests/
├── README.md                 # Este arquivo
├── test_baseline.py          # ⭐ Teste principal (5 projetos)
├── test_rag_setup.py         # Teste RAG isolado
├── test_rag_integration.py   # Verificação de integração
├── test_crewai_tracking.py   # Teste de tracking
└── test_tracking.py          # Testes adicionais
```

## Outputs dos Testes

### test_baseline.py
```
metrics/data/
├── baseline_report.json          # Relatório consolidado
├── baseline_project_01.json      # Todo List CLI
├── baseline_project_02.json      # URL Shortener
├── baseline_project_03.json      # Weather CLI
├── baseline_project_04.json      # Password Generator
└── baseline_project_05.json      # Markdown Converter
```

### test_rag_setup.py
```
rag/vector_db/
├── test_collection.index         # Índice FAISS temporário
└── test_collection.pkl           # Dados temporários
```

## Métricas Coletadas

Todos os testes coletam:

### Performance
- ⏱️ Latência total
- ⏱️ Latência por etapa (retrieval, LLM)
- 🚀 Throughput

### Custo
- 💰 Custo em USD
- 🎫 Tokens usados

### Qualidade
- ✅ Taxa de sucesso
- 📊 LLM calls
- 🔍 RAG retrievals

## Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"
```bash
# Configure no .env
echo "OPENAI_API_KEY=sk-proj-your-key" >> ../.env
```

### Erro: "FAISS não instalado"
```bash
pip install faiss-cpu
pip install "numpy<2.0.0"
```

### Erro: "Knowledge base vazia"
```bash
# Verificar se existe
ls -la ../knowledge_base/

# Inicializar manualmente
python -c "from rag import setup_knowledge_base; setup_knowledge_base('knowledge_base')"
```

### Testes falhando
```bash
# Executar em modo verbose
python tests/test_rag_setup.py -v

# Ver logs
tail -f ../agentops.log
```

## Estimativas de Custo e Tempo

| Teste | Duração | Custo (USD) | LLM Calls |
|-------|---------|-------------|-----------|
| test_rag_integration.py | 5s | $0 | 0 |
| test_rag_setup.py | 30s | ~$0.02 | 0 (só embeddings) |
| test_crewai_tracking.py | 1min | ~$0.10 | ~2-3 |
| test_baseline.py | 10-15min | $1.50-3.00 | ~75 |

## Próximos Passos

Após executar os testes:

1. **Analisar resultados**
   ```bash
   python scripts/analyze_baseline.py
   ```

2. **Ver relatório JSON**
   ```bash
   cat metrics/data/baseline_report.json | python -m json.tool
   ```

3. **Consultar documentação**
   - [BASELINE_TEST_GUIDE.md](../docs/BASELINE_TEST_GUIDE.md)
   - [PLANO_ESTUDO_RAG_METRICAS.md](../docs/PLANO_ESTUDO_RAG_METRICAS.md)

## Links Úteis

- 📖 [README Principal](../README.md)
- 📚 [Documentação](../docs/)
- 🔧 [Scripts](../scripts/)
- 🔍 [Sistema RAG](../rag/)
- 📊 [Sistema de Métricas](../metrics/)

---

**Voltar para**: [README Principal](../README.md) | [Documentação](../docs/README.md)
