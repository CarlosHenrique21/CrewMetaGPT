# 📚 Documentação CrewAI Project

## Índice de Documentação

Bem-vindo à documentação completa do projeto CrewAI com RAG!

### 🚀 Guias de Início Rápido

- **[QUICK_START_TESTS.md](QUICK_START_TESTS.md)** - Resumo de todos os scripts e testes disponíveis
- **[SETUP_COMPLETO.md](SETUP_COMPLETO.md)** - Guia passo a passo de instalação e configuração

### 🔍 Sistema RAG

- **[RAG_INTEGRATION.md](RAG_INTEGRATION.md)** - Como o RAG funciona e está integrado no sistema
- Como os agentes usam a base de conhecimento
- Fluxo de retrieval e contexto

### 🧪 Testes e Baseline

- **[BASELINE_TEST_GUIDE.md](BASELINE_TEST_GUIDE.md)** - Guia completo de testes baseline
  - Como executar 5 projetos de teste
  - Métricas coletadas
  - Como analisar resultados

- **[BASELINE_COMPARISON.md](BASELINE_COMPARISON.md)** - Comparação COM RAG vs SEM RAG
  - Teste baseline sem RAG
  - Script de comparação detalhada
  - Análise de impacto do RAG
  - Interpretação de resultados

- **[DSPY_OPTIMIZATION.md](DSPY_OPTIMIZATION.md)** - Por que DSPy é Superior a AutoPDL
  - Comparação técnica detalhada
  - Vantagens do DSPy para sistemas multi-agente
  - Evidências e benchmarks
  - Guia de implementação

### 📊 Estudos e Métricas

- **[PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md)** - Plano completo de estudo comparativo
  - Fase 1: Baseline
  - Fase 2: RAG
  - Fase 3: Otimizado (AutoPDL + DSPy)
  - Metodologia científica
  - Protocolo de testes

### 🔧 Configuração e Setup

- **[TRACKING_STATUS_REPORT.md](TRACKING_STATUS_REPORT.md)** - Status do tracking com AgentOps
- **[FIX_LLM_TRACKING.md](FIX_LLM_TRACKING.md)** - Soluções de tracking LLM

### 📈 Comparações e Análises

- **[METAGPT_VS_CREWAI.md](METAGPT_VS_CREWAI.md)** - Comparação entre MetaGPT e CrewAI
- **[RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md)** - Resumo executivo do projeto
- **[CORREÇÕES_COMPLETAS.md](CORREÇÕES_COMPLETAS.md)** - Histórico de correções

## 🗂️ Organização por Categoria

### Para Iniciantes
1. [SETUP_COMPLETO.md](SETUP_COMPLETO.md) - Comece aqui
2. [QUICK_START_TESTS.md](QUICK_START_TESTS.md) - Scripts disponíveis
3. [RAG_INTEGRATION.md](RAG_INTEGRATION.md) - Entenda o RAG

### Para Desenvolvedores
1. [RAG_INTEGRATION.md](RAG_INTEGRATION.md) - Arquitetura do RAG
2. [TRACKING_STATUS_REPORT.md](TRACKING_STATUS_REPORT.md) - Observabilidade
3. [METAGPT_VS_CREWAI.md](METAGPT_VS_CREWAI.md) - Comparações técnicas

### Para Pesquisadores
1. [PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md) - Metodologia completa
2. [BASELINE_TEST_GUIDE.md](BASELINE_TEST_GUIDE.md) - Como coletar dados
3. [BASELINE_COMPARISON.md](BASELINE_COMPARISON.md) - Comparar COM vs SEM RAG
4. [RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md) - Resultados agregados

## 🔗 Links Rápidos

### Executar Testes
```bash
# Teste rápido (1 projeto)
cd .. && ./quick_test.sh

# Teste baseline COM RAG (5 projetos)
cd .. && ./scripts/run_baseline_test.sh

# Teste baseline SEM RAG (5 projetos)
cd .. && ./scripts/run_baseline_no_rag.sh

# Treinar pipeline DSPy (opcional, antes do próximo)
cd .. && python scripts/train_dspy_optimizer.py

# Teste baseline COM RAG + DSPy (5 projetos otimizados)
cd .. && ./scripts/run_baseline_dspy.sh

# Comparar os 3 baselines
cd .. && python scripts/compare_all_baselines.py

# Ou comparar apenas 2
cd .. && python scripts/compare_baselines.py

# Analisar resultados
cd .. && python scripts/analyze_baseline.py
```

### Ver Código
```bash
# Core do projeto
cd .. && ls -la *.py

# Sistema RAG
cd .. && ls -la rag/

# Sistema de métricas
cd .. && ls -la metrics/
```

### Explorar Base de Conhecimento
```bash
cd .. && ls -la knowledge_base/
```

## 📖 Como Usar Esta Documentação

1. **Se você é novo**: Comece com [SETUP_COMPLETO.md](SETUP_COMPLETO.md)
2. **Se quer testar**: Veja [QUICK_START_TESTS.md](QUICK_START_TESTS.md)
3. **Se quer entender o RAG**: Leia [RAG_INTEGRATION.md](RAG_INTEGRATION.md)
4. **Se vai fazer pesquisa**: Estude [PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md)

## 🆘 Precisa de Ajuda?

- Veja [TRACKING_STATUS_REPORT.md](TRACKING_STATUS_REPORT.md) para troubleshooting
- Consulte o [README principal](../README.md) para visão geral
- Revise [CORREÇÕES_COMPLETAS.md](CORREÇÕES_COMPLETAS.md) para soluções conhecidas

---

**Voltar para**: [README Principal](../README.md)
