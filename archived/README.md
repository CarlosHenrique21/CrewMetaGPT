# Archived Files

Este diretório contém arquivos obsoletos que não são mais utilizados no projeto, mas foram preservados para referência histórica.

## 📦 Conteúdo

### Versões Antigas do DSPy (Auto-otimização)
- `agents_dspy.py` - Agents com otimização automática do DSPy (não usado)
- `agents_dspy_manual.py` - Primeira versão manual (substituída por agents_crewai_dspy.py)
- `crew_dspy.py` - Crew com otimização automática (não usado)
- `crew_dspy_manual.py` - Primeira versão manual (substituída por crew_crewai_dspy.py)

### Scripts de Baseline Antigos
- `run_baseline_dspy.sh` - Versão com otimização automática (não funcionou)
- `run_baseline_dspy_fresh.sh` - Tentativa de fresh run (não funcionou)
- `run_baseline_dspy_manual.sh` - Versão DSPy puro sem CrewAI (não rastreava tudo)
- `train_dspy_optimizer.py` - Script de treinamento do optimizer (não usado mais)

### Testes Temporários/Debugging
- `test_dspy_basic.py` - Teste básico do DSPy
- `test_dspy_llm.py` - Teste de LLM calls
- `test_manual_with_logging.py` - Teste com logging verbose
- `test_baseline_dspy.py` - Teste de baseline antigo
- `test_baseline_dspy_fresh.py` - Teste de baseline fresh
- `test_crewai_tracking.py` - Teste de tracking do CrewAI
- `test_llm_tracking_fixed.py` - Teste de LLM tracking
- `test_tracking.py` - Teste geral de tracking

### Scripts Temporários
- `quick_test.sh` - Script rápido de teste
- `run_fresh_test_clean.sh` - Script de teste limpo
- `run_dspy_training_clean.py` - Script de treinamento limpo

## ⚠️ Importante

**Estes arquivos NÃO devem ser usados.**

A versão atual e funcional do projeto usa:
- `agents_crewai_dspy.py` (agents com DSPy + CrewAI)
- `crew_crewai_dspy.py` (crew com DSPy + CrewAI)
- `scripts/run_baseline_crewai_dspy.sh` (baseline completo)
- `tests/test_crewai_dspy.py` (teste único)

Estes arquivos mantêm a integração completa do CrewAI com tracking do AgentOps.

## 🗑️ Por Que Foram Arquivados?

### Problemas das Versões Antigas

1. **DSPy Auto-otimização** (`agents_dspy.py`, `crew_dspy.py`):
   - Usava cache de demonstrações
   - Não fazia LLM calls reais
   - 0 tokens, 0 custo (suspeito!)

2. **DSPy Manual Puro** (`agents_dspy_manual.py`, `crew_dspy_manual.py`):
   - Bypass completo do CrewAI framework
   - AgentOps só rastreava LLM calls
   - Não rastreava agents, tasks, tools
   - Não executava tasks corretamente
   - Não criava arquivos

3. **Scripts de Baseline Antigos**:
   - Tentaram várias abordagens que não funcionaram
   - Circular import issues
   - Tracking incompleto

### Solução Final (Atual)

A abordagem híbrida atual (`agents_crewai_dspy.py` + `crew_crewai_dspy.py`):
- ✅ Usa CrewAI framework (agents, tasks, tools)
- ✅ Incorpora DSPy few-shot optimization nos prompts
- ✅ Rastreia TUDO no AgentOps (agents, tasks, tools, LLM, costs)
- ✅ Executa tasks corretamente
- ✅ Cria arquivos usando tools
- ✅ Sem circular imports

---

**Data de Arquivamento**: 2025-11-13
**Motivo**: Substituição por implementação híbrida funcional
