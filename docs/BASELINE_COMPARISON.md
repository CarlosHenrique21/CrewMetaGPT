# 📊 Comparação de Baselines: COM RAG vs SEM RAG

## Visão Geral

Este documento descreve o processo de comparação entre dois baselines do sistema CrewAI:
- **Baseline COM RAG**: Sistema com Retrieval-Augmented Generation habilitado
- **Baseline SEM RAG**: Sistema usando apenas conhecimento do LLM

## 🎯 Objetivo

Medir o impacto quantitativo do RAG no sistema CrewAI através de métricas objetivas:
- **Custo** ($): Quanto custa executar cada configuração
- **Tokens**: Quantos tokens são consumidos
- **Performance** (tempo): Quanto tempo leva para executar
- **LLM Calls**: Quantas chamadas são feitas ao LLM
- **RAG Retrievals**: Quantas buscas no knowledge base são feitas (apenas COM RAG)

## 📁 Estrutura de Arquivos

### Arquivos COM RAG (Original)
```
# Código
agents.py                    # Agentes COM RAG tools
tasks.py                     # Tasks usando agents.py
crew.py                      # Crew usando tasks.py

# Teste
tests/test_baseline.py       # Teste baseline COM RAG

# Script
scripts/run_baseline_test.sh # Executa teste COM RAG

# Métricas
metrics/data/
├── baseline_report.json               # Relatório consolidado
└── baseline_project_*.json            # Métricas por projeto
```

### Arquivos SEM RAG (Novos)
```
# Código
agents_no_rag.py             # Agentes SEM RAG tools
tasks_no_rag.py              # Tasks usando agents_no_rag.py
crew_no_rag.py               # Crew usando tasks_no_rag.py

# Teste
tests/test_baseline_no_rag.py # Teste baseline SEM RAG

# Script
scripts/run_baseline_no_rag.sh # Executa teste SEM RAG

# Métricas
metrics/data/no_rag/
├── baseline_report.json              # Relatório consolidado
└── baseline_project_*.json           # Métricas por projeto
```

### Arquivos de Comparação
```
# Script de comparação
scripts/compare_baselines.py  # Compara os dois baselines

# Relatório de comparação
metrics/data/comparison_report.json  # Análise comparativa
```

## 🔄 Diferenças entre as Versões

### agents.py vs agents_no_rag.py

**COM RAG (agents.py):**
```python
from rag import retrieve_context_tool, semantic_search_tool

def create_product_manager() -> Agent:
    return Agent(
        role="Product Manager",
        backstory="""...
        IMPORTANT: Before creating the PRD, use the retrieve_context tool
        to search the knowledge base for similar projects...""",
        tools=[
            file_writer_tool,
            retrieve_context_tool,     # RAG tool
            semantic_search_tool,      # RAG tool
        ],
    )
```

**SEM RAG (agents_no_rag.py):**
```python
# Sem importações de RAG

def create_product_manager() -> Agent:
    return Agent(
        role="Product Manager",
        backstory="""...""",  # Sem instruções de RAG
        tools=[
            file_writer_tool,
            # Sem RAG tools
        ],
    )
```

### Principais Diferenças:

| Aspecto | COM RAG | SEM RAG |
|---------|---------|---------|
| **RAG Tools** | ✅ retrieve_context, semantic_search | ❌ Não incluído |
| **Backstory** | ✅ Instruções para usar RAG | ❌ Sem instruções RAG |
| **Knowledge Base** | ✅ Acessa 5 documentos | ❌ Não acessa |
| **Context Retrieval** | ✅ Busca semântica habilitada | ❌ Apenas LLM knowledge |
| **Knowledge Manager** | ✅ Agente dedicado | ❌ Não existe |

## 🚀 Como Executar os Baselines

### Passo 1: Executar Baseline COM RAG

```bash
# Executar teste
./scripts/run_baseline_test.sh

# Verificar resultados
cat metrics/data/baseline_report.json | python -m json.tool
```

**Duração estimada:** 10-15 minutos
**Custo estimado:** ~$1.50-3.00

### Passo 2: Executar Baseline SEM RAG

```bash
# Executar teste
./scripts/run_baseline_no_rag.sh

# Verificar resultados
cat metrics/data/no_rag/baseline_report.json | python -m json.tool
```

**Duração estimada:** 10-15 minutos
**Custo estimado:** ~$1.50-3.00

### Passo 3: Comparar os Baselines

```bash
# Executar comparação
python scripts/compare_baselines.py

# Ver relatório de comparação
cat metrics/data/comparison_report.json | python -m json.tool
```

## 📊 Estrutura dos Relatórios

### Relatório Individual (baseline_report.json)

```json
{
  "report_type": "baseline" ou "baseline_no_rag",
  "rag_enabled": true ou false,
  "timestamp": "2025-01-12T...",
  "total_projects": 5,
  "successful_projects": 5,
  "aggregated_stats": {
    "total_cost": 2.5430,
    "avg_cost_per_project": 0.5086,
    "total_tokens": 85340,
    "avg_tokens_per_project": 17068,
    "total_llm_calls": 125,
    "avg_llm_calls_per_project": 25,
    "total_rag_retrievals": 45,  // Apenas COM RAG
    "avg_duration_per_project": 144.1
  },
  "projects": [...]
}
```

### Relatório de Comparação (comparison_report.json)

```json
{
  "timestamp": "2025-01-12T...",
  "baseline_with_rag": {
    "stats": {...}
  },
  "baseline_without_rag": {
    "stats": {...}
  },
  "comparison": {
    "cost": {
      "with_rag": 2.5430,
      "without_rag": 2.3200,
      "difference_percent": 9.61,
      "impact": "increase"
    },
    "tokens": {...},
    "duration": {...},
    "llm_calls": {...}
  }
}
```

## 📈 Métricas Analisadas

### 1. Custo ($)
- **Total Cost**: Custo total de todos os projetos
- **Avg Cost per Project**: Custo médio por projeto
- **Comparação**: % de diferença entre COM e SEM RAG

### 2. Tokens
- **Total Tokens**: Tokens totais consumidos
- **Avg Tokens per Project**: Média de tokens por projeto
- **Comparação**: % de diferença entre COM e SEM RAG

### 3. Performance (Tempo)
- **Avg Duration per Project**: Tempo médio de execução
- **Batch Duration**: Tempo total do batch
- **Comparação**: % de diferença entre COM e SEM RAG

### 4. LLM Calls
- **Total LLM Calls**: Total de chamadas ao LLM
- **Avg LLM Calls**: Média de chamadas por projeto
- **Comparação**: % de diferença entre COM e SEM RAG

### 5. RAG Retrievals (apenas COM RAG)
- **Total RAG Retrievals**: Total de buscas no knowledge base
- **Avg per Project**: Média de retrievals por projeto

## 🔍 Output do Script de Comparação

O script `compare_baselines.py` gera output formatado com:

### Seções:

1. **Informações dos Testes**
   - Data de execução
   - Projetos executados
   - Duração total

2. **Comparação de Custos** 💰
   - Custo total e médio
   - Diferença percentual
   - Indicador visual (📈/📉)

3. **Comparação de Tokens** 🎫
   - Tokens totais e médios
   - Diferença percentual
   - Indicador visual

4. **Comparação de LLM Calls** 📞
   - Calls totais e médias
   - Diferença percentual
   - Indicador visual

5. **Comparação de Performance** ⏱️
   - Duração média por projeto
   - Diferença percentual
   - Indicador visual

6. **Métricas RAG** 🔍
   - Total de retrievals (apenas COM RAG)
   - Média por projeto

7. **Comparação Detalhada por Projeto** 📋
   - Comparação lado a lado de cada projeto
   - Todas as métricas por projeto

8. **Resumo Executivo** 📈
   - Impacto geral do RAG
   - Conclusões por métrica

## 📝 Projetos de Teste

Os mesmos 5 projetos são usados em ambos os baselines:

1. **Todo List CLI** - Aplicação CLI para gerenciar tarefas
2. **URL Shortener API** - API REST para encurtar URLs
3. **Weather CLI** - Ferramenta CLI de previsão do tempo
4. **Password Generator** - Gerador de senhas seguras
5. **Markdown to HTML Converter** - Conversor Markdown para HTML

## 🎯 Interpretação dos Resultados

### Indicadores de Impacto:

- **< 5% de diferença**: NEUTRO - Impacto mínimo
- **5-20% de diferença**: MODERADO - Impacto visível
- **> 20% de diferença**: SIGNIFICATIVO - Impacto alto

### Símbolos:

- 📈 = Aumento (RAG maior que sem RAG)
- 📉 = Redução (RAG menor que sem RAG)
- = = Neutro (< 0.01% diferença)

### Cenários Esperados:

#### Cenário 1: RAG Aumenta Custos/Tokens
- **Causa**: Contexto adicional recuperado do knowledge base
- **Trade-off**: Maior qualidade vs maior custo
- **Decisão**: Vale a pena se qualidade melhorar significativamente

#### Cenário 2: RAG Reduz Custos/Tokens
- **Causa**: Respostas mais diretas com contexto relevante
- **Benefício**: Melhor eficiência com contexto adequado
- **Decisão**: Win-win (melhor qualidade E menor custo)

#### Cenário 3: RAG Neutro em Custos
- **Causa**: Custos de retrieval compensados por respostas mais eficientes
- **Benefício**: Melhor qualidade sem custo adicional
- **Decisão**: Claramente benéfico

## 🔧 Troubleshooting

### Erro: Relatório não encontrado

```bash
# Verificar se os testes foram executados
ls -la metrics/data/baseline_report.json
ls -la metrics/data/no_rag/baseline_report.json

# Se não existirem, executar:
./scripts/run_baseline_test.sh        # COM RAG
./scripts/run_baseline_no_rag.sh      # SEM RAG
```

### Erro: Projetos diferentes

Os dois baselines DEVEM usar os mesmos projetos. Verifique:
```python
# Em tests/test_baseline.py e tests/test_baseline_no_rag.py
TEST_PROJECTS = [...]  # Devem ser idênticos
```

### Erro: Comparação inválida

Se os baselines foram executados em momentos muito diferentes:
- Modelos podem ter mudado
- Custos podem ter mudado
- Re-execute ambos os baselines no mesmo dia

## 📚 Referências

- **Baseline COM RAG**: [BASELINE_TEST_GUIDE.md](./BASELINE_TEST_GUIDE.md)
- **RAG Integration**: [RAG_INTEGRATION.md](./RAG_INTEGRATION.md)
- **Plano de Estudo**: [PLANO_ESTUDO_RAG_METRICAS.md](./PLANO_ESTUDO_RAG_METRICAS.md)

## 🚦 Próximos Passos

1. ✅ Executar baseline COM RAG
2. ✅ Executar baseline SEM RAG
3. ✅ Comparar resultados
4. ⏳ Analisar qualidade dos outputs (manual)
5. ⏳ Decidir se RAG vale a pena
6. ⏳ Otimizar RAG (se necessário)
7. ⏳ Repetir testes com otimizações

## 📌 Notas Importantes

### Isolamento dos Testes
- Cada baseline usa arquivos separados (agents, tasks, crew)
- Métricas são salvas em diretórios separados
- Nenhum baseline interfere no outro

### Reprodutibilidade
- Mesmos projetos
- Mesmo modelo (gpt-4o-mini)
- Mesmas configurações (max_rpm, verbose, etc)
- Diferentes apenas em RAG tools

### Limitações
- **Métricas quantitativas apenas**: Não mede qualidade dos outputs
- **Variabilidade LLM**: Respostas podem variar entre execuções
- **Rate limits**: Aguarde 5s entre projetos para evitar rate limits

---

**Última atualização**: 2025-01-12
**Versão**: 1.0
